from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.MultiElementContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.settingcontainer.AbstractMapSettingContainer import *

T = TypeVar["T"]
MatrixStack = TypeVar["net.minecraft.client.util.math.MatrixStack"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class AbstractMapSettingContainer_MapSettingEntry(MultiElementContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, textRenderer: TextRenderer, parent: AbstractMapSettingContainer, key: str, value: T) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	@overload
	def setPos(self, x: int, y: int, width: int, height: int) -> None:
		pass

	@overload
	def setKey(self, newKey: str) -> None:
		pass

	@overload
	def setValue(self, newValue: T) -> None:
		pass

	@overload
	def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float) -> None:
		pass

	pass


