from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.core.language.BaseWrappedException_SourceLocation import *
from .xyz.wagyourtail.jsmacros.core.language.BaseWrappedException import *

T = TypeVar["T"]
StackTraceElement = TypeVar["java.lang.StackTraceElement"]

class BaseWrappedException:
	stackFrame: T
	location: BaseWrappedException_SourceLocation
	message: str
	next: "BaseWrappedException"

	@overload
	def __init__(self, exception: T, message: str, location: BaseWrappedException_SourceLocation, next: "BaseWrappedException") -> None:
		pass

	@overload
	def wrapHostElement(self, t: StackTraceElement, next: "BaseWrappedException") -> "BaseWrappedException":
		pass

	pass


