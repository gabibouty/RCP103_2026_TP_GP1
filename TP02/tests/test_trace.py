from sources.events_and_messages import Message, Event, EventType
from sources.trace import get_time_and_node, generateTraceOut, generateTraceCSV
import csv
import os

def test_get_time_and_node_event_SEND_MSG():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.SEND_MSG, 0.0, message)
    assert get_time_and_node(event) == (1, 0.0)


def test_get_time_and_node_event_RECV_MSG():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.RECV_MSG, 0.0, message)
    assert get_time_and_node(event) == (2, 1.1)


def test_get_time_and_node_event_MSG_DEPT():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.MSG_DEPT, 0.0, message)
    assert get_time_and_node(event) == (2, 2.6)
    
def test_generateTraceOut_SEND_MSG(capsys):
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)
    
    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, 0.0, message1)
    event2 = Event(2, EventType.SEND_MSG, 0.0, message2)
    t_event = [event1, event2]
    
    generateTraceOut(t_event)
    
    # https://docs.pytest.org/en/6.2.x/capture.html
    capture = capsys.readouterr()
    assert f"time\tnode\tevent\tsrc\tdst\tmsgID" in capture.out
    assert f"0.0\t1\tSEND_MSG\t1\t2\t1" in capture.out
    assert f"0.2\t1\tSEND_MSG\t1\t3\t2" in capture.out
    
    
def test_generateTraceOut_RECV_MSG(capsys):
    message1 = Message(42, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)
    
    message2 = Message(43, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.RECV_MSG, 0.0, message1)
    event2 = Event(2, EventType.RECV_MSG, 0.0, message2)
    t_event = [event1, event2]
    
    generateTraceOut(t_event)
    
    # https://docs.pytest.org/en/6.2.x/capture.html
    capture = capsys.readouterr()
    assert f"time\tnode\tevent\tsrc\tdst\tmsgID" in capture.out
    assert f"1.1\t2\tRECV_MSG\t1\t2\t42" in capture.out
    assert f"1.2\t3\tRECV_MSG\t1\t3\t43" in capture.out
    
def test_generateTraceOut_MSG_DEPT(capsys):
    message1 = Message(42, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)
    
    message2 = Message(43, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.MSG_DEPT, 0.0, message1)
    event2 = Event(2, EventType.MSG_DEPT, 0.0, message2)
    t_event = [event1, event2]
    
    generateTraceOut(t_event)
    
    # https://docs.pytest.org/en/6.2.x/capture.html
    capture = capsys.readouterr()
    assert f"time\tnode\tevent\tsrc\tdst\tmsgID" in capture.out
    assert f"2.6\t2\tMSG_DEPT\t1\t2\t42" in capture.out
    assert f"4.6\t3\tMSG_DEPT\t1\t3\t43" in capture.out
    
    
    
def test_generateTraceCSV():
    message1 = Message(42, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)
    
    message2 = Message(43, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, 0.0, message1)
    event2 = Event(2, EventType.MSG_DEPT, 0.0, message2)
    t_event = [event1, event2]
    
    generateTraceCSV(t_event)
    
    # https://docs.python.org/3/library/csv.html
    with open("trace.csv", mode="r", newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar='"')
        rows = list(spamreader)
    assert rows[0] == ["time", "node", "event", "src", "dst", "msgID"]
    assert rows[1] == ["0.0", "1", "SEND_MSG", "1", "2", "42"]
    assert rows[2] == ["4.6", "3", "MSG_DEPT", "1", "3", "43"]
    os.remove("trace.csv")
