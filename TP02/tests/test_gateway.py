from sources.events_and_messages import Message, Event, EventType
from sources.gateway import Gateway
from sources.queue import Queue
from sources.server import Server


def test_send_message():
    gateway: Gateway = Gateway(
        t_server_count=1,
        t_server_starting_count=4,
        t_queue_limit=4,
        t_avg_req_by_time_unit=1,
    )
    
    message1 = Message(1, 3)
    message1.set_message_send_time(0.2)
    message1.set_message_arrival_time(1.2)
    event1 = Event(1, EventType.MSG_DEPT, message1)
    
    msg_list = gateway.send_message(event1.get_message(), 1.3)

    assert msg_list[0] == message1
    Message.reset_ids()
    
    
def test_send_message_dropped_or_in_queue():
    gateway: Gateway = Gateway(
        t_server_count=1,
        t_server_starting_count=4,
        t_queue_limit=1,
        t_avg_req_by_time_unit=0.1,
    )
    
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    event1 = Event(1, EventType.MSG_DEPT, message1)
    msg_list = gateway.send_message(event1.get_message(), 1.2)
    assert msg_list[0] == message1
    
    message2 = Message(1, 3)
    message2.set_message_send_time(0.1)
    message2.set_message_arrival_time(1.1)
    event2 = Event(2, EventType.MSG_DEPT, message2)
    msg_list = gateway.send_message(event2.get_message(), 1.3)
    assert len(msg_list) == 0
    
    message3 = Message(1, 4)
    message3.set_message_send_time(0.2)
    message3.set_message_arrival_time(1.1)
    event3 = Event(3, EventType.MSG_DEPT, message3)
    msg_list = gateway.send_message(event3.get_message(), 1.4)

    assert len(msg_list) == 0
    Message.reset_ids()


