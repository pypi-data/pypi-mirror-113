# @Time     : 2021/6/3
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum

from .enums import EnumUtil

BASE = 10


class UnitOfTime(Enum):
    SECOND = BASE ** 0  # 秒
    MILLISECOND = BASE ** 3  # 毫秒
    MICROSECOND = BASE ** 6  # 微秒


class ITimeUnit(object):

    def get_time_unit(self) -> int:
        raise NotImplementedError()


class SecondUnit(ITimeUnit):

    def get_time_unit(self) -> int:
        return EnumUtil.unenum(UnitOfTime.SECOND)


class MilliSecondUnit(ITimeUnit):

    def get_time_unit(self) -> int:
        return EnumUtil.unenum(UnitOfTime.MILLISECOND)


class MicroSecondUnit(ITimeUnit):

    def get_time_unit(self) -> int:
        return EnumUtil.unenum(UnitOfTime.MICROSECOND)


class TimeUnit(ITimeUnit):

    def __init__(self, unit_of_time: UnitOfTime):
        self._unit = self._create_unit(unit_of_time)

    def get_time_unit(self) -> int:
        return self._unit.get_time_unit()

    def _create_unit(self, unit_of_time: UnitOfTime) -> ITimeUnit:
        if unit_of_time == UnitOfTime.SECOND:
            return SecondUnit()
        elif unit_of_time == UnitOfTime.MILLISECOND:
            return MilliSecondUnit()
        return MicroSecondUnit()


def timeunit(unit: UnitOfTime):
    return TimeUnit(unit).get_time_unit()


def second():
    """
    second
    :return:
    """
    return timeunit(UnitOfTime.SECOND)


def microsecond():
    """
    microsecond
    :return:
    """
    return timeunit(UnitOfTime.MICROSECOND)


def millisecond():
    """
    millisecond
    :return:
    """
    return timeunit(UnitOfTime.MILLISECOND)
