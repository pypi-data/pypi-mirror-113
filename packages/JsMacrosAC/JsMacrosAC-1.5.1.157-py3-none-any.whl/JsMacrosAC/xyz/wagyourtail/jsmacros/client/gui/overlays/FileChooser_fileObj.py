from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.gui.elements.Button import *

File = TypeVar["java.io.File"]

class FileChooser_fileObj:
	file: File
	btn: Button

	@overload
	def __init__(self, file: File, btn: Button) -> None:
		pass

	pass


