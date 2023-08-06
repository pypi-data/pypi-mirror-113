from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.MultiElementContainer import *
from .xyz.wagyourtail.jsmacros.core.config.ScriptTrigger_TriggerType import *
from .xyz.wagyourtail.jsmacros.client.gui.screens.MacroScreen import *

MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class MacroListTopbar(MultiElementContainer):
	deftype: ScriptTrigger_TriggerType

	@overload
	def __init__(self, parent: MacroScreen, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, deftype: ScriptTrigger_TriggerType) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def updateType(self, type: ScriptTrigger_TriggerType) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


