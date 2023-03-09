from enum import Enum

class EventType(Enum):
    PassengerArrivalEvent = 'passenger_arrival_event'
    FullCarArrivalEvent = 'full_car_arrival_event'
    EmptyCarArrivalEvent = 'empty_car_arrival_event'
    