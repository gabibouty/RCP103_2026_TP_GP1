from sources.engine import Engine, TraceType
from sources.stats import *
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from sources.constants import SERVER_AVG_TIME, TRANSMISSION_DURATION


def main():

    SIMULATION_DURATION = 100
    QUEUE_SIZES = [4]
    CLIENTS_COUNT = [1]
    SERVERS_COUNT = [1]

    combinations = []
    for c in CLIENTS_COUNT:
        for s in SERVERS_COUNT:
            for q in QUEUE_SIZES:
                combinations.append((c, s, q))

    print()

    for _client_count, _server_count, _queue_size in combinations:
        print(
            f"Launch simulation: Cli={_client_count}, Ser={_server_count}, Q={_queue_size}"
        )

        engine: Engine = Engine(
            SIMULATION_DURATION,
            t_server_count=_server_count,
            t_client_count=_client_count,
            t_queue_limit=_queue_size,
        )

        engine.run()
        
        # engine.log(TraceType.STDIO)
        events = engine.log(TraceType.EVENT_LIST)
        assert len(events) > 0

        avg_time = average_time_in_queue(events)
        print(f"Avg time in queue = {avg_time}")
        max_time = maximum_waiting_time_in_queue(events)
        print(f"Max time in queue = {max_time}")

        print()

        sended_count = []
        dropped_count = []
        transmit_count = []
        still_in_transmission = []
        still_in_queue = []
        x = []
        for t in range(0, SIMULATION_DURATION + 1):
            _time = float(t)
            x.append(t)

            sended_count.append(total_messages_sended(events, _time))
            transmit_count.append(total_messages_transmit(events, _time))
            dropped_count.append(messages_dropped_at(events, _queue_size, _time))
            still_in_transmission.append(
                total_messages_still_in_transmission(events, _time) * 10
            )
            still_in_queue.append(messages_in_queue_at(events, _queue_size, _time) * 10)

        plt.plot(
            x,
            sended_count,
            linestyle="-",
            color="blue",
            linewidth=2,
            label="sended",
        )

        plt.plot(
            x,
            dropped_count,
            linestyle="-",
            color="red",
            linewidth=2,
            label="dropped",
        )

        plt.plot(
            x,
            transmit_count,
            linestyle="-",
            color="green",
            linewidth=2,
            label="transmit",
        )

        plt.plot(
            x,
            still_in_transmission,
            linestyle="-",
            color="orange",
            linewidth=2,
            label="in transmission (x10)",
        )

        plt.plot(
            x,
            still_in_queue,
            linestyle="-",
            color="purple",
            linewidth=2,
            label="in queue (x10)",
        )

        plt.xlabel("$time$")
        plt.title(f"Cli={_client_count}, Ser={_server_count}, Q={_queue_size}")
        plt.legend()

        plt.grid(True)
        # add block=True in order to show graphical content on GNU/Linux
        plt.show(block=True)


if __name__ == "__main__":
    main()
