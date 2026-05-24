from sources.engine import Engine, TraceType
from sources.stats import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages


def __add_bar(area, t_range, t_data, t_bottom, t_label, t_color):
    area.bar(
        t_range,
        t_data,
        bottom=t_bottom,
        label=t_label,
        color=t_color,
        align="edge",
        width=1.0,
        linewidth=0.5,
        edgecolor="black",
    )


def main():
    SIMULATION_DURATION = 10
    QUEUE_SIZES = [4, 8, 12, 16]
    CLIENTS_COUNT = [1, 2, 4, 8]
    SERVERS_COUNT = [1, 2, 4, 8]

    combinations = []
    for c in CLIENTS_COUNT:
        for s in SERVERS_COUNT:
            for q in QUEUE_SIZES:
                combinations.append((c, s, q))

    print()

    with PdfPages("simulation_results.pdf") as pdf:
        for _client_count, _server_count, _queue_size in combinations:
            print(
                f"Launch simulation: Cli={_client_count}, Ser={_server_count}, Q={_queue_size}, Duration={SIMULATION_DURATION}"
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

            dropped_count = []
            transmit_count = []
            still_in_transmission = []
            still_in_queue = []
            _t = []
            for t in range(0, SIMULATION_DURATION):
                _time = float(t)
                _t.append(t)

                previous = 0 if len(transmit_count) == 0 else transmit_count[-1]
                transmit_count.append(total_messages_transmit(events, _time) - previous)
                previous = 0 if len(dropped_count) == 0 else dropped_count[-1]
                dropped_count.append(
                    messages_dropped_at(events, _queue_size, _time) - previous
                )
                still_in_transmission.append(
                    total_messages_still_in_transmission(events, _time) * 10
                )
                still_in_queue.append(
                    messages_in_queue_at(events, _queue_size, _time) * 10
                )

            # Graph

            plt.figure(figsize=(11.69, 8.27))
            gs = gridspec.GridSpec(2, 1, height_ratios=[1.8, 0.2])
            ax1 = plt.subplot(gs[0, 0])
            ax2 = plt.subplot(gs[1, 0])

            _bottom = [0] * (SIMULATION_DURATION)
            assert len(_t) == len(_bottom)
            assert len(_t) == len(still_in_transmission)
            __add_bar(
                ax1, _t, still_in_transmission, _bottom, "in transmission", "#1f77b4"
            )
            _bottom = [a + b for a, b in zip(still_in_transmission, _bottom)]
            __add_bar(ax1, _t, still_in_queue, _bottom, "in queue", "#f1c62a")
            _bottom = [a + b for a, b in zip(still_in_queue, _bottom)]
            __add_bar(ax1, _t, dropped_count, _bottom, "dropped", "#b4301f")
            _bottom = [a + b for a, b in zip(dropped_count, _bottom)]
            __add_bar(ax1, _t, transmit_count, _bottom, "transmit", "#1fb42bd3")

            # Legend
            ax1.set_xlabel("$time$")
            ax1.set_ylabel("Message count")
            ax1.set_title(
                f"Duration={SIMULATION_DURATION}, Clients={_client_count}, Servers={_server_count}, Q={_queue_size}"
            )
            ax1.legend()

            # Comment
            text = f"\nMessage sended = {total_messages_sended(events, SIMULATION_DURATION)}"
            text += f"\nMessage transmitted = {total_messages_transmit(events, SIMULATION_DURATION)}"
            text += f"\nMessage dropped = {messages_dropped_at(events, _queue_size, SIMULATION_DURATION)}"
            text += f"\nStill in transmission = {total_messages_still_in_transmission(events, SIMULATION_DURATION)}"
            text += f"\nStill in queue = {messages_in_queue_at(events, _queue_size, SIMULATION_DURATION)}"
            text += f"\nAverage time in queue = {average_time_in_queue(events):.4f}"
            text += (
                f"\nMaximum time in queue = {maximum_waiting_time_in_queue(events):.4f}"
            )

            ax2.text(
                x=0,
                y=1,
                s=text,
                fontsize=12,
            )
            ax2.axis("off")

            plt.tight_layout()
            pdf.savefig()
            plt.close()


if __name__ == "__main__":
    main()
