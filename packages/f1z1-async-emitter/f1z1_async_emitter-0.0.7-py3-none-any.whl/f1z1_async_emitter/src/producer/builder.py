# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import CoroOrFunction, UnitOfTime, is_validators, ArgsTypes, KwargsTypes

from ..components import CountGenerator, Speed, EmitRecorder, EmitTaskQueue, SpeedTypes, SpeedUnit, Size
from .worker import EmitWorker


class IWorkerBuilder(object):

    def set_count(self, count: int) -> ["IWorkerBuilder"]:
        raise NotImplementedError()

    def set_speed(self, speed: SpeedTypes) -> ["IWorkerBuilder"]:
        raise NotImplementedError()

    def set_time_unit(self, time_unit: UnitOfTime) -> ["IWorkerBuilder"]:
        raise NotImplementedError()

    def set_thread_workers(self, workers: int) -> ["IWorkerBuilder"]:
        raise NotImplementedError()

    def build(self) -> EmitWorker:
        raise NotImplementedError("NotImplemented .build() -> T")


class EmitWorkerBuilder(IWorkerBuilder):
    """
    worker builder
    """

    def __init__(self, target: CoroOrFunction, args: ArgsTypes = None, kwargs: KwargsTypes = None):

        self._target = target
        self._args = () if not args else args
        self._kwargs = {} if not kwargs else kwargs

        """ 辅助变量 """
        self._count: int = 1  # run count
        self._speed: SpeedTypes = 100  # speed
        self._time_unit: SpeedUnit = UnitOfTime.MILLISECOND  # speed unit
        self._thread_workers: Size = None

    def set_count(self, count) -> ["EmitWorkerBuilder"]:
        self._check_int(count)
        self._count = abs(count)
        return self

    def set_speed(self, speed) -> ["EmitWorkerBuilder"]:
        self._check_speed(speed)
        self._speed = abs(speed)
        return self

    def set_time_unit(self, time_unit) -> ["EmitWorkerBuilder"]:
        self._check_unit(time_unit)
        self._time_unit = time_unit

    def set_thread_workers(self, workers) -> ["EmitWorkerBuilder"]:
        self._check_int(workers)
        self._thread_workers = abs(workers)
        return self

    def build(self) -> EmitWorker:
        count = self._count
        counter = self._create_count_generator(count)
        tasks = self._create_task_queue(count)
        recoder = self._create_recorder()
        return self._create_worker(counter, tasks, recoder)

    def _create_worker(self, counter, tasks, recorder):
        return EmitWorker(
            self._target,
            counter=counter,
            tasks=tasks,
            recorder=recorder,
            args=self._args,
            kwargs=self._kwargs,
            thread_workers=self._thread_workers
        )

    def _create_recorder(self):
        return EmitRecorder()

    def _create_task_queue(self, count: int):
        return EmitTaskQueue(count)

    def _create_count_generator(self, count: int):
        speed = Speed(self._speed, self._time_unit)
        return CountGenerator(speed, count)

    def _check_int(self, value):
        if not is_validators.is_int(value):
            raise ValueError(
                f"worker need int, but got {type(value).__name__}"
            )

    def _check_unit(self, value):
        if not is_validators.is_enum(value):
            raise ValueError(
                f"unit need Enum, but got {type(value).__name__}"
            )

    def _check_speed(self, value):
        if not is_validators.is_number(value):
            raise ValueError(
                f"speed need int or float, but got {type(value).__name__}"
            )
