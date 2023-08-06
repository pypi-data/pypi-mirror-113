from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.ItemStackHelper import *

ItemStack = TypeVar["net.minecraft.item.ItemStack"]

class EventHeldItemChange(BaseEvent):
	offHand: bool
	item: ItemStackHelper
	oldItem: ItemStackHelper

	@overload
	def __init__(self, item: ItemStack, oldItem: ItemStack, offHand: bool) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


