from typing import overload
from .xyz.wagyourtail.jsmacros.core.event.IEventListener import *
from .xyz.wagyourtail.jsmacros.core.config.ScriptTrigger import *
from .xyz.wagyourtail.jsmacros.core.Core import *
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.core.language.ContextContainer import *


class BaseListener(IEventListener):

	@overload
	def __init__(self, trigger: ScriptTrigger, runner: Core) -> None:
		pass

	@overload
	def getRawTrigger(self) -> ScriptTrigger:
		pass

	@overload
	def runScript(self, event: BaseEvent) -> ContextContainer:
		pass

	@overload
	def equals(self, o: object) -> bool:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


