# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from multiprocessing import cpu_count
from typing import Union

from f1z1_common import is_validators, UnitOfTime
from f1z1_async_runner import create_runner, start

from ..components import (
    EmitBufferQueue,
    EmitTaskQueue,
    EmitTaskSet,
    EmitRecorderChain,
    Speed,
    SpeedTypes,
    SpeedUnit,
    Size
)
from .base import IWorker, IWorkerGroup, IFactory
from .worker_group import EmitWorkerGroup
from .worker_master import EmitWorkerMaster


class EmitWorkerGroupFactory(IFactory):
    """
    worker group factory
    """

    @classmethod
    def create(cls,
               speed: SpeedTypes, *,
               speed_unit: SpeedUnit = UnitOfTime.MICROSECOND,
               maxsize: Size = None) -> EmitWorkerGroup:
        maxsize_ = cls._maxsize(maxsize)
        return EmitWorkerGroup(
            EmitBufferQueue(Speed(speed, speed_unit), maxsize_),
            EmitTaskQueue(maxsize_),
            EmitRecorderChain()
        )

    @classmethod
    def _maxsize(cls, maxsize: Size = None):
        return 2 ** 31 if is_validators.is_none(maxsize) else abs(maxsize)


class EmitWorkerMasterFactory(IFactory):
    """
    worker master factory
    """

    @classmethod
    def create(cls, maxsize: Size = None) -> EmitWorkerMaster:
        maxsize_ = cls._maxsize_with_cpu(maxsize)
        return EmitWorkerMaster(
            EmitTaskSet(maxsize_),
            EmitRecorderChain()
        )

    @classmethod
    def _maxsize_with_cpu(cls, cpu: Size = None):
        min_cpu = cpu_count()
        if not is_validators.is_int(cpu):
            return min_cpu
        return min(abs(cpu), min_cpu)


def is_worker(value):
    return isinstance(value, IWorker)


def is_group(value):
    return isinstance(value, IWorkerGroup)


def run(worker_or_group: Union[IWorker, IWorkerGroup]):
    if all([not is_worker(worker_or_group), not is_group(worker_or_group)]):
        raise ValueError(
            f"worker_or_group need IWorker or IWorkerGroup, but got {type(worker_or_group).__name__}"
        )
    runner = create_runner(worker_or_group.start())
    return start(runner)
