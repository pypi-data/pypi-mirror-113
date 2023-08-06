from typing import overload
from typing import TypeVar
from .xyz.wagyourtail.jsmacros.client.api.sharedclasses.PositionCommon_Pos2D import *
from .xyz.wagyourtail.jsmacros.client.api.sharedclasses.PositionCommon_Pos3D import *
from .xyz.wagyourtail.jsmacros.client.api.sharedclasses.PositionCommon_Vec3D import *

Vec3d = TypeVar["net.minecraft.util.math.Vec3d"]

class PositionCommon_Pos3D(PositionCommon_Pos2D):
	ZERO: "PositionCommon_Pos3D"
	z: float

	@overload
	def __init__(self, vec: Vec3d) -> None:
		pass

	@overload
	def __init__(self, x: float, y: float, z: float) -> None:
		pass

	@overload
	def getZ(self) -> float:
		pass

	@overload
	def add(self, pos: "PositionCommon_Pos3D") -> "PositionCommon_Pos3D":
		pass

	@overload
	def multiply(self, pos: "PositionCommon_Pos3D") -> "PositionCommon_Pos3D":
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def toVector(self) -> PositionCommon_Vec3D:
		pass

	pass


