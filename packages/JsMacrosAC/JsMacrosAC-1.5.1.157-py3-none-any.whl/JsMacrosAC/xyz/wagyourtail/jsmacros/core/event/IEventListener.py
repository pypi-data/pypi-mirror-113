from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.core.language.ContextContainer import *


class IEventListener:

	@overload
	def trigger(self, event: BaseEvent) -> ContextContainer:
		pass

	pass


