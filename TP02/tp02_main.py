from sources.engine import Engine, TraceType
from sources.stats import *
from sources.constants import SERVER_LAMBDA
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from sources.trace import get_time_and_nodes
from sources.constants import SERVER_LAMBDA


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

    # Client/Server/Q
    configuration = [
        [1, 1, None],
        [1, 1, 4],
        [1, 1, 8],
        [1, 3, 8],
    ]

    with PdfPages("simulation_results.pdf") as pdf:
        CLIENT_LAMBDAS = [4, 6, 8, 12]
        for _client_count, _server_count, _queue_size in configuration:
            for _client_lambda in CLIENT_LAMBDAS:
                title = f"Duration={SIMULATION_DURATION}, "
                title += f"Clients count={_client_count}, "
                title += f"Client's λ={_client_lambda}, "
                title += f"Servers count={_server_count}, "
                title += f"Q={"inf." if _queue_size is None else _queue_size}"
                print(f"Launch simulation: {title}")

                # -----------------------------------------------------------
                # Launch simulation
                # -----------------------------------------------------------
                engine: Engine = Engine(
                    SIMULATION_DURATION,
                    t_server_count=_server_count,
                    t_client_count=_client_count,
                    t_queue_limit=_queue_size,
                    t_client_lambda=_client_lambda,
                )

                engine.run()

                events = engine.log(TraceType.EVENT_LIST)
                assert len(events) > 0

                # -----------------------------------------------------------
                # Compute stats
                # -----------------------------------------------------------
                dropped_count = []
                transmit_count = []
                still_in_transmission = []
                still_in_queue = []
                _t = []
                for t in range(0, SIMULATION_DURATION):
                    _time = float(t)
                    _t.append(t)

                    previous = 0 if len(transmit_count) == 0 else transmit_count[-1]
                    transmit_count.append(
                        total_messages_transmit(events, _time) - previous
                    )
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

                # -----------------------------------------------------------
                # PAGE 1: Draw bar graph
                # -----------------------------------------------------------
                fig, ax = plt.subplots(figsize=(11.69, 8.27))
                _bottom = [0] * (SIMULATION_DURATION)
                assert len(_t) == len(_bottom)
                assert len(_t) == len(still_in_transmission)
                __add_bar(
                    ax,
                    _t,
                    still_in_transmission,
                    _bottom,
                    "in transmission",
                    "#1f77b4",
                )
                _bottom = [a + b for a, b in zip(still_in_transmission, _bottom)]
                __add_bar(ax, _t, still_in_queue, _bottom, "in queue", "#f1c62a")
                _bottom = [a + b for a, b in zip(still_in_queue, _bottom)]
                __add_bar(ax, _t, dropped_count, _bottom, "dropped", "#b4301f")
                _bottom = [a + b for a, b in zip(dropped_count, _bottom)]
                __add_bar(ax, _t, transmit_count, _bottom, "transmit", "#1fb42bd3")

                plt.xlabel("$time$")
                plt.ylabel("Message count")
                _fontdict = {}
                _fontdict["fontweight"] = "bold"
                plt.title(title, fontdict=_fontdict)
                plt.legend()

                plt.tight_layout()
                pdf.savefig()
                plt.close()

                # -----------------------------------------------------------
                # PAGE 2
                # -----------------------------------------------------------
                fig = plt.figure(figsize=(11.69, 8.27))
                gs = gridspec.GridSpec(1, 2)
                ax1 = plt.subplot(gs[0, 0])
                ax2 = plt.subplot(gs[0, 1])
                ax1.axis("off")
                ax2.axis("off")

                # -----------------------------------------------------------
                # Draw Trace
                # -----------------------------------------------------------
                all_data = []
                for e in events:
                    node, source, destination, time = get_time_and_nodes(e)
                    all_data.append(
                        [
                            round(time, 4),
                            node,
                            e.get_event_type().name,
                            source,
                            destination,
                            e.get_message().get_message_id(),
                        ]
                    )

                table_data = []

                all_data_len = len(all_data)
                MAX_ROWS = 44
                found_t1 = False
                last_row_index = len(all_data) - MAX_ROWS
                for i in range(all_data_len):
                    if all_data[i][0] <= 1.0 or i >= last_row_index:
                        table_data.append(all_data[i])
                    elif not found_t1:
                        found_t1 = True
                        table_data.append(all_data[i])
                        table_data.append(["...", "...", "...", "...", "...", "..."])
                        table_data.append(["...", "...", "...", "...", "...", "..."])
                        last_row_index = last_row_index + len(table_data)

                table_data.append(["END", "---", "---", "---", "---", "---"])
                column_titles = [
                    "time",
                    "node",
                    "event",
                    "src",
                    "dst",
                    "msgID",
                ]
                column_width = np.full(len(column_titles), 0.5)
                column_width[1] = 0.25
                column_width[3] = 0.25
                column_width[4] = 0.25
                column_width[5] = 0.25
                trace = ax1.table(
                    cellText=table_data,
                    colLabels=column_titles,
                    colWidths=column_width,
                    loc="center",
                    cellLoc="center",
                    bbox=[0.0, 0.0, 1.0, 1.0],
                )
                trace.auto_set_font_size(True)
                for col in range(len(column_titles)):
                    cell = trace.get_celld()[(0, col)]
                    cell.set_facecolor("#A30018")
                    cell.set_text_props(weight="bold", color="#FFFFFF")
                    cell = trace.get_celld()[(MAX_ROWS + 1, col)]
                    cell.set_facecolor("#A30018")
                    cell.set_text_props(weight="bold", color="#FFFFFF")

                # -----------------------------------------------------------
                # Draw comments
                # -----------------------------------------------------------
                text = f"Configuration:\n{title}\n\n"
                text += f"\nTotal message sended = {total_messages_sended(events, SIMULATION_DURATION)}"
                text += f"\nTotal message transmitted = {total_messages_transmit(events, SIMULATION_DURATION)}"
                text += f"\nTotal message dropped = {messages_dropped_at(events, _queue_size, SIMULATION_DURATION)}"
                text += f"\n\nStill in transmission at end = {total_messages_still_in_transmission(events, SIMULATION_DURATION)}"
                text += f"\nStill in queue at end = {messages_in_queue_at(events, _queue_size, SIMULATION_DURATION)}"
                text += f"\n\nAverage time in queue = {average_time_in_queue(events):.4f} $t.u.$"
                text += f"\nMaximum time in queue = {maximum_waiting_time_in_queue(events):.4f} $t.u.$"

                ax2.text(x=0.1, y=0.5, s=text, fontsize=12, va="center", ha="left")

                plt.tight_layout()
                pdf.savefig()
                plt.close()


if __name__ == "__main__":
    main()
