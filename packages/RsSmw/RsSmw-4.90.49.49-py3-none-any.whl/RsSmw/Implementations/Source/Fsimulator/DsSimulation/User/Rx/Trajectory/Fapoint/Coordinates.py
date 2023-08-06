from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coordinates:
	"""Coordinates commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coordinates", core, parent)

	# noinspection PyTypeChecker
	class DmsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Longitude_Deg: int: No parameter help available
			- Longitude_Min: int: No parameter help available
			- Longitude_Sec: int: No parameter help available
			- Longitude_Dir: str: No parameter help available
			- Latitude_Deg: int: No parameter help available
			- Latitude_Min: int: No parameter help available
			- Latitude_Sec: int: No parameter help available
			- Latitude_Dir: str: No parameter help available
			- Altitude: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Longitude_Deg'),
			ArgStruct.scalar_int('Longitude_Min'),
			ArgStruct.scalar_int('Longitude_Sec'),
			ArgStruct.scalar_str('Longitude_Dir'),
			ArgStruct.scalar_int('Latitude_Deg'),
			ArgStruct.scalar_int('Latitude_Min'),
			ArgStruct.scalar_int('Latitude_Sec'),
			ArgStruct.scalar_str('Latitude_Dir'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude_Deg: int = None
			self.Longitude_Min: int = None
			self.Longitude_Sec: int = None
			self.Longitude_Dir: str = None
			self.Latitude_Deg: int = None
			self.Latitude_Min: int = None
			self.Latitude_Sec: int = None
			self.Latitude_Dir: str = None
			self.Altitude: float = None

	def get_dms(self) -> DmsStruct:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DMS \n
		Snippet: value: DmsStruct = driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.get_dms() \n
		No command help available \n
			:return: structure: for return value, see the help for DmsStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DMS?', self.__class__.DmsStruct())

	def set_dms(self, value: DmsStruct) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DMS \n
		Snippet: driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.set_dms(value = DmsStruct()) \n
		No command help available \n
			:param value: see the help for DmsStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DMS', value)

	# noinspection PyTypeChecker
	class XyzStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Xcoor: float: No parameter help available
			- Ycoor: float: No parameter help available
			- Altitude: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Xcoor'),
			ArgStruct.scalar_float('Ycoor'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Xcoor: float = None
			self.Ycoor: float = None
			self.Altitude: float = None

	def get_xyz(self) -> XyzStruct:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:XYZ \n
		Snippet: value: XyzStruct = driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.get_xyz() \n
		No command help available \n
			:return: structure: for return value, see the help for XyzStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:XYZ?', self.__class__.XyzStruct())

	def set_xyz(self, value: XyzStruct) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:XYZ \n
		Snippet: driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.set_xyz(value = XyzStruct()) \n
		No command help available \n
			:param value: see the help for XyzStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:XYZ', value)

	# noinspection PyTypeChecker
	class DecimalStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Longitude: float: No parameter help available
			- Latitude: float: No parameter help available
			- Altitude: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def get_decimal(self) -> DecimalStruct:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:[DECimal] \n
		Snippet: value: DecimalStruct = driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.get_decimal() \n
		No command help available \n
			:return: structure: for return value, see the help for DecimalStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DECimal?', self.__class__.DecimalStruct())

	def set_decimal(self, value: DecimalStruct) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:[DECimal] \n
		Snippet: driver.source.fsimulator.dsSimulation.user.rx.trajectory.fapoint.coordinates.set_decimal(value = DecimalStruct()) \n
		No command help available \n
			:param value: see the help for DecimalStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:FAPoint:COORdinates:DECimal', value)
