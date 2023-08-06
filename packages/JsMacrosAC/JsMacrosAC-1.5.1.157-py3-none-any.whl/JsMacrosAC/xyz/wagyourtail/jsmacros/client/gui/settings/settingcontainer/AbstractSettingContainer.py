from typing import overload
from typing import List
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.MultiElementContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.elements.Scrollbar import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.SettingsOverlay import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.SettingsOverlay_SettingField import *

TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class AbstractSettingContainer(MultiElementContainer):
	group: List[str]
	scroll: Scrollbar

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addSetting(self, setting: SettingsOverlay_SettingField) -> None:
		pass

	pass


