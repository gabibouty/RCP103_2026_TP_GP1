from sources.events_and_messages import Event
from collections import deque

class Queue:

    # https://docs.python.org/3.13/library/collections.html#deque-objects
    def __init__(self):
        self.queue = deque()

    def put(self, t_event: Event):
        # append to the right of the queue
        self.queue.append(t_event)

    def get(self) -> Event:
        # remove form the left of the queue
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue.popleft()

    def is_empty(self) -> bool:
        return True if len(self.queue) == 0 else False

    def size(self) -> int:
        return len(self.queue)
        
    def index(self, t_event: Event) -> int:
        return self.queue.index(t_event)
    
    def __str__(self) -> str:
        return (
            f"Size: {self.size()}\n"
            f"Elements : {str(list(self.queue))}"
        )
