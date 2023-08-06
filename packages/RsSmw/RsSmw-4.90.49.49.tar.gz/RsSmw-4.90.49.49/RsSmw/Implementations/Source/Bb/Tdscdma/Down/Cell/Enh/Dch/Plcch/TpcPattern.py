from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpcPattern:
	"""TpcPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpcPattern", core, parent)

	# noinspection PyTypeChecker
	class TpcPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Tpc_Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 21"""
		__meta_args_list = [
			ArgStruct('Tpc_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tpc_Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: TpcPatternStruct, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:TPCPattern \n
		Snippet: driver.source.bb.tdscdma.down.cell.enh.dch.plcch.tpcPattern.set(value = [PROPERTY_STRUCT_NAME](), cell = repcap.Cell.Default) \n
		Sets the TPC pattern and the pattern length. \n
			:param structure: for set value, see the help for TpcPatternStruct structure arguments.
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		cell_cmd_val = self._base.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:PLCCh:TPCPattern', structure)

	def get(self, cell=repcap.Cell.Default) -> TpcPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:PLCCh:TPCPattern \n
		Snippet: value: TpcPatternStruct = driver.source.bb.tdscdma.down.cell.enh.dch.plcch.tpcPattern.get(cell = repcap.Cell.Default) \n
		Sets the TPC pattern and the pattern length. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for TpcPatternStruct structure arguments."""
		cell_cmd_val = self._base.get_repcap_cmd_value(cell, repcap.Cell)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:DCH:PLCCh:TPCPattern?', self.__class__.TpcPatternStruct())
