from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Decimal:
	"""Decimal commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("decimal", core, parent)

	# noinspection PyTypeChecker
	class PzStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Longitude: float: float Range: -180 to 180
			- Latitude: float: float Range: -90 to 90
			- Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def get_pz(self) -> PzStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:PZ \n
		Snippet: value: PzStruct = driver.source.bb.gnss.adGeneration.gps.location.coordinates.decimal.get_pz() \n
		Sets the geographic reference location in decimal format. \n
			:return: structure: for return value, see the help for PzStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:PZ?', self.__class__.PzStruct())

	def set_pz(self, value: PzStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:PZ \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.location.coordinates.decimal.set_pz(value = PzStruct()) \n
		Sets the geographic reference location in decimal format. \n
			:param value: see the help for PzStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:PZ', value)

	# noinspection PyTypeChecker
	class WgsStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Longitude: float: float Range: -180 to 180
			- Latitude: float: float Range: -90 to 90
			- Altitude: float: float Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def get_wgs(self) -> WgsStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: value: WgsStruct = driver.source.bb.gnss.adGeneration.gps.location.coordinates.decimal.get_wgs() \n
		Sets the geographic reference location in decimal format. \n
			:return: structure: for return value, see the help for WgsStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:WGS?', self.__class__.WgsStruct())

	def set_wgs(self, value: WgsStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.location.coordinates.decimal.set_wgs(value = WgsStruct()) \n
		Sets the geographic reference location in decimal format. \n
			:param value: see the help for WgsStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:LOCation:COORdinates:DECimal:WGS', value)
