from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.screens.BaseScreen import *
from .xyz.wagyourtail.jsmacros.client.api.sharedinterfaces.IScreen import *
from .xyz.wagyourtail.jsmacros.core.MethodWrapper import *

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]

class ScriptScreen(BaseScreen):

	@overload
	def __init__(self, title: str, dirt: bool) -> None:
		pass

	@overload
	def setParent(self, parent: IScreen) -> None:
		pass

	@overload
	def setOnRender(self, onRender: MethodWrapper) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	@overload
	def onClose(self) -> None:
		pass

	pass


