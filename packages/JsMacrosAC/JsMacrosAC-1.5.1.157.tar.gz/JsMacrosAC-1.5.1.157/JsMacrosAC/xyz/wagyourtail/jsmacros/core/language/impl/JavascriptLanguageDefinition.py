from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.language.BaseLanguage import *
from .xyz.wagyourtail.jsmacros.core.Core import *
from .xyz.wagyourtail.jsmacros.core.language.BaseWrappedException import *
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.core.language.impl.JSScriptContext import *

Throwable = TypeVar["java.lang.Throwable"]

class JavascriptLanguageDefinition(BaseLanguage):

	@overload
	def __init__(self, extension: str, runner: Core) -> None:
		pass

	@overload
	def wrapException(self, ex: Throwable) -> BaseWrappedException:
		pass

	@overload
	def createContext(self, event: BaseEvent) -> JSScriptContext:
		pass

	pass


