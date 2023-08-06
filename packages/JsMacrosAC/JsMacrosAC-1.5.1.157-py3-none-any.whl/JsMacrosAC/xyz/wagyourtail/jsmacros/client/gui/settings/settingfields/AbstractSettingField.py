from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.containers.MultiElementContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.settingcontainer.AbstractSettingContainer import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.SettingsOverlay_SettingField import *

TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class AbstractSettingField(MultiElementContainer):

	@overload
	def __init__(self, x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: AbstractSettingContainer, field: SettingsOverlay_SettingField) -> None:
		pass

	pass


