from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.event.IEventListener import *
from .xyz.wagyourtail.jsmacros.core.MethodWrapper import *

Thread = TypeVar["java.lang.Thread"]

class FJsMacros_ScriptEventListener(IEventListener):

	@overload
	def getCreator(self) -> Thread:
		pass

	@overload
	def getWrapper(self) -> MethodWrapper:
		pass

	pass


