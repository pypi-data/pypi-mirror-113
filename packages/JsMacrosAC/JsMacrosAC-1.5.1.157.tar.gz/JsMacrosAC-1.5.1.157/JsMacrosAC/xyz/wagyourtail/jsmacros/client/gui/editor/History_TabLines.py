from typing import overload
from .xyz.wagyourtail.jsmacros.client.gui.editor.History_HistoryStep import *
from .xyz.wagyourtail.jsmacros.client.gui.editor.SelectCursor import *


class History_TabLines(History_HistoryStep):

	@overload
	def __init__(self, startLine: int, lineCount: int, reversed: bool, cursor: SelectCursor) -> None:
		pass

	pass


