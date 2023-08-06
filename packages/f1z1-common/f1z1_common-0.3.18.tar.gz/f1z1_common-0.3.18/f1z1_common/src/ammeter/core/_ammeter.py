# @Time     : 2021/4/14
# @Project  : w8_project_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
from functools import wraps
from typing import Callable

from ...utils import UnitOfTime
from ...validator import check_function, is_function

from . import (
    Counter,
    Timer,
    IntOrFloat
)

Function = Callable


class AbstractMessageCounter(metaclass=abc.ABCMeta):
    """
    消息流
    """

    def __init__(self,
                 callback: Function,
                 wait_time: IntOrFloat,
                 time_unit: UnitOfTime = UnitOfTime.MILLISECOND):
        self._counter = Counter(0)
        self._timer = Timer(time_unit, wait_time)

        check_function(callback)
        self._callback = callback

    @property
    def callback(self) -> Function:
        """
        timeout callback
        :return:
        """
        return self._callback

    @abc.abstractmethod
    def tracking(self, func: Function) -> Function:
        raise NotImplementedError()

    @property
    def is_timeout(self):
        return self._timer.is_timeout

    def auto_increment(self, value: int) -> None:
        """
        auto increment
        :param value:
        :return:
        """
        self._counter.increment(value)

    def start(self) -> None:
        self._timer.start()

    def restart(self) -> None:
        """
        restart
        :return:
        """
        self._timer.restart()
        self._counter.clear()

    def trigger(self) -> None:
        cb = self._callback
        if is_function(cb):
            cb(self._counter.count())


class MessageCounter(AbstractMessageCounter):
    """
    同步消息计流器
    """

    def __init__(self,
                 callback: Function,
                 wait_time: IntOrFloat,
                 time_unit: UnitOfTime = UnitOfTime.MILLISECOND):
        super().__init__(callback, wait_time, time_unit)

    def tracking(self, func: Function) -> Function:
        """
        sync tracking
        :param func:
        :return:
        """
        flower = self

        @wraps(func)
        def decorate(*args, **kwargs):
            flower.start()
            flower.auto_increment(1)
            result = func(*args, **kwargs)
            if flower.is_timeout:
                flower.trigger()
                flower.restart()
            return result

        return decorate


class AsyncMessageCounter(AbstractMessageCounter):
    """
    异步消息计流器
    """

    def __init__(self,
                 callback: Function,
                 wait_time: IntOrFloat,
                 time_unit: UnitOfTime = UnitOfTime.MILLISECOND):
        super().__init__(callback, wait_time, time_unit)

    def tracking(self, func: Function) -> Function:
        """
        异步 tracking
        :param func:
        :return:
        """
        counter = self

        @wraps(func)
        async def async_decorate(*args, **kwargs):
            counter.start()
            # counter.auto_increment(1)
            result = await func(*args, **kwargs)
            counter.auto_increment(1)
            if counter.is_timeout:
                counter.trigger()
                counter.restart()
            return result

        return async_decorate
