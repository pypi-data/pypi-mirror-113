from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.ItemStackHelper import *

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class EventArmorChange(BaseEvent):
	slot: str
	item: ItemStackHelper
	oldItem: ItemStackHelper

	@overload
	def __init__(self, slot: str, item: ItemStack, old: ItemStack) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


