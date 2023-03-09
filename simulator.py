import numpy as np 
from abc import abstractmethod, ABCMeta
from event_handler.event import Event
from event_handler.event_manager import EventManager
from event_handler.event_type import EventType
from logger import log
from utils.passenger_generator import ParamPassGen
from utils.routing_strategy_enum import RoutingStrategy
from utils.toolfunc import frac_allocation

class BaseSimulator():
    def __init__(self) -> None:
        self._passgen = None
    
    def set_passgen(self, pgen):
        self._passgen = pgen
    
    def run(self, 
        c_num: int, r_num: int, lbd_vec: np.ndarray, mu_mat: np.ndarray, p_mat: np.ndarray, 
        routing_strategy=RoutingStrategy.FluidQ, q_mat=None, time_limit=6
    ) -> None:
        event_manager = EventManager()
        
        if isinstance(self._passgen, ParamPassGen):
            self._passgen.set_param(lbd=lbd_vec, car_num=c_num)
        for i in range(r_num):  # event heap init
            event_manager.enqueue(self._passgen.get_passenger(i))
        
        e_mat = np.diag(frac_allocation(c_num, lbd_vec))
        f_mat = np.zeros((r_num, r_num))
        
        satisfied_cnt = np.zeros(r_num)
        arrival_cnt = np.zeros(r_num)
        
        timestamp = 0
        
        while True:
            assert event_manager.empty is not True
            event = event_manager.dequeue()
            
            if event.timestamp - timestamp > 3:
                self._get_utility(lbd_vec, arrival_cnt, satisfied_cnt)
                timestamp = event.timestamp
                satisfied_cnt = np.zeros(r_num)
                arrival_cnt = np.zeros(r_num)
                        
            if event.timestamp >= time_limit:
                break

            if event.type == EventType.PassengerArrivalEvent:
                event_manager.enqueue(self._passgen.get_passenger(event.dest))
                
                arrival_cnt[event.dest] += 1
                if(e_mat[event.dest, event.dest] <= 0):
                    continue
                satisfied_cnt[event.dest] += 1
            
                full_car_source = event.dest
                full_car_dest = np.random.choice(np.arange(r_num), p = p_mat[full_car_source])
                full_car_arrival_time = event.timestamp + 1 / mu_mat[full_car_source, full_car_dest]
    
                e_mat[event.dest, event.dest] -= 1
                f_mat[full_car_source, full_car_dest] += 1
                
                event_manager.enqueue(Event(
                    type=EventType.FullCarArrivalEvent, 
                    timestamp=full_car_arrival_time, 
                    source=full_car_source,
                    dest=full_car_dest
                ))
                
            elif event.type == EventType.FullCarArrivalEvent:
                
                empty_car_source =  event.dest
                empty_car_dest = self._get_empty_car_dest(
                    s=routing_strategy, c_num=c_num, r_num=r_num, source_region=empty_car_source, 
                    q_mat=q_mat, e_mat=e_mat, lbd_vec=lbd_vec, mu_mat=mu_mat
                )
                empty_car_arrival_time = event.timestamp + 1 / mu_mat[empty_car_source, empty_car_dest]

                f_mat[event.source, event.dest] -= 1    
                e_mat[empty_car_source, empty_car_dest] += 1
                if empty_car_source == empty_car_dest:  # no routing
                    continue
                
                event_manager.enqueue(Event(
                    type=EventType.EmptyCarArrivalEvent,
                    timestamp=empty_car_arrival_time,
                    source=empty_car_source,
                    dest=empty_car_dest
                ))
                
            elif event.type == EventType.EmptyCarArrivalEvent:
                e_mat[event.source, event.dest] -= 1
                e_mat[event.dest, event.dest] += 1
                
            else:
                pass
            
    def _get_utility(self, lbd: np.ndarray, arrival_cnt: np.ndarray, satisfied_cnt: np.ndarray) -> None:
        
        availability = satisfied_cnt / arrival_cnt
        log.info(f'availability: {availability}' )
        utility = np.dot(availability, lbd) / np.sum(lbd)
        log.info(f'utility: {utility}')
        
    def _get_empty_car_dest(self, 
        s: RoutingStrategy, r_num: int, source_region: int, 
        q_mat=None, lbd_vec=None, mu_mat=None, e_mat=None, c_num=None
    ):
        if s == RoutingStrategy.FluidQ:
            assert q_mat is not None
            return np.random.choice(np.arange(r_num), p = q_mat[source_region]) 
        elif s == RoutingStrategy.JLCRZero:
            assert e_mat is not None
            assert lbd_vec is not None
            return self._get_jlcr_dest(source_region=source_region, jlcr_param=0, lbd_vec=lbd_vec, e_mat=e_mat)
        elif s == RoutingStrategy.JLCRHalf:
            assert e_mat is not None
            assert lbd_vec is not None
            return self._get_jlcr_dest(source_region=source_region, jlcr_param=0.5, lbd_vec=lbd_vec, e_mat=e_mat)
        elif s == RoutingStrategy.JLCROne:
            assert e_mat is not None
            assert lbd_vec is not None
            # return source_region
            return self._get_jlcr_dest(source_region=source_region, jlcr_param=1, lbd_vec=lbd_vec, e_mat=e_mat)
        elif s == RoutingStrategy.SW:
            assert e_mat is not None
            assert lbd_vec is not None
            assert mu_mat is not None
            assert c_num is not None
            return self._get_sw_dest(r_num=r_num, c_num=c_num, source_region=source_region,lbd_vec=lbd_vec, mu_mat=mu_mat, e_mat=e_mat)
    
    def _get_jlcr_dest(self, source_region: int, jlcr_param: float, lbd_vec: np.ndarray, e_mat: np.ndarray):
        col_sum = np.sum(e_mat, axis=0)
        jclr_arr = col_sum / lbd_vec
        jclr_arr[source_region] = (1 - jlcr_param) * col_sum[source_region] / lbd_vec[source_region]
        min_index = np.argmin(jclr_arr)
        return min_index
        # if jclr_arr[source_region] == jclr_arr[min_index]: 
        #     return source_region
        # else: 
        #     return min_index
        
    def _get_sw_dest(self, r_num: int, c_num: int, source_region: int, lbd_vec: np.ndarray, mu_mat: np.ndarray, e_mat: np.ndarray):
        arr = []
        for j in range(r_num):
            val1 = 1 / mu_mat[source_region, j]
            val2 = (
                e_mat[j,j] + 1 / mu_mat[source_region, j] * (
                    np.dot(mu_mat[:, j], e_mat[:, j]) - mu_mat[j,j] * e_mat[j,j]
                ) - c_num * lbd_vec[j] / mu_mat[source_region, j]
            ) / (c_num * lbd_vec[j])
            arr.append(val1 + max(val2, 0))
            
        arr[source_region] = e_mat[source_region,source_region] / (c_num * lbd_vec[source_region])
        min_index = np.argmin(np.array(arr))
        return min_index