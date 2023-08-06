from typing import List

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.Types import DataType
from ............Internal.StructBase import StructBase
from ............Internal.ArgStruct import ArgStruct
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbpAtt:
	"""RbpAtt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbpAtt", core, parent)

	# noinspection PyTypeChecker
	class RbpAttStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: 275 bits
			- Bitcount: int: integer Range: 275 to 275"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: RbpAttStruct, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, rateSettingNull=repcap.RateSettingNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH0>:CELL<ST0>:DL:BWP<DIR0>:RATM:RS<GR0>:RBPatt \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.ratm.rs.rbpAtt.set(value = [PROPERTY_STRUCT_NAME](), userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, rateSettingNull = repcap.RateSettingNull.Default) \n
		Sets the resource block level bitmap pattern directly, alternatively to loading a data list with the command
		[:SOURce<hw>]:BB:NR5G:UBWP:USER<ch0>:CELL<st0>:DL:BWP<dir0>:RATM:RS<gr0>:RBDList. \n
			:param structure: for set value, see the help for RbpAttStruct structure arguments.
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSettingNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')"""
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		rateSettingNull_cmd_val = self._base.get_repcap_cmd_value(rateSettingNull, repcap.RateSettingNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:RATM:RS{rateSettingNull_cmd_val}:RBPatt', structure)

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, rateSettingNull=repcap.RateSettingNull.Default) -> RbpAttStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH0>:CELL<ST0>:DL:BWP<DIR0>:RATM:RS<GR0>:RBPatt \n
		Snippet: value: RbpAttStruct = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.ratm.rs.rbpAtt.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, rateSettingNull = repcap.RateSettingNull.Default) \n
		Sets the resource block level bitmap pattern directly, alternatively to loading a data list with the command
		[:SOURce<hw>]:BB:NR5G:UBWP:USER<ch0>:CELL<st0>:DL:BWP<dir0>:RATM:RS<gr0>:RBDList. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSettingNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')
			:return: structure: for return value, see the help for RbpAttStruct structure arguments."""
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		rateSettingNull_cmd_val = self._base.get_repcap_cmd_value(rateSettingNull, repcap.RateSettingNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:RATM:RS{rateSettingNull_cmd_val}:RBPatt?', self.__class__.RbpAttStruct())
