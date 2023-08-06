from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnPattern:
	"""AnPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("anPattern", core, parent)

	# noinspection PyTypeChecker
	class AnPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- An_Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 36"""
		__meta_args_list = [
			ArgStruct('An_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.An_Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: AnPatternStruct, cell=repcap.Cell.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:ANPattern \n
		Snippet: driver.source.bb.tdscdma.up.cell.enh.dch.hsich.anPattern.set(value = [PROPERTY_STRUCT_NAME](), cell = repcap.Cell.Default) \n
		Sets the ACK/NACK Pattern and the maximum pattern length. A '1' corresponds to ACK, a '0' to NAK. \n
			:param structure: for set value, see the help for AnPatternStruct structure arguments.
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		cell_cmd_val = self._base.get_repcap_cmd_value(cell, repcap.Cell)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:HSICh:ANPattern', structure)

	def get(self, cell=repcap.Cell.Default) -> AnPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:ENH:DCH:HSICh:ANPattern \n
		Snippet: value: AnPatternStruct = driver.source.bb.tdscdma.up.cell.enh.dch.hsich.anPattern.get(cell = repcap.Cell.Default) \n
		Sets the ACK/NACK Pattern and the maximum pattern length. A '1' corresponds to ACK, a '0' to NAK. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for AnPatternStruct structure arguments."""
		cell_cmd_val = self._base.get_repcap_cmd_value(cell, repcap.Cell)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{cell_cmd_val}:ENH:DCH:HSICh:ANPattern?', self.__class__.AnPatternStruct())
