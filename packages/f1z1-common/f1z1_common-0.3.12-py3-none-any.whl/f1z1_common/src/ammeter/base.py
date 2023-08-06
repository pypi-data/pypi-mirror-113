# @Time     : 2021/4/13
# @Project  : w8_project_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum
import typing

T = typing.TypeVar("T")


class TimeoutStates(enum.Enum):
    """
    超时状态枚举
    """
    UN_TIMEOUT = 0
    TIMEOUT = 1


class RunStates(enum.Enum):
    """
    运行状态
    """
    UN_START = 0  # 停
    STARTED = 1  # 已开始
    PAUSE = 2  # 暂停


class ITimer(object):
    """
    消息计时器
    """

    @property
    def is_timeout(self) -> bool:
        """
        is_timeout
        :return:
        """
        raise NotImplementedError()

    def current(self, **kwargs) -> T:
        """
        get current time
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def start(self, **kwargs) -> None:
        """
        start timer
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def restart(self, **kwargs) -> None:
        raise NotImplementedError()

    def stop(self, **kwargs) -> None:
        """
        stop timer
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def clear(self) -> None:
        """
        clear timeout
        :return:
        """
        raise NotImplementedError()


class ICounter(object):
    """
    消息计数器
    """

    def count(self, **kwargs) -> T:
        """
        get count
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def increment(self, value: T, **kwargs) -> None:
        """
        increment
        :param value:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def clear(self, **kwargs) -> None:
        """
        clear
        :return:
        """
        raise NotImplementedError()
