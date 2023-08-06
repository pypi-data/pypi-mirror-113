from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH0>:DPCH:CCODing:STATe \n
		Snippet: driver.source.bb.w3Gpp.bstation.enhanced.channel.dpch.ccoding.state.set(state = False, channelNull = repcap.ChannelNull.Default) \n
		The command activates or deactivates channel coding for the selected enhanced DPCH. When channel coding is activated and
		a channel coding type conforming to the standard is selected, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.
		Dpch.Ccoding.TypePy.set) the slot format, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.Sformat.
		set) and thus the symbol rate, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.SymbolRate.get_) the
		bits per frame, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.BpFrame.get_) , the pilot length
		(method RsSmw.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.Plength.set) and the TFCI state (BB:W3GP:BST1:CHAN:DPCC:TFCI STAT)
		are set to the associated values. \n
			:param state: ON| OFF
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(state)
		channelNull_cmd_val = self._base.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channelNull_cmd_val}:DPCH:CCODing:STATe {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH0>:DPCH:CCODing:STATe \n
		Snippet: value: bool = driver.source.bb.w3Gpp.bstation.enhanced.channel.dpch.ccoding.state.get(channelNull = repcap.ChannelNull.Default) \n
		The command activates or deactivates channel coding for the selected enhanced DPCH. When channel coding is activated and
		a channel coding type conforming to the standard is selected, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.
		Dpch.Ccoding.TypePy.set) the slot format, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.Sformat.
		set) and thus the symbol rate, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.SymbolRate.get_) the
		bits per frame, (method RsSmw.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.BpFrame.get_) , the pilot length
		(method RsSmw.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.Plength.set) and the TFCI state (BB:W3GP:BST1:CHAN:DPCC:TFCI STAT)
		are set to the associated values. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Channel')
			:return: state: ON| OFF"""
		channelNull_cmd_val = self._base.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channelNull_cmd_val}:DPCH:CCODing:STATe?')
		return Conversions.str_to_bool(response)
