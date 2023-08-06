from typing import overload
from typing import List
from .xyz.wagyourtail.jsmacros.client.config.Sorting_MacroSortMethod import *


class Sorting_MacroSortMethod:
	Enabled: "Sorting_MacroSortMethod"
	TriggerName: "Sorting_MacroSortMethod"
	FileName: "Sorting_MacroSortMethod"

	@overload
	def values(self) -> List["Sorting_MacroSortMethod"]:
		pass

	@overload
	def valueOf(self, name: str) -> "Sorting_MacroSortMethod":
		pass

	pass


