import numpy as np


class Server:
    def __init__(self, t_id: int, t_avgWorkTime: float):
        self.__id: int = t_id
        self.__avg_work_time = t_avgWorkTime
        self.__work_end: float = None
        self.__random_engine = np.random.default_rng(seed=1)

    def get_id(self) -> int:
        return self.__id

    def is_free(self, t_timestamp: float) -> bool:
        return self.__work_end is None or self.__work_end <= t_timestamp

    def start_work(self, t_timestamp: float) -> None:
        self.__work_end = t_timestamp + self.__random_engine.exponential(
            scale=1.0 / self.__avg_work_time
        )

    def get_work_end(self) -> float:
        return self.__work_end
