from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


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

	def set(self, structure: PatternStruct, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TPC:DATA:PATTern \n
		Snippet: driver.source.bb.w3Gpp.mstation.pcpch.tpc.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), mobileStation = repcap.MobileStation.Default) \n
		The command determines the bit pattern for the PATTern data source selection. The maximum length of the bit pattern is 64
		bits. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		mobileStation_cmd_val = self._base.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PCPCh:TPC:DATA:PATTern', structure)

	def get(self, mobileStation=repcap.MobileStation.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:TPC:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.w3Gpp.mstation.pcpch.tpc.data.pattern.get(mobileStation = repcap.MobileStation.Default) \n
		The command determines the bit pattern for the PATTern data source selection. The maximum length of the bit pattern is 64
		bits. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		mobileStation_cmd_val = self._base.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PCPCh:TPC:DATA:PATTern?', self.__class__.PatternStruct())
