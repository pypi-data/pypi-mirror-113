from typing import overload
from .xyz.wagyourtail.jsmacros.core.language.BaseWrappedException_SourceLocation import *


class BaseWrappedException_HostLocation(BaseWrappedException_SourceLocation):
	location: str

	@overload
	def __init__(self, location: str) -> None:
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


