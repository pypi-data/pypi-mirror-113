from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.TextHelper import *

Text = TypeVar["net.minecraft.text.Text"]

class EventRecvMessage(BaseEvent):
	text: TextHelper

	@overload
	def __init__(self, message: Text) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


