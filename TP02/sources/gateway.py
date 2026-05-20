from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler, SERVER_AVG_TIME
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV


class Gateway:

    # t_server_starting_count has to be set to the last client t_id + 1
    def __init__(self, t_server_count: int, t_server_starting_count: int,):
        self.__id: int = 0
    
        self.__servers: List[Server] = []
        for i in range(t_client_count):
            self.__servers.append(Server(t_server_starting_count + i, SERVER_AVG_TIME))
        
        self.__queue: Queue = Queue()
        
        
    def add_to_queue(self, msg: Message):
        self.__queue.put(msg)
        
    def __get_free_server(self, t_timestamp: float) -> Server:
        for server in self.__servers:
            if server.is_free(t_timestamp):
                return server
        return None
        
    def __get_next_workend(self) -> float:
        work_end = self.__servers[0].get_work_end()
        for server in self.__servers:
            work_end = min(work_end, server.get_work_end())
        return work_end
        
    def consume_message(self, current_time: float) -> Event:
        if not self.__queue.is_empty():
            server = self.__get_free_server(current_time)
            if server != None:
                msg = self.__queue.get()
                msg.set_message_server_time(current_time)
                msg.set_message_destination(server.get_id())
                self.__scheduler.add_event(t_event=)
                server.start_work(current_time)
                return Event(event_id, EventType.MSG_DEPT, msg)
        return None
        
