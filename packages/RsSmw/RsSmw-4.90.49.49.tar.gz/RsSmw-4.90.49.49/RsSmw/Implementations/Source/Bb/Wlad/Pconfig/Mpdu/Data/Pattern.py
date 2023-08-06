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

	def set(self, structure: PatternStruct, macPdu=repcap.MacPdu.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MPDU<ST>:DATA:PATTern \n
		Snippet: driver.source.bb.wlad.pconfig.mpdu.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), macPdu = repcap.MacPdu.Default) \n
		Determines the bit pattern for the PATTern selection. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param macPdu: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')"""
		macPdu_cmd_val = self._base.get_repcap_cmd_value(macPdu, repcap.MacPdu)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MPDU{macPdu_cmd_val}:DATA:PATTern', structure)

	def get(self, macPdu=repcap.MacPdu.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:MPDU<ST>:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.wlad.pconfig.mpdu.data.pattern.get(macPdu = repcap.MacPdu.Default) \n
		Determines the bit pattern for the PATTern selection. \n
			:param macPdu: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		macPdu_cmd_val = self._base.get_repcap_cmd_value(macPdu, repcap.MacPdu)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:WLAD:PCONfig:MPDU{macPdu_cmd_val}:DATA:PATTern?', self.__class__.PatternStruct())
