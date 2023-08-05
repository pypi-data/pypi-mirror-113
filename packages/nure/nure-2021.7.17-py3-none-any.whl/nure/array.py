import concurrent.futures
import itertools
import os
from typing import Callable, List, Union

_DEFAULT_N_WORKERS_ = os.cpu_count() or 4


def _slice_list_(array, start, stop):
    return array[start:stop]


def _accumulate_list_(list_array):
    return list(itertools.chain.from_iterable(list_array))


def split(array: list, size: int, slice: Callable = _slice_list_):
    # looping till length l
    for i in range(0, len(array), size):
        yield slice(array, i, i + size)


class ParallelTask:
    def __init__(self, func: Callable, args: tuple, kwargs: dict) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, payload):
        return self.func(payload, *self.args, **self.kwargs)


def parallelize(
        array: List, func: Callable, *args,
        executor: concurrent.futures.Executor = None,
        chunksize: int = None,
        n_workers: int = _DEFAULT_N_WORKERS_,
        use_process: bool = False,
        slice: Callable = _slice_list_,
        accumulate: Callable = _accumulate_list_,
        length: Union[Callable, int] = len,
        **kwargs
):
    # check if exe is provided
    if executor is None:
        if use_process:
            my_executor = concurrent.futures.ProcessPoolExecutor(max_workers=n_workers)
        else:
            my_executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_workers)
    else:
        my_executor = executor

    # split data
    if chunksize is None:
        array_size = length(array) if callable(accumulate) else length
        chunksize = max(array_size // n_workers, n_workers)

    chunks = split(array, chunksize, slice=slice)
    # wrap to obj for serializable in Process Pool
    if not issubclass(type(func), ParallelTask):
        func = ParallelTask(func, args, kwargs)

    # execute
    processed_chunks = my_executor.map(func, chunks)

    # if is my exe, then shutdown
    if executor is None:
        my_executor.shutdown()

    accumulated_array = accumulate(processed_chunks)
    return accumulated_array
