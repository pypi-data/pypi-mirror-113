from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.PlayerListEntryHelper import *

PlayerListEntry = TypeVar["net.minecraft.client.network.PlayerListEntry"]
UUID = TypeVar["java.util.UUID"]

class EventPlayerLeave(BaseEvent):
	UUID: str
	player: PlayerListEntryHelper

	@overload
	def __init__(self, uuid: UUID, player: PlayerListEntry) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


