from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH0>:PATTern \n
		Snippet: driver.source.bb.eutra.downlink.mbsfn.pmch.pattern.set(value = [PROPERTY_STRUCT_NAME](), indexNull = repcap.IndexNull.Default) \n
		Sets the pattern of the data source for the selected PMCH/MTCH. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pmch')"""
		indexNull_cmd_val = self._base.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{indexNull_cmd_val}:PATTern', structure)

	def get(self, indexNull=repcap.IndexNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH0>:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.eutra.downlink.mbsfn.pmch.pattern.get(indexNull = repcap.IndexNull.Default) \n
		Sets the pattern of the data source for the selected PMCH/MTCH. \n
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Pmch')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		indexNull_cmd_val = self._base.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{indexNull_cmd_val}:PATTern?', self.__class__.PatternStruct())
