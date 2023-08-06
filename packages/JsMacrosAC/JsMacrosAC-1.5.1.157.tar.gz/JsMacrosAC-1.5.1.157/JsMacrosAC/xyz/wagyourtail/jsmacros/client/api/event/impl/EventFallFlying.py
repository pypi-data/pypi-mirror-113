from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventFallFlying(BaseEvent):
	state: bool

	@overload
	def __init__(self, state: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


