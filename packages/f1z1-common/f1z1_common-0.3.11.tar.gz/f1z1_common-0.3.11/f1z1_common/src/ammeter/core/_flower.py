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
    MessageCounter,
    MessageTimer,
    IntOrFloat
)

Function = Callable


class AbsMessageCounter(metaclass=abc.ABCMeta):
    """
    消息流
    """

    def __init__(self,
                 callback: Function,
                 wait_time: IntOrFloat,
                 unit: UnitOfTime = UnitOfTime.MILLISECOND):
        self._message_counter = MessageCounter(0)
        self._message_timer = MessageTimer(unit, wait_time)

        check_function(callback)
        self._callback = callback

    @property
    def message_timer(self):
        """
        timer
        :return:
        """
        return self._message_timer

    @property
    def message_counter(self):
        """
        counter
        :return:
        """
        return self._message_counter

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

    def auto_increment(self, value: int) -> None:
        """
        auto increment
        :param value:
        :return:
        """
        self.message_counter.change(value)

    def restart(self) -> None:
        """
        restart
        :return:
        """
        if self._message_timer.is_timeout:
            self.message_timer.restart()
            self.message_counter.clear()

    def trigger(self) -> None:
        cb = self._callback
        if is_function(cb):
            cb(self.message_counter.get_current())


class SyncMessageCounter(AbsMessageCounter):
    """
    同步消息计流器
    """

    def tracking(self, func: Function) -> Function:
        flower = self

        @wraps(func)
        def decorating_function(*args, **kwargs):
            flower.message_timer.start()
            result = func(*args, **kwargs)
            flower.auto_increment(1)
            flower.trigger()
            flower.restart()
            return result

        return decorating_function


class AsyncMessageCounter(AbsMessageCounter):
    """
    异步消息计流器
    """

    def tracking(self, func: Function) -> Function:
        flower = self

        @wraps(func)
        async def decorating_function(*args, **kwargs):
            flower.message_timer.start()
            result = await func(*args, **kwargs)
            flower.auto_increment(1)
            flower.trigger()
            flower.restart()
            return result

        return decorating_function
