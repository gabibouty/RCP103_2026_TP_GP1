from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV
from sources.constants import SERVER_AVG_TIME


class Gateway:

    # t_server_starting_count has to be set to the last client t_id + 1
    def __init__(self, t_server_count: int, t_server_starting_count: int,t_queue_limit: int = 4096):
        self.__id: int = 0
    
        self.__servers: List[Server] = []
        for i in range(t_server_count):
            self.__servers.append(Server(t_server_starting_count + i, SERVER_AVG_TIME))
        
        self.__queue: Queue = Queue(size=t_queue_limit)
        
        
    def send_message(self, msg: Message):
        self.__queue.put(msg)
        
    def __get_free_server(self, t_timestamp: float) -> Server:
        for server in self.__servers:
            if server.is_free(t_timestamp):
                return server
        return None
        
    def try_start_server_job(self, t_time: float) -> list[Message]:
        msg_list = []
        server = self.__get_free_server(t_time)
        while server != None and not self.__queue.is_empty():
            msg = self.__queue.get()
            msg.set_message_server_time(t_time)
            msg.set_message_destination(server.get_id())
            msg_list.append(msg)
            server.start_work(t_time)
            server = self.__get_free_server(t_time)
        return msg_list
