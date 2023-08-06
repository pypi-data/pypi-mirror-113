from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventDimensionChange(BaseEvent):
	dimension: str

	@overload
	def __init__(self, dimension: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


