from typing import List

from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal.Types import DataType
from ............Internal.StructBase import StructBase
from ............Internal.ArgStruct import ArgStruct
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SltPatt:
	"""SltPatt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sltPatt", core, parent)

	# noinspection PyTypeChecker
	class SltPattStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Rate_Mat_Slot_Patt: List[str]: 28 bits
			- Bitcount: int: integer Range: 14 to 28"""
		__meta_args_list = [
			ArgStruct('Rate_Mat_Slot_Patt', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rate_Mat_Slot_Patt: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: SltPattStruct, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, rateSettingNull=repcap.RateSettingNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH0>:CELL<ST0>:DL:BWP<DIR0>:RATM:RS<GR0>:SLTPatt \n
		Snippet: driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.ratm.rs.sltPatt.set(value = [PROPERTY_STRUCT_NAME](), userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, rateSettingNull = repcap.RateSettingNull.Default) \n
		Set the slots to be used as a pattern. \n
			:param structure: for set value, see the help for SltPattStruct structure arguments.
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSettingNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')"""
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		rateSettingNull_cmd_val = self._base.get_repcap_cmd_value(rateSettingNull, repcap.RateSettingNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:RATM:RS{rateSettingNull_cmd_val}:SLTPatt', structure)

	def get(self, userNull=repcap.UserNull.Default, cellNull=repcap.CellNull.Default, bwPartNull=repcap.BwPartNull.Default, rateSettingNull=repcap.RateSettingNull.Default) -> SltPattStruct:
		"""SCPI: [SOURce<HW>]:BB:NR5G:UBWP:USER<CH0>:CELL<ST0>:DL:BWP<DIR0>:RATM:RS<GR0>:SLTPatt \n
		Snippet: value: SltPattStruct = driver.source.bb.nr5G.ubwp.user.cell.downlink.bwp.ratm.rs.sltPatt.get(userNull = repcap.UserNull.Default, cellNull = repcap.CellNull.Default, bwPartNull = repcap.BwPartNull.Default, rateSettingNull = repcap.RateSettingNull.Default) \n
		Set the slots to be used as a pattern. \n
			:param userNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param bwPartNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSettingNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')
			:return: structure: for return value, see the help for SltPattStruct structure arguments."""
		userNull_cmd_val = self._base.get_repcap_cmd_value(userNull, repcap.UserNull)
		cellNull_cmd_val = self._base.get_repcap_cmd_value(cellNull, repcap.CellNull)
		bwPartNull_cmd_val = self._base.get_repcap_cmd_value(bwPartNull, repcap.BwPartNull)
		rateSettingNull_cmd_val = self._base.get_repcap_cmd_value(rateSettingNull, repcap.RateSettingNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{userNull_cmd_val}:CELL{cellNull_cmd_val}:DL:BWP{bwPartNull_cmd_val}:RATM:RS{rateSettingNull_cmd_val}:SLTPatt?', self.__class__.SltPattStruct())
