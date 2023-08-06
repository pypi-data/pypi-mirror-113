from typing import overload
from .xyz.wagyourtail.jsmacros.core.config.BaseProfile import *


class BaseEvent:
	profile: BaseProfile

	@overload
	def getEventName(self) -> str:
		pass

	pass


