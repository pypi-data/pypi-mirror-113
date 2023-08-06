from typing import overload
from .xyz.wagyourtail.jsmacros.client.access.ILoomScreen import *


class MixinLoomScreen(ILoomScreen):

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def jsmacros_canApplyDyePattern(self) -> bool:
		pass

	pass


