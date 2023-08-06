from typing import overload
from .xyz.wagyourtail.jsmacros.client.api.helpers.NBTElementHelper import *


class NBTElementHelper_NBTListHelper(NBTElementHelper):

	@overload
	def length(self) -> int:
		pass

	@overload
	def get(self, index: int) -> NBTElementHelper:
		pass

	@overload
	def getHeldType(self) -> int:
		pass

	pass


