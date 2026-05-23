from sources.stats import *
from sources.engine import Engine, TraceType


def test_all_stats():
    SIMULATION_DURATION = 10
    QUEUE_SIZE = 4
    engine: Engine = Engine(
        SIMULATION_DURATION,
        t_server_count=2,
        t_client_count=2,
        t_queue_limit=QUEUE_SIZE,
    )

    engine.run()

    # UNCOMMENT TO PRINT TRACE
    engine.log(TraceType.STDIO)

    print()

    events = engine.log(TraceType.EVENT_LIST)

    avg_time = average_time_in_queue(events)
    print(f"Avg time in queue = {avg_time}")
    max_time = maximum_waiting_time_in_queue(events)
    print(f"Max time in queue = {max_time}")
    # With this configuration, queue must be used
    assert avg_time != 0.0
    assert max_time != 0.0

    print()

    sended_count = 0
    transmit_count = 0
    dropped_count = 0
    still_in_transmission = 0
    still_in_queue = 0
    for t in range(0, SIMULATION_DURATION + 1):
        _time = float(t)
        _sended_count = total_messages_sended(events, _time)
        _transmit_count = total_messages_transmit(events, _time)
        _dropped_count = messages_dropped_at(events, QUEUE_SIZE, _time)
        still_in_transmission = total_messages_still_in_transmission(events, _time)
        still_in_queue = messages_in_queue_at(events, QUEUE_SIZE, _time)

        print(f"STATS @ {_time}")
        print(f"\tSended in interval = {_sended_count - sended_count}")
        print(f"\tStill in transmission = {still_in_transmission}")
        print(f"\tStill in queue = {still_in_queue}")
        print(f"\tTransmit in interval = {_transmit_count - transmit_count}")
        print(f"\tDropped in interval = {_dropped_count - dropped_count}")

        assert _sended_count - sended_count == still_in_transmission

        sended_count = _sended_count
        transmit_count = _transmit_count
        dropped_count = _dropped_count

        print(f"\tTotal sended = {sended_count}")
        print(f"\tTotal transmit = {transmit_count}")
        print(f"\tTotal dropped = {dropped_count}")

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


def test_all_stats_with_different_combination():
    SIMULATION_DURATION = 10
    QUEUE_SIZES = [4, 8, 12, 16]
    CLIENT_COUNT_MAX = 8
    SERVER_COUNT_MAX = 8

    combinations = []
    for c in range(1, CLIENT_COUNT_MAX + 1):
        for s in range(1, SERVER_COUNT_MAX + 1):
            for q in QUEUE_SIZES:
                combinations.append((c, s, q))

    print()
    for _client_count, _server_count, _queue_size in combinations:
        print(f"Test: Cli={_client_count}, Ser={_server_count}, Q={_queue_size}")

        engine: Engine = Engine(
            SIMULATION_DURATION,
            t_server_count=_server_count,
            t_client_count=_client_count,
            t_queue_limit=_queue_size,
        )

        engine.run()

        events = engine.log(TraceType.EVENT_LIST)
        assert len(events) > 0

        avg_time = average_time_in_queue(events)
        max_time = maximum_waiting_time_in_queue(events)
        # TODO: maybe the assert could confirm mathematical rule
        assert max_time > 0.0 if avg_time > 0.0 else max_time == 0.0

        sended_count = 0
        transmit_count = 0
        dropped_count = 0
        still_in_transmission = 0
        still_in_queue = 0
        for t in range(0, SIMULATION_DURATION + 1):
            _sended_count = total_messages_sended(events, t)
            _transmit_count = total_messages_transmit(events, t)
            _dropped_count = messages_dropped_at(events, _queue_size, t)
            still_in_transmission = total_messages_still_in_transmission(events, t)
            still_in_queue = messages_in_queue_at(events, _queue_size, t)

            assert _sended_count - sended_count == still_in_transmission

            sended_count = _sended_count
            transmit_count = _transmit_count
            dropped_count = _dropped_count

            assert (
                sended_count
                == transmit_count
                + dropped_count
                + still_in_queue
                + still_in_transmission
            )
