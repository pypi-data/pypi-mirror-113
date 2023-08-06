from typing import overload
from typing import List
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.settings.settingcontainer.AbstractMapSettingContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.SettingsOverlay import *

TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class FileMapSetting(AbstractMapSettingContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: SettingsOverlay, group: List[str]) -> None:
		pass

	@overload
	def addField(self, key: str, value: str) -> None:
		pass

	pass


