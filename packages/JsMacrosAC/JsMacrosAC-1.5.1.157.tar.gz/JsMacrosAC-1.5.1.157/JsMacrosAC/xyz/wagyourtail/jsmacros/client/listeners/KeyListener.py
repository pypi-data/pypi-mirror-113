from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.BaseListener import *
from .xyz.wagyourtail.jsmacros.core.config.ScriptTrigger import *
from .xyz.wagyourtail.jsmacros.core.Core import *
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.core.language.ContextContainer import *


class KeyListener(BaseListener):

	@overload
	def __init__(self, macro: ScriptTrigger, runner: Core) -> None:
		pass

	@overload
	def trigger(self, event: BaseEvent) -> ContextContainer:
		pass

	pass


