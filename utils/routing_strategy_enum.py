from enum import Enum

class RoutingStrategy(Enum):
    FluidQ = 'routing_by_fluid_q'
    JLCRZero = 'rouing_by_jlcr_0'
    JLCRHalf = 'rouing_by_jlcr_0.5'
    JLCROne = 'rouing_by_jlcr_1'
    SW = 'routing_by_sw'
    