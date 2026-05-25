import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator

from sources.trace import get_time_and_nodes
from sources.engine import Engine, TraceType
from sources.stats import *
from sources.constants import SERVER_LAMBDA


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
        for _client_count, _server_count, _queue_size in configuration:
            CLIENT_LAMBDAS = [4, 6, 8, 12]
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
                    t_client_avg_send_by_time_unit=_client_lambda,
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
                total_in_system = []
                _t = []
                STEP = 0.2
                _time = STEP

                while _time <= SIMULATION_DURATION:
                    _t.append(_time - STEP)

                    transmit_count.append(
                        total_messages_transmit(events, _time) - sum(transmit_count)
                    )
                    dropped_count.append(
                        total_messages_dropped(events, _queue_size, _time)
                        - sum(dropped_count)
                    )
                    still_in_transmission.append(
                        messages_still_in_transmission_at(events, _time)
                    )
                    still_in_queue.append(
                        messages_in_queue_at(events, _queue_size, _time)
                    )
                    total_in_system.append(
                        transmit_count[-1]
                        + dropped_count[-1]
                        + still_in_transmission[-1]
                        + still_in_queue[-1]
                    )
                    _time += STEP

                assert len(_t) == len(transmit_count)
                assert len(_t) == len(still_in_transmission)
                assert len(_t) == len(still_in_queue)
                assert len(_t) == len(dropped_count)

                # -----------------------------------------------------------
                # Prepare draw environment
                # -----------------------------------------------------------
                fig = plt.figure(figsize=(11.69, 8.27))
                _fontdict = {}
                _fontdict["fontweight"] = "bold"
                plt.title(f"{title}\n", fontdict=_fontdict)
                plt.axis("off")

                gs_main = gridspec.GridSpec(1, 2, figure=fig)
                gs_left = gridspec.GridSpecFromSubplotSpec(
                    2, 1, subplot_spec=gs_main[0, 0], height_ratios=[3, 1]
                )

                _left_top = fig.add_subplot(gs_left[0, 0])
                _left_bottom = fig.add_subplot(gs_left[1, 0])
                _left_bottom.axis("off")
                _right = fig.add_subplot(gs_main[0, 1])
                _right.axis("off")

                # -----------------------------------------------------------
                # Draw bar graph
                # -----------------------------------------------------------
                data_sets = [
                    np.array(still_in_transmission),
                    np.array(still_in_queue),
                    np.array(dropped_count),
                    np.array(transmit_count),
                ]

                current_bottom = np.zeros(len(_t))
                labels = ["in transmission", "in queue", "dropped", "transmit"]
                colors = ["#1f77b4", "#f1c62a", "#b4301f", "#1fb42bd3"]
                for data, label, color in zip(data_sets, labels, colors):
                    _left_top.bar(
                        _t,
                        data,
                        bottom=current_bottom,
                        label=label,
                        color=color,
                        align="edge",
                        width=STEP,
                        edgecolor="grey",
                    )
                    current_bottom += data

                div = np.ceil(max(total_in_system) / 20)
                _left_top.yaxis.set_major_locator(MultipleLocator(div))
                _left_top.grid(axis="y", linestyle="--", alpha=0.7)
                _left_top.xaxis.set_major_locator(MultipleLocator(1))

                _left_top.set_xlabel("$time$")
                _left_top.set_ylabel(
                    "Message counts during interval (in_system = in_transmission + in_queue)"
                )
                _left_top.legend()

                # -----------------------------------------------------------
                # Draw comments
                # -----------------------------------------------------------
                text = f"\nTotal message sended = {total_messages_sended(events, SIMULATION_DURATION)}"
                text += f"\nTotal message transmitted = {total_messages_transmit(events, SIMULATION_DURATION)}"
                text += f"\nTotal message dropped = {total_messages_dropped(events, _queue_size, SIMULATION_DURATION)}"
                text += f"\n\nStill in transmission at end = {messages_still_in_transmission_at(events, SIMULATION_DURATION)}"
                text += f"\nStill in queue at end = {messages_in_queue_at(events, _queue_size, SIMULATION_DURATION)}"
                text += f"\n\nAverage queue size = {mean_queue_size(events, _queue_size, SIMULATION_DURATION):.4f}"
                text += f"\nAverage requests count in system = {mean_request_in_system(events, _queue_size, SIMULATION_DURATION):.4f}"
                text += f"\n\nAverage time in queue = {average_time_in_queue(events):.4f} $t.u.$"
                text += f"\nMaximum time in queue = {maximum_waiting_time_in_queue(events):.4f} $t.u.$"

                _left_bottom.text(
                    x=0, y=0.65, s=text, fontsize=9, va="center", ha="left"
                )

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
                    if len(table_data) < (MAX_ROWS / 2 - 2) or i >= last_row_index:
                        table_data.append(all_data[i])
                    elif len(table_data) == (MAX_ROWS / 2 - 2):
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
                trace = _right.table(
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
                # Close
                # -----------------------------------------------------------
                plt.tight_layout()
                pdf.savefig()
                plt.close()


if __name__ == "__main__":
    main()
