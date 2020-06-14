import time


class Timer:
    def __init__(self, batch_idx):
        self.__start_time__ = None
        self.__batch_idx = batch_idx

    def __enter__(self):
        self.__start_time__ = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.perf_counter() - self.__start_time__
        print("Took Time {:.2f}s for batch index {}".format(elapsed_time, self.__batch_idx))
