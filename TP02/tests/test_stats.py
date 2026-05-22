from sources.stats import *
from sources.engine import Engine, TraceType


def test_all_stats():
    SIMULATION_DURATION = 10
    QUEUE_SIZE = 4
    engine: Engine = Engine(
        SIMULATION_DURATION,
        t_server_count=4,
        t_client_count=1,
        t_queue_limit=QUEUE_SIZE,
    )

    engine.run()

    # UNCOMMENT TO PRINT TRACE
    # engine.log(TraceType.STDIO)

    print()

    events = engine.log(TraceType.EVENT_LIST)

    avg_time = average_time_in_queue(events)
    print(f"Avg time in queue = {avg_time}")
    max_time = maximum_waiting_time_in_queue(events)
    print(f"Max time in queue = {max_time}")
    # TODO: maybe the assert could confirm mathematical rule
    assert avg_time != 0.0
    assert max_time != 0.0

    print()

    sended_count = 0
    transmit_count = 0
    dropped_count = 0
    still_in_transmission = 0
    still_in_queue = 0
    for t in range(0, SIMULATION_DURATION + 1):
        _sended_count = total_messages_sended(events, t) - sended_count
        _transmit_count = total_messages_transmit(events, t) - transmit_count
        _dropped_count = messages_dropped_at(events, QUEUE_SIZE, t) - dropped_count

        still_in_transmission = total_messages_still_in_transmission(events, t)
        still_in_queue = messages_in_queue_at(events, QUEUE_SIZE, t)
        print(f"STATS @ {t}")
        print(f"\tSended in interval = {_sended_count}")
        print(f"\tStill in transmission = {still_in_transmission}")
        print(f"\tStill in queue = {still_in_queue}")
        print(f"\tTransmit in interval = {_transmit_count}")
        print(f"\tDropped in interval = {_dropped_count}")

        sended_count += _sended_count
        transmit_count += _transmit_count
        dropped_count += _dropped_count

        assert _sended_count == still_in_transmission
        assert (
            sended_count
            == transmit_count + dropped_count + still_in_queue + still_in_transmission
        )

    print()

    print(f"STATS @ END")
    print(f"\tTotal sended = {sended_count}")
    print(f"\tStill in transmission = {still_in_transmission}")
    print(f"\tStill in queue = {still_in_queue}")
    print(f"\tTotal transmit = {transmit_count}")
    print(f"\tTotal dropped = {dropped_count}")
