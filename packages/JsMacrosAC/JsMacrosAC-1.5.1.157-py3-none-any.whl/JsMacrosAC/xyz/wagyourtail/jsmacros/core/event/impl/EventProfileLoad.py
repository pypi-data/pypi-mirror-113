from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.core.config.BaseProfile import *


class EventProfileLoad(BaseEvent):
	profileName: str

	@overload
	def __init__(self, profile: BaseProfile, profileName: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


