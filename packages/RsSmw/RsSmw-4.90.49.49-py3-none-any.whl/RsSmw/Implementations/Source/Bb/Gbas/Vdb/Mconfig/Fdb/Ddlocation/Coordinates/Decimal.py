from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Decimal:
	"""Decimal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("decimal", core, parent)

	# noinspection PyTypeChecker
	class DecimalStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Longitude: str: string Range: -0.182045 to 0.182045
			- Latitude: str: string Range: -0.091023 to 0.091023"""
		__meta_args_list = [
			ArgStruct.scalar_str('Longitude'),
			ArgStruct.scalar_str('Latitude')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Longitude: str = None
			self.Latitude: str = None

	def set(self, structure: DecimalStruct, vdbTransmitter=repcap.VdbTransmitter.Default, fdbTransmitter=repcap.FdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:DDLocation:COORdinates:DECimal \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.fdb.ddlocation.coordinates.decimal.set(value = [PROPERTY_STRUCT_NAME](), vdbTransmitter = repcap.VdbTransmitter.Default, fdbTransmitter = repcap.FdbTransmitter.Default) \n
		Defines the coordinates of the Delta DERP location in decimal format. \n
			:param structure: for set value, see the help for DecimalStruct structure arguments.
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param fdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')"""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		fdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(fdbTransmitter, repcap.FdbTransmitter)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:FDB{fdbTransmitter_cmd_val}:DDLocation:COORdinates:DECimal', structure)

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default, fdbTransmitter=repcap.FdbTransmitter.Default) -> DecimalStruct:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:DDLocation:COORdinates:DECimal \n
		Snippet: value: DecimalStruct = driver.source.bb.gbas.vdb.mconfig.fdb.ddlocation.coordinates.decimal.get(vdbTransmitter = repcap.VdbTransmitter.Default, fdbTransmitter = repcap.FdbTransmitter.Default) \n
		Defines the coordinates of the Delta DERP location in decimal format. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param fdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')
			:return: structure: for return value, see the help for DecimalStruct structure arguments."""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		fdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(fdbTransmitter, repcap.FdbTransmitter)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:FDB{fdbTransmitter_cmd_val}:DDLocation:COORdinates:DECimal?', self.__class__.DecimalStruct())
