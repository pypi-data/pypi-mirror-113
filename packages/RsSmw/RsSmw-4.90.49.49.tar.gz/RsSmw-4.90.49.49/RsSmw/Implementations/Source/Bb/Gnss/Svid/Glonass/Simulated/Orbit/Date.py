from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Date:
	"""Date commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("date", core, parent)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Year: int: integer Range: 1996 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def set(self, structure: DateStruct, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIMulated:ORBit:DATE \n
		Snippet: driver.source.bb.gnss.svid.glonass.simulated.orbit.date.set(value = [PROPERTY_STRUCT_NAME](), satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the reference date. \n
			:param structure: for set value, see the help for DateStruct structure arguments.
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')"""
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIMulated:ORBit:DATE', structure)

	def get(self, satelliteSvid=repcap.SatelliteSvid.Default) -> DateStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass:SIMulated:ORBit:DATE \n
		Snippet: value: DateStruct = driver.source.bb.gnss.svid.glonass.simulated.orbit.date.get(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Sets the reference date. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: structure: for return value, see the help for DateStruct structure arguments."""
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GLONass:SIMulated:ORBit:DATE?', self.__class__.DateStruct())
