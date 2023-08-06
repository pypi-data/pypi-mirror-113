from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.sharedclasses.PositionCommon_Pos3D import *


class EventSound(BaseEvent):
	sound: str
	volume: float
	pitch: float
	position: PositionCommon_Pos3D

	@overload
	def __init__(self, sound: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


