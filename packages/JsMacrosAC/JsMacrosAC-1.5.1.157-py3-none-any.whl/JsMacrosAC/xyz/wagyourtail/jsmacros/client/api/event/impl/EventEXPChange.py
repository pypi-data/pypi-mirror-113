from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventEXPChange(BaseEvent):
	progress: float
	total: int
	level: int

	@overload
	def __init__(self, progress: float, total: int, level: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


