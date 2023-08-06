from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.overlays.OverlayContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.overlays.IOverlayParent import *

T = TypeVar["T"]
Element = TypeVar["net.minecraft.client.gui.Element"]

class IContainerParent:

	@overload
	def addDrawableChild(self, drawableElement: T) -> T:
		pass

	@overload
	def remove(self, button: Element) -> None:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer) -> None:
		pass

	@overload
	def openOverlay(self, overlay: OverlayContainer, disableButtons: bool) -> None:
		pass

	@overload
	def getFirstOverlayParent(self) -> IOverlayParent:
		pass

	pass


