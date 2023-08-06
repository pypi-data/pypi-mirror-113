from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.EntityHelper import *

Entity = TypeVar["net.minecraft.entity.Entity"]

class EventEntityDamaged(BaseEvent):
	entity: EntityHelper
	damage: float

	@overload
	def __init__(self, e: Entity, amount: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


