from typing import overload
from typing import List
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.settings.settingcontainer.AbstractMapSettingContainer_MapSettingEntry import *
from .xyz.wagyourtail.jsmacros.client.gui.settings.settingcontainer.ProfileSetting import *
from .xyz.wagyourtail.jsmacros.core.config.ScriptTrigger import *

List = TypeVar["java.util.List_xyz.wagyourtail.jsmacros.core.config.ScriptTrigger_"]
TextRenderer = TypeVar["net.minecraft.client.font.TextRenderer"]

class ProfileSetting_ProfileEntry(AbstractMapSettingContainer_MapSettingEntry):

	@overload
	def __init__(self, x: int, y: int, width: int, textRenderer: TextRenderer, parent: ProfileSetting, key: str, value: List[ScriptTrigger]) -> None:
		pass

	@overload
	def init(self) -> None:
		pass

	pass


