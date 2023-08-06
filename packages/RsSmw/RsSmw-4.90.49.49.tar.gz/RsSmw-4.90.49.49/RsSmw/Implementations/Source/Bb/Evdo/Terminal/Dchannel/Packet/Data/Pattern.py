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

	def set(self, structure: PatternStruct, terminal=repcap.Terminal.Default, packet=repcap.Packet.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:DATA:PATTern \n
		Snippet: driver.source.bb.evdo.terminal.dchannel.packet.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), terminal = repcap.Terminal.Default, packet = repcap.Packet.Default) \n
		(enabled for an access terminal working in traffic mode) Selects the bit pattern for the data source. Note: Configuration
		of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for physical layer subtype 2. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param packet: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		terminal_cmd_val = self._base.get_repcap_cmd_value(terminal, repcap.Terminal)
		packet_cmd_val = self._base.get_repcap_cmd_value(packet, repcap.Packet)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DCHannel:PACKet{packet_cmd_val}:DATA:PATTern', structure)

	def get(self, terminal=repcap.Terminal.Default, packet=repcap.Packet.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.evdo.terminal.dchannel.packet.data.pattern.get(terminal = repcap.Terminal.Default, packet = repcap.Packet.Default) \n
		(enabled for an access terminal working in traffic mode) Selects the bit pattern for the data source. Note: Configuration
		of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for physical layer subtype 2. \n
			:param terminal: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param packet: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		terminal_cmd_val = self._base.get_repcap_cmd_value(terminal, repcap.Terminal)
		packet_cmd_val = self._base.get_repcap_cmd_value(packet, repcap.Packet)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EVDO:TERMinal{terminal_cmd_val}:DCHannel:PACKet{packet_cmd_val}:DATA:PATTern?', self.__class__.PatternStruct())
