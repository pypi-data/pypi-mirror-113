from typing import List

from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal.Types import DataType
from ..............Internal.StructBase import StructBase
from ..............Internal.ArgStruct import ArgStruct
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Ack_Pattern: List[str]: 128 bits Bit pattern
			- Ack_Bitcount: int: integer Pattern length, should be the same as the length set with the command [:SOURcehw]:BB:NR5G:SCHed:CELLch0:SUBFst0:USERdir0:BWPartgr0:ALLocuser0:PUSCh:UCI:ACK:BITS. Range: 0 to 128"""
		__meta_args_list = [
			ArgStruct('Ack_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Ack_Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ack_Pattern: List[str] = None
			self.Ack_Bitcount: int = None

	def set(self, structure: PatternStruct, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH0>:SUBF<ST0>:USER<DIR0>:BWPart<GR0>:ALLoc<USER0>:PUSCh:UCI:ACK:PATTern \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.uci.ack.pattern.set(value = [PROPERTY_STRUCT_NAME](), cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the ACK/CSI 1/CSI 2 bits in pattern form. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')"""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:UCI:ACK:PATTern', structure)

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH0>:SUBF<ST0>:USER<DIR0>:BWPart<GR0>:ALLoc<USER0>:PUSCh:UCI:ACK:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.pusch.uci.ack.pattern.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default) \n
		Sets the ACK/CSI 1/CSI 2 bits in pattern form. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:PUSCh:UCI:ACK:PATTern?', self.__class__.PatternStruct())
