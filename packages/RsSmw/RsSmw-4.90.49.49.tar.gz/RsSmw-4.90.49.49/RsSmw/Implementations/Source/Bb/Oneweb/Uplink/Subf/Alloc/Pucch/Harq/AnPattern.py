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
			- Ack_Nack_Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 32"""
		__meta_args_list = [
			ArgStruct('Ack_Nack_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ack_Nack_Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: AnPatternStruct, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:HARQ:ANPattern \n
		Snippet: driver.source.bb.oneweb.uplink.subf.alloc.pucch.harq.anPattern.set(value = [PROPERTY_STRUCT_NAME](), subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the PUCCH ACK/NACK pattern or ACK/NACK + SR pattern per subframe. \n
			:param structure: for set value, see the help for AnPatternStruct structure arguments.
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')"""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:ONEWeb:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:HARQ:ANPattern', structure)

	def get(self, subframeNull=repcap.SubframeNull.Default, allocationNull=repcap.AllocationNull.Default) -> AnPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:UL:[SUBF<ST0>]:ALLoc<CH0>:PUCCh:HARQ:ANPattern \n
		Snippet: value: AnPatternStruct = driver.source.bb.oneweb.uplink.subf.alloc.pucch.harq.anPattern.get(subframeNull = repcap.SubframeNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the PUCCH ACK/NACK pattern or ACK/NACK + SR pattern per subframe. \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for AnPatternStruct structure arguments."""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:ONEWeb:UL:SUBF{subframeNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUCCh:HARQ:ANPattern?', self.__class__.AnPatternStruct())
