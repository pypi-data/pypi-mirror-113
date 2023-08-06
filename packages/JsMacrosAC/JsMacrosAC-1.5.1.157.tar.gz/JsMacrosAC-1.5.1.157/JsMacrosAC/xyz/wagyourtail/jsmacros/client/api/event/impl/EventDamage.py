from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.EntityHelper import *

DamageSource = TypeVar["net.minecraft.entity.damage.DamageSource"]

class EventDamage(BaseEvent):
	attacker: EntityHelper
	source: str
	health: float
	change: float

	@overload
	def __init__(self, source: DamageSource, health: float, change: float) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


