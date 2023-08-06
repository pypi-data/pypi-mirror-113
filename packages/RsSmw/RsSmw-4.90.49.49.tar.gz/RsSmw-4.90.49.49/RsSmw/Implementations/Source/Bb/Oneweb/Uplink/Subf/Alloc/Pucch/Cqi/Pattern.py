from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


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
			- Bitcount: int: integer Range: 1 to 13"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:CQI:PATTern \n
		Snippet: driver.source.bb.oneweb.uplink.subf.alloc.pucch.cqi.pattern.set(value = [PROPERTY_STRUCT_NAME](), subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the CQI pattern for the PUCCH. The length of the pattern is determined by the number of CQI bits
		([:SOURce<hw>]:BB:ONEWeb:UL[:SUBF<st0>]:ALLoc<ch0>:PUCCh:CQI:CBITs?) . \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')"""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:ONEWeb:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:CQI:PATTern', structure)

	def get(self, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:CQI:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.oneweb.uplink.subf.alloc.pucch.cqi.pattern.get(subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the CQI pattern for the PUCCH. The length of the pattern is determined by the number of CQI bits
		([:SOURce<hw>]:BB:ONEWeb:UL[:SUBF<st0>]:ALLoc<ch0>:PUCCh:CQI:CBITs?) . \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:ONEWeb:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:CQI:PATTern?', self.__class__.PatternStruct())
