from sources.events_and_messages import Event, EventType, Message
import csv


def get_time_and_node(e: Event):
    if e.get_event_type() == EventType.SEND_MSG:
        node = e.get_message().get_message_source()
    else:
        node = e.get_message().get_message_destination()
    return node, e.get_event_time()


def generateTraceOut(t_event: list[Event]):
    print(f"\ntime\tnode\tevent\t\tsrc\tdst\tmsgID")

    for e in t_event:
        node, time = get_time_and_node(e)
        print(
            f"{time:.4}\t"
            f"{node}\t"
            f"{e.get_event_type().name}\t"
            f"{e.get_message().get_message_source()}\t"
            f"{e.get_message().get_message_destination()}\t"
            f"{e.get_message().get_message_id()}\t"
        )


def generateTraceCSV(t_event: list[Event]):
    # https://docs.python.org/fr/3/library/csv.html
    with open("trace.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";", quotechar='"')
        spamwriter.writerow(["time", "node", "event", "src", "dst", "msgID"])
        for e in t_event:
            node, time = get_time_and_node(e)
            spamwriter.writerow(
                [
                    time,
                    node,
                    e.get_event_type().name,
                    e.get_message().get_message_source(),
                    e.get_message().get_message_destination(),
                    e.get_message().get_message_id(),
                ]
            )
