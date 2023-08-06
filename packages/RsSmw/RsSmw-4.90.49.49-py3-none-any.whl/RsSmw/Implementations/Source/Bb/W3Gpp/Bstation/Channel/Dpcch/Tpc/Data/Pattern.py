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
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:DPCCh:TPC:DATA:PATTern \n
		Snippet: driver.source.bb.w3Gpp.bstation.channel.dpcch.tpc.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		Determines the bit pattern. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')"""
		baseStation_cmd_val = self._base.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._base.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:DPCCh:TPC:DATA:PATTern', structure)

	def get(self, baseStation=repcap.BaseStation.Default, channelNull=repcap.ChannelNull.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH0>:DPCCh:TPC:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.w3Gpp.bstation.channel.dpcch.tpc.data.pattern.get(baseStation = repcap.BaseStation.Default, channelNull = repcap.ChannelNull.Default) \n
		Determines the bit pattern. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		baseStation_cmd_val = self._base.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		channelNull_cmd_val = self._base.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:CHANnel{channelNull_cmd_val}:DPCCh:TPC:DATA:PATTern?', self.__class__.PatternStruct())
