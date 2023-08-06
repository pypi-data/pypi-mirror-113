from typing import overload
from .xyz.wagyourtail.jsmacros.core.library.BaseLibrary import *
from .xyz.wagyourtail.jsmacros.core.language.ContextContainer import *


class PerExecLibrary(BaseLibrary):

	@overload
	def __init__(self, context: ContextContainer) -> None:
		pass

	pass


