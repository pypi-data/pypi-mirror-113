# @Time     : 2021/4/13
# @Project  : w8_project_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import time
from typing import Union

from ...utils import TimeUnit, UnitOfTime
from .. import IMessageTimer, RunStates

_time = time.time
IntOrFloat = Union[int, float]


class MessageTimer(IMessageTimer):

    def __init__(self, unit: UnitOfTime, wait_time: IntOrFloat):
        self._state: RunStates = RunStates.UN_START  # 状态
        self._step_time: IntOrFloat = 0  # 间隔时间
        self._start_time: IntOrFloat = 0  # 开始时间

        self._time_unit: TimeUnit = TimeUnit(unit)  # 时间单位
        self._wait_time = wait_time  # 超时时间

    @property
    def is_started(self) -> bool:
        return self._state == RunStates.STARTED

    @property
    def is_timeout(self) -> bool:
        """
        is timeout
        :return:
        """
        return self._get_current_step() >= self._wait_time

    def get_current(self, **kwargs) -> IntOrFloat:
        """
        get current
        :param kwargs:
        :return:
        """
        return _time() * self._time_unit.get_time_unit()

    def start(self, **kwargs) -> None:
        if self.is_started:
            return

        # update state, start time
        self._set_state(RunStates.STARTED)
        self._set_start(self.get_current())

    def restart(self, **kwargs) -> None:
        """
        restart timer
        :return:
        """
        self._set_start(self.get_current())

    def stop(self, **kwargs) -> None:
        # update state, step time
        self._set_state(RunStates.UN_START)

    def clear(self) -> None:
        """
        clear timer
        :return:
        """
        self._set_state(RunStates.UN_START)
        self._set_start(0)

    def _set_start(self, start_time: IntOrFloat) -> None:
        self._start_time = abs(start_time)

    def _set_state(self, state: RunStates) -> None:
        self._state = state

    def _set_step(self, step: IntOrFloat) -> None:
        if step < 0:
            self._step_time = 0
        else:
            self._step_time = step

    def _get_current_step(self) -> IntOrFloat:
        """
        获取间隔时间
        :return:
        """
        return self.get_current() - self._start_time
