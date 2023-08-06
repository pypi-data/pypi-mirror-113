from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsPattern:
	"""UsPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usPattern", core, parent)

	# noinspection PyTypeChecker
	class UsPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Use_Subfr_Pat: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Use_Subfr_Pat', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Use_Subfr_Pat: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: UsPatternStruct, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:USER<CH>:AS:DL:[CELL<CCIDX>]:USPattern \n
		Snippet: driver.source.bb.oneweb.downlink.user.asPy.downlink.cell.usPattern.set(value = [PROPERTY_STRUCT_NAME](), userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param structure: for set value, see the help for UsPatternStruct structure arguments.
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')"""
		userIx_cmd_val = self._base.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:ONEWeb:DL:USER{userIx_cmd_val}:AS:DL:CELL{cellNull_cmd_val}:USPattern', structure)

	def get(self, userIx=repcap.UserIx.Default, cellNull=repcap.CellNull.Default) -> UsPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:USER<CH>:AS:DL:[CELL<CCIDX>]:USPattern \n
		Snippet: value: UsPatternStruct = driver.source.bb.oneweb.downlink.user.asPy.downlink.cell.usPattern.get(userIx = repcap.UserIx.Default, cellNull = repcap.CellNull.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:return: structure: for return value, see the help for UsPatternStruct structure arguments."""
		userIx_cmd_val = self._base.get_repcap_cmd_value(userIx, repcap.UserIx)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:ONEWeb:DL:USER{userIx_cmd_val}:AS:DL:CELL{cellNull_cmd_val}:USPattern?', self.__class__.UsPatternStruct())
