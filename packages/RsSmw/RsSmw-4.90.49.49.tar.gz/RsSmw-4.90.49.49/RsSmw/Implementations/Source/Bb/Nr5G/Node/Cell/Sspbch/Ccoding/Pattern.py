from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 64 bits
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, cellNull=repcap.CellNull.Nr0, ssPbchNull=repcap.SsPbchNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH0>:SSPBch<ST0>:CCODing:PATTern \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.ccoding.pattern.set(value = [PROPERTY_STRUCT_NAME](), cellNull = repcap.CellNull.Nr0, ssPbchNull = repcap.SsPbchNull.Default) \n
		Sets a bit pattern as a data source. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param cellNull: optional repeated capability selector. Default value: Nr0
			:param ssPbchNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')"""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		ssPbchNull_cmd_val = self._base.get_repcap_cmd_value(ssPbchNull, repcap.SsPbchNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{ssPbchNull_cmd_val}:CCODing:PATTern', structure)

	def get(self, cellNull=repcap.CellNull.Nr0, ssPbchNull=repcap.SsPbchNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CH0>:SSPBch<ST0>:CCODing:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.node.cell.sspbch.ccoding.pattern.get(cellNull = repcap.CellNull.Nr0, ssPbchNull = repcap.SsPbchNull.Default) \n
		Sets a bit pattern as a data source. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0
			:param ssPbchNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		ssPbchNull_cmd_val = self._base.get_repcap_cmd_value(ssPbchNull, repcap.SsPbchNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{ssPbchNull_cmd_val}:CCODing:PATTern?', self.__class__.PatternStruct())
