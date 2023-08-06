from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coordinates:
	"""Coordinates commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coordinates", core, parent)

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
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:TDF:ENU:COORdinates:[DECimal] \n
		Snippet: value: DecimalStruct = driver.source.fsimulator.dsSimulation.user.rx.trajectory.tdf.enu.coordinates.get_decimal() \n
		No command help available \n
			:return: structure: for return value, see the help for DecimalStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:TDF:ENU:COORdinates:DECimal?', self.__class__.DecimalStruct())

	def set_decimal(self, value: DecimalStruct) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:DSSimulation:USER:RX:TRAJectory:TDF:ENU:COORdinates:[DECimal] \n
		Snippet: driver.source.fsimulator.dsSimulation.user.rx.trajectory.tdf.enu.coordinates.set_decimal(value = DecimalStruct()) \n
		No command help available \n
			:param value: see the help for DecimalStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:FSIMulator:DSSimulation:USER:RX:TRAJectory:TDF:ENU:COORdinates:DECimal', value)
