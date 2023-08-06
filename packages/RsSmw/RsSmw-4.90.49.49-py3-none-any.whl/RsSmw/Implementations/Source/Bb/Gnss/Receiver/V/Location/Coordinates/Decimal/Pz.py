from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pz:
	"""Pz commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pz", core, parent)

	# noinspection PyTypeChecker
	class PzStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude: float: float Range: -180 to 180
			- Latitude: float: float Range: -90 to 90
			- Altitude: float: float Defines the altitude. The altitude value is the height above the reference ellipsoid. Range: -10E3 to 50E6"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude'),
			ArgStruct.scalar_float('Altitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None
			self.Altitude: float = None

	def set(self, structure: PzStruct, vehicle=repcap.Vehicle.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:DECimal:PZ \n
		Snippet: driver.source.bb.gnss.receiver.v.location.coordinates.decimal.pz.set(value = [PROPERTY_STRUCT_NAME](), vehicle = repcap.Vehicle.Default) \n
		Defines the coordinates of the geographic location of the GNSS receiver in decimal format. \n
			:param structure: for set value, see the help for PzStruct structure arguments.
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:COORdinates:DECimal:PZ', structure)

	def get(self, vehicle=repcap.Vehicle.Default) -> PzStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:COORdinates:DECimal:PZ \n
		Snippet: value: PzStruct = driver.source.bb.gnss.receiver.v.location.coordinates.decimal.pz.get(vehicle = repcap.Vehicle.Default) \n
		Defines the coordinates of the geographic location of the GNSS receiver in decimal format. \n
			:param vehicle: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: structure: for return value, see the help for PzStruct structure arguments."""
		vehicle_cmd_val = self._base.get_repcap_cmd_value(vehicle, repcap.Vehicle)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{vehicle_cmd_val}:LOCation:COORdinates:DECimal:PZ?', self.__class__.PzStruct())
