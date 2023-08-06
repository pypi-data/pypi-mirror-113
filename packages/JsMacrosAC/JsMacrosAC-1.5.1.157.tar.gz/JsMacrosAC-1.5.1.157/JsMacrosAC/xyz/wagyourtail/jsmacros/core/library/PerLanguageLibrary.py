from typing import overload
from .xyz.wagyourtail.jsmacros.core.library.BaseLibrary import *


class PerLanguageLibrary(BaseLibrary):

	@overload
	def __init__(self, language: Class) -> None:
		pass

	pass


