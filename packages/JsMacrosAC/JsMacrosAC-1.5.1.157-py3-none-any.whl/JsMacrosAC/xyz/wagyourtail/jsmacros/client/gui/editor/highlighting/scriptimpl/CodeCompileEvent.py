from typing import overload
from typing import List
from typing import TypeVar
from typing import Any
from typing import Mapping
from .xyz.wagyourtail.jsmacros.core.event.BaseEvent import *
from .xyz.wagyourtail.jsmacros.client.gui.editor.SelectCursor import *
from .xyz.wagyourtail.jsmacros.client.gui.screens.EditorScreen import *
from .xyz.wagyourtail.jsmacros.client.api.helpers.TextHelper import *
from .xyz.wagyourtail.jsmacros.client.gui.editor.highlighting.AutoCompleteSuggestion import *
from .xyz.wagyourtail.jsmacros.core.MethodWrapper import *
from .xyz.wagyourtail.jsmacros.client.api.classes.TextBuilder import *
from .xyz.wagyourtail.StringHashTrie import *

Prism4j_Node = TypeVar["io.noties.prism4j.Prism4j.Node"]
List = TypeVar["java.util.List_io.noties.prism4j.Prism4j.Node_"]
Map = TypeVar["java.util.Map_java.lang.String,short[]_"]

class CodeCompileEvent(BaseEvent):
	cursor: SelectCursor
	code: str
	language: str
	screen: EditorScreen
	textLines: List[TextHelper]
	autoCompleteSuggestions: List[AutoCompleteSuggestion]
	rightClickActions: MethodWrapper

	@overload
	def __init__(self, code: str, language: str, screen: EditorScreen) -> None:
		pass

	@overload
	def genPrismNodes(self) -> List[Prism4j_Node]:
		pass

	@overload
	def createMap(self) -> Mapping[Any, Any]:
		pass

	@overload
	def createTextBuilder(self) -> TextBuilder:
		pass

	@overload
	def createSuggestion(self, startIndex: int, suggestion: str) -> AutoCompleteSuggestion:
		pass

	@overload
	def createSuggestion(self, startIndex: int, suggestion: str, displayText: TextHelper) -> AutoCompleteSuggestion:
		pass

	@overload
	def createPrefixTree(self) -> StringHashTrie:
		pass

	@overload
	def getThemeData(self) -> Mapping[str, List[float]]:
		pass

	pass


