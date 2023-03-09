import numpy as np

from config.two_region_config import (
    CAR_NUM, REGION_NUM, LBD_ARR, P_MAT, MU_MAT
)
from utils.data_utils import read_realdata
from utils.routing_strategy_enum import RoutingStrategy
from utils.passenger_generator import ParamPassGen
from fluid_model import FluidModel
from logger import log
# from naive_simulator import NaiveSimulator
from simulator import BaseSimulator

if __name__ == "__main__":
    
    fluid_model = FluidModel()
    routing_matrix_q = fluid_model.get_fluid_q(REGION_NUM, LBD_ARR, MU_MAT, P_MAT)
    log.info('fluid empty car routing matrix is:')
    log.info(routing_matrix_q)
    
    naive_simulator = BaseSimulator()
    naive_simulator.set_passgen(ParamPassGen())
    naive_simulator.run(
        c_num=CAR_NUM, r_num= REGION_NUM, lbd_vec= LBD_ARR, mu_mat= MU_MAT, p_mat=P_MAT,
        routing_strategy=RoutingStrategy.FluidQ, q_mat=routing_matrix_q, time_limit=30
    )
    
    # data =  read_realdata(1, 17, 18, None)
    # log.info(data)