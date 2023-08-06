# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import sleep
from collections.abc import Awaitable
from functools import lru_cache
from typing import Optional, Union

from f1z1_common import UnitOfTime, timeunit

from .base import IAwaitSpeed

SpeedTypes = Union[int, float]
SpeedUnit = Optional[UnitOfTime]


class Speed(Awaitable, IAwaitSpeed):
    """
    speed module
    """

    def __init__(self, speed: SpeedTypes, unit: SpeedUnit = UnitOfTime.MICROSECOND):
        self._speed = speed
        self._unit = unit

    def __await__(self):
        return self._await_speed(self.computed_speed_use_lru()).__await__()

    async def _await_speed(self, speed: SpeedTypes):
        return await sleep(speed)

    @lru_cache()
    def computed_speed_use_lru(self):
        return self._speed / timeunit(self._unit)

    def __str__(self):
        return f"{self.__class__.__name__}(speed={self.computed_speed_use_lru()})"
