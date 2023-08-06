from typing import Any, Awaitable, Callable, Union

from eventipy import Event

EventHandler = Callable[[Event], Union[Any, Awaitable[Any]]]
