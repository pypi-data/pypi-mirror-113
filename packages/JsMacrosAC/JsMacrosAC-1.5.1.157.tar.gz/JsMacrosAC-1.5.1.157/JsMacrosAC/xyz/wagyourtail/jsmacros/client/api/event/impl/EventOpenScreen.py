from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.sharedinterfaces.IScreen import *

Screen = TypeVar["net.minecraft.client.gui.screen.Screen"]

class EventOpenScreen(BaseEvent):
	screen: IScreen
	screenName: str

	@overload
	def __init__(self, screen: Screen) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


