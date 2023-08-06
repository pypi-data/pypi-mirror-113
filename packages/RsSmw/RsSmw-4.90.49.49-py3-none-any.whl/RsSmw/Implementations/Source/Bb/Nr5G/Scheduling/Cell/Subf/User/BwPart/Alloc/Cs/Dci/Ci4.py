from typing import List

from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.Types import DataType
from .............Internal.StructBase import StructBase
from .............Internal.ArgStruct import ArgStruct
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ci4:
	"""Ci4 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ci4", core, parent)

	# noinspection PyTypeChecker
	class Ci4Struct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 7 bits Bit pattern for the cancellation indication.
			- Bitcount: int: integer Range: 1 to 7"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: Ci4Struct, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH0>:SUBF<ST0>:USER<DIR0>:BWPart<GR0>:ALLoc<USER0>:CS:DCI<S2US0>:CI4 \n
		Snippet: driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ci4.set(value = [PROPERTY_STRUCT_NAME](), cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the cancellation indication parameters for the DCI format 2_4. \n
			:param structure: for set value, see the help for Ci4Struct structure arguments.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Dci')"""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		indexNull_cmd_val = self._base.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:DCI{indexNull_cmd_val}:CI4', structure)

	def get(self, cellNull=repcap.CellNull.Default, subframeNull=repcap.SubframeNull.Default, userNull=repcap.UserNull.Default, bwPartNull=repcap.BwPartNull.Default, allocationNull=repcap.AllocationNull.Default, indexNull=repcap.IndexNull.Default) -> Ci4Struct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH0>:SUBF<ST0>:USER<DIR0>:BWPart<GR0>:ALLoc<USER0>:CS:DCI<S2US0>:CI4 \n
		Snippet: value: Ci4Struct = driver.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.cs.dci.ci4.get(cellNull = repcap.CellNull.Default, subframeNull = repcap.SubframeNull.Default, userNull = repcap.UserNull.Default, bwPartNull = repcap.BwPartNull.Default, allocationNull = repcap.AllocationNull.Default, indexNull = repcap.IndexNull.Default) \n
		Sets the cancellation indication parameters for the DCI format 2_4. \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'BwPart')
			:param allocationNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Alloc')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Dci')
			:return: structure: for return value, see the help for Ci4Struct structure arguments."""
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		allocationNull_cmd_val = self._base.get_repcap_cmd_value(allocationNull, repcap.AllocationNull)
		indexNull_cmd_val = self._base.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{cellNull_cmd_val}:SUBF{subframeNull_cmd_val}:USER{userNull_cmd_val}:BWPart{bwPartNull_cmd_val}:ALLoc{allocationNull_cmd_val}:CS:DCI{indexNull_cmd_val}:CI4?', self.__class__.Ci4Struct())
