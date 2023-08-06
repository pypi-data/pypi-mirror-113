from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *


class EventJoinedTick(BaseEvent):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


