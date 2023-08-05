import concurrent.futures
from typing import Callable, Dict, List, Union

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from pandas.io.parsers import TextFileReader

from .array import _DEFAULT_N_WORKERS_, ParallelTask, parallelize
from .code import LabelCoder


def _dataframe_slice_(dataframe: DataFrame, start: int, stop: int):
    return dataframe.iloc[start:stop]


def _dataframe_accummulate_(dataframes: List[DataFrame]):
    return pd.concat(list(dataframes))


class ParallelDataFrameTask(ParallelTask):
    def __call__(self, dataframe: DataFrame):
        return dataframe.apply(self.func, *self.args, **self.kwargs)


def apply(
        dataframe: DataFrame, func: Callable, *args,
        chunksize: int = None, executor: concurrent.futures.Executor = None,
        n_workers=_DEFAULT_N_WORKERS_, use_process=False,
        **kwargs):

    dataframe = parallelize(
        dataframe, ParallelDataFrameTask(func, args, kwargs),
        executor=executor, n_workers=n_workers, use_process=use_process,
        chunksize=chunksize, slice=_dataframe_slice_,
        accumulate=_dataframe_accummulate_
    )

    return dataframe


class ParallelDataFrameGroupByTask(ParallelTask):
    def __call__(self, dataframe_list: List[DataFrame]):
        results = []
        for dataframe in dataframe_list:
            results.append(dataframe.apply(self.func, *self.args, **self.kwargs))

        return pd.concat(results)


def groupby_apply(
        groups: DataFrameGroupBy, func: Callable, *args,
        chunksize: int = None, executor: concurrent.futures.Executor = None,
        n_workers=_DEFAULT_N_WORKERS_, use_process=False,
        **kwargs):

    dataframe_list = [df for _, df in groups]

    dataframe = parallelize(
        dataframe_list, ParallelDataFrameGroupByTask(func, args, kwargs),
        executor=executor, n_workers=n_workers, use_process=use_process,
        chunksize=chunksize, accumulate=_dataframe_accummulate_
    )

    return dataframe


def encode_dataframe(dataframe: DataFrame, columns: Union[List[str], Dict[str, LabelCoder]]):
    if not isinstance(columns, dict):
        columns = {cname: LabelCoder() for cname in columns}

    dataframe = dataframe.assign(**{
        cname: encoder.encode(dataframe[cname].values) for cname, encoder in columns.items()
    })

    return dataframe, columns


def decode_dataframe(dataframe: DataFrame, columns: Dict[str, LabelCoder]):
    dataframe = dataframe.assign(**{
        cname: encoder.decode(dataframe[cname].values) for cname, encoder in columns.items()
    })

    return dataframe


def read_csv_and_encode(filepath, encode_columns: Union[List[str], Dict[str, LabelCoder]], chunksize: int = None, **kargs):
    if chunksize is None:
        dataframe = pd.read_csv(filepath, **kargs)
        dataframe, encode_columns = encode_dataframe(dataframe, encode_columns)
        return dataframe, encode_columns

    dataframe_chunks = []
    with pd.read_csv(filepath, iterator=True, chunksize=chunksize, ** kargs) as reader:
        reader: TextFileReader
        for dataframe in reader:
            dataframe, encode_columns = encode_dataframe(dataframe, encode_columns)
            dataframe_chunks.append(dataframe)

    ignore_index = ('index_col' not in kargs) or (not kargs['index_col'])
    dataframe: DataFrame = pd.concat(dataframe_chunks, ignore_index=ignore_index)
    return dataframe, encode_columns


def decode_and_write_csv(filepath, dataframe: DataFrame, encode_columns: Dict[str, LabelCoder], chunksize: int = None, **kargs):
    if chunksize is None:
        chunksize = len(dataframe)

    dataframe_list = np.array_split(dataframe, range(chunksize, len(dataframe), chunksize))
    dataframe = decode_dataframe(dataframe_list[0], encode_columns)
    dataframe.to_csv(filepath, **kargs)

    for dataframe in dataframe_list[1:]:
        dataframe = decode_dataframe(dataframe, encode_columns)
        dataframe.to_csv(filepath, header=False, mode='a', **kargs)
