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
			- Nbiot_An_Pat: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 1"""
		__meta_args_list = [
			ArgStruct('Nbiot_An_Pat', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nbiot_An_Pat: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, userEquipment=repcap.UserEquipment.Default, transmission=repcap.Transmission.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:HARQ:PATTern \n
		Snippet: driver.source.bb.eutra.uplink.ue.niot.trans.harq.pattern.set(value = [PROPERTY_STRUCT_NAME](), userEquipment = repcap.UserEquipment.Default, transmission = repcap.Transmission.Default) \n
		Set the ACK/ANCK pattern. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param transmission: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		userEquipment_cmd_val = self._base.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		transmission_cmd_val = self._base.get_repcap_cmd_value(transmission, repcap.Transmission)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:NIOT:TRANs{transmission_cmd_val}:HARQ:PATTern', structure)

	def get(self, userEquipment=repcap.UserEquipment.Default, transmission=repcap.Transmission.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:HARQ:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.eutra.uplink.ue.niot.trans.harq.pattern.get(userEquipment = repcap.UserEquipment.Default, transmission = repcap.Transmission.Default) \n
		Set the ACK/ANCK pattern. \n
			:param userEquipment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param transmission: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		userEquipment_cmd_val = self._base.get_repcap_cmd_value(userEquipment, repcap.UserEquipment)
		transmission_cmd_val = self._base.get_repcap_cmd_value(transmission, repcap.Transmission)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{userEquipment_cmd_val}:NIOT:TRANs{transmission_cmd_val}:HARQ:PATTern?', self.__class__.PatternStruct())
