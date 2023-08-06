from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventChunkLoad(BaseEvent):
	x: int
	z: int
	isFull: bool

	@overload
	def __init__(self, x: int, z: int, isFull: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


