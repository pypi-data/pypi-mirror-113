from typing import overload
from .xyz.wagyourtail.jsmacros.core.library.BaseLibrary import *


class FTime(BaseLibrary):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def time(self) -> float:
		pass

	@overload
	def sleep(self, millis: float) -> None:
		pass

	pass


