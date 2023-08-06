from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.IContainerParent import *
from .xyz.wagyourtail.jsmacros.client.gui.overlays.OverlayContainer import *

Element = TypeVar["net.minecraft.client.gui.Element"]

class IOverlayParent(IContainerParent):

	@overload
	def closeOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def setFocused(self, focused: Element) -> None:
		pass

	@overload
	def getChildOverlay(self) -> OverlayContainer:
		pass

	pass


