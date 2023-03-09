import heapq

from .event import Event

class EventManager(object):
    """ event mamager, powered by package:heapq, ordered by timestamp.  """
    
    def __init__(self) -> None:
        self._q = []
    
    @property
    def empty(self) -> bool:
        if len(self._q) <= 0:
            return True
        return False
    
    def enqueue(self, e:Event) -> None:
        heapq.heappush(self._q, e)
        
    def dequeue(self) -> Event:
        assert self.empty is not True
        return heapq.heappop(self._q)