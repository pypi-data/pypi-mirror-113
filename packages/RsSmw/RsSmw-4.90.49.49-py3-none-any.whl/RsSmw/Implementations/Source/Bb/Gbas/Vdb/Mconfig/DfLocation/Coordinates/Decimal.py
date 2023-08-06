from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Decimal:
	"""Decimal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("decimal", core, parent)

	# noinspection PyTypeChecker
	class DecimalStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude: float: float Range: -1.0 to 1.0
			- Latitude: float: float Range: -1.0 to 1.0"""
		__meta_args_list = [
			ArgStruct.scalar_float('Longitude'),
			ArgStruct.scalar_float('Latitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: float = None
			self.Latitude: float = None

	def set(self, structure: DecimalStruct, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DFLocation:COORdinates:DECimal \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.dfLocation.coordinates.decimal.set(value = [PROPERTY_STRUCT_NAME](), vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Defines the coordinates of the Delta FPAD location in decimal format. \n
			:param structure: for set value, see the help for DecimalStruct structure arguments.
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DFLocation:COORdinates:DECimal', structure)

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> DecimalStruct:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DFLocation:COORdinates:DECimal \n
		Snippet: value: DecimalStruct = driver.source.bb.gbas.vdb.mconfig.dfLocation.coordinates.decimal.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Defines the coordinates of the Delta FPAD location in decimal format. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: structure: for return value, see the help for DecimalStruct structure arguments."""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DFLocation:COORdinates:DECimal?', self.__class__.DecimalStruct())
