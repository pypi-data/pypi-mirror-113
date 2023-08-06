from typing import overload
from typing import List
from .xyz.wagyourtail.jsmacros.client.gui.containers.IContainerParent import *


class ICategoryTreeParent(IContainerParent):

	@overload
	def selectCategory(self, category: List[str]) -> None:
		pass

	pass


