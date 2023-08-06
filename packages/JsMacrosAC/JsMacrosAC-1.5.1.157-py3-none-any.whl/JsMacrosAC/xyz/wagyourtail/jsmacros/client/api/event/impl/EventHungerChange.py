from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventHungerChange(BaseEvent):
	foodLevel: int

	@overload
	def __init__(self, foodLevel: int) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


