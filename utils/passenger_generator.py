import numpy as np 
from abc import abstractmethod, ABCMeta
from event_handler.event import Event
from event_handler.event_type import EventType

class PassGen(metaclass=ABCMeta):
    """ interface class powered by package:abc """
    
    @abstractmethod
    def get_passenger(self, r_index):
        pass
    
    
class ParamPassGen(PassGen):
    """ passenger generator based on parameter lambda. 
    
        note that: 1 unit time in the system is equal to 10 minutes in real world.
    """
    
    def __init__(self) -> None:  
        self._lbd = None
        self._timestamp = None
    
    def set_param(self, lbd, car_num) -> None:
        self._car_num = car_num
        self._lbd = lbd
        if self._timestamp is None:
            self._timestamp = np.zeros(len(self._lbd))  
    
    def reset_passgen(self) -> None:
        self._lbd = None
        self._timestamp = None
    
    def get_passenger(self, r_index) -> Event:
        
        assert self._lbd is not None
        assert r_index < len(self._lbd)
        
        t = np.random.exponential(scale=1 / (self._car_num * self._lbd[r_index]))
        self._timestamp[r_index] += t
        
        return Event(
            type=EventType.PassengerArrivalEvent, 
            timestamp=self._timestamp[r_index],
            source=None,
            dest=r_index
        )


class RealDataPassGen(PassGen):
    """ passenger generator based on real data """
    
    def get_passenger(self, r_index):
        return super().get_passenger(r_index)