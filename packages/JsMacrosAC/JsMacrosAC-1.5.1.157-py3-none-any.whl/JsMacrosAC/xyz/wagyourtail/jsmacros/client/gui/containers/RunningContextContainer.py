from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.MultiElementContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.screens.CancelScreen import *
from .xyz.wagyourtail.jsmacros.core.language.ScriptContext import *

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
WeakReference = TypeVar["java.lang.ref.WeakReference_xyz.wagyourtail.jsmacros.core.language.ScriptContext___"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class RunningContextContainer(MultiElementContainer):
	t: WeakReference

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: CancelScreen, t: ScriptContext) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


