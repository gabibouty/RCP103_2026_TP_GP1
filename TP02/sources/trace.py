from sources.events_and_messages import Event, EventType, Message
import csv


def get_time_and_nodes(e: Event):
    if e.get_event_type() == EventType.SEND_MSG:
        source = e.get_message().get_message_source()
        destination = 0
        node = source
    elif e.get_event_type() == EventType.RECV_MSG:
        source = e.get_message().get_message_source()
        destination = 0
        node = 0
    else:
        source = 0
        destination = e.get_message().get_message_destination()
        node = 0
    return node, source, destination, e.get_event_time()


def generateTraceOut(t_event: list[Event]):
    print(f"\ntime\tnode\tevent\t\tsrc\tdst\tmsgID")

    for e in t_event:
        node, source, destination, time = get_time_and_nodes(e)
        print(
            f"{round(time, 4)}\t"
            f"{node}\t"
            f"{e.get_event_type().name}\t"
            f"{source}\t"
            f"{destination}\t"
            f"{e.get_message().get_message_id()}\t"
        )


def generateTraceCSV(t_event: list[Event]):
    # https://docs.python.org/fr/3/library/csv.html
    with open("trace.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";", quotechar='"')
        spamwriter.writerow(["time", "node", "event", "src", "dst", "msgID"])
        for e in t_event:
            node, source, destination, time = get_time_and_nodes(e)
            spamwriter.writerow(
                [
                    time,
                    node,
                    e.get_event_type().name,
                    source,
                    destination,
                    e.get_message().get_message_id(),
                ]
            )
