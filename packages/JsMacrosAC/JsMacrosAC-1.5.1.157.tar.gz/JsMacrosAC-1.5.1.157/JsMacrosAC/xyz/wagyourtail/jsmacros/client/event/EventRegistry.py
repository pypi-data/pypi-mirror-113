from typing import overload
from typing import List
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.BaseEventRegistry import *
from .xyz.wagyourtail.jsmacros.core.Core import *
from .xyz.wagyourtail.jsmacros.core.config.ScriptTrigger import *

List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.config.ScriptTrigger_"]

class EventRegistry(BaseEventRegistry):

	@overload
	def __init__(self, runner: Core) -> None:
		pass

	@overload
	def addScriptTrigger(self, rawmacro: ScriptTrigger) -> None:
		pass

	@overload
	def removeScriptTrigger(self, rawmacro: ScriptTrigger) -> bool:
		pass

	@overload
	def getScriptTriggers(self) -> List[ScriptTrigger]:
		pass

	pass


