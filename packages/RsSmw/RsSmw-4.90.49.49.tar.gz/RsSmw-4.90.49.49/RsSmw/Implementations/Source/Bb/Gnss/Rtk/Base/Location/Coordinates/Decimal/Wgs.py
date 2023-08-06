from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wgs:
	"""Wgs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wgs", core, parent)

	# noinspection PyTypeChecker
	class WgsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
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

	def set(self, structure: WgsStruct, baseSt=repcap.BaseSt.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: driver.source.bb.gnss.rtk.base.location.coordinates.decimal.wgs.set(value = [PROPERTY_STRUCT_NAME](), baseSt = repcap.BaseSt.Default) \n
		No command help available \n
			:param structure: for set value, see the help for WgsStruct structure arguments.
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')"""
		baseSt_cmd_val = self._base.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:COORdinates:DECimal:WGS', structure)

	def get(self, baseSt=repcap.BaseSt.Default) -> WgsStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:COORdinates:DECimal:[WGS] \n
		Snippet: value: WgsStruct = driver.source.bb.gnss.rtk.base.location.coordinates.decimal.wgs.get(baseSt = repcap.BaseSt.Default) \n
		No command help available \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:return: structure: for return value, see the help for WgsStruct structure arguments."""
		baseSt_cmd_val = self._base.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:COORdinates:DECimal:WGS?', self.__class__.WgsStruct())
