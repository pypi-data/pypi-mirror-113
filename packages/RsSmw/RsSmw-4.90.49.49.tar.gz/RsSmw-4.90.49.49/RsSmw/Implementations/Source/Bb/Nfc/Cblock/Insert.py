from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:INSert \n
		Snippet: driver.source.bb.nfc.cblock.insert.set(commandBlock = repcap.CommandBlock.Default) \n
		Inserts a default command block before the selected command block. The command block with this position must be existing,
		otherwise an error is returned. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		commandBlock_cmd_val = self._base.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:INSert')

	def set_with_opc(self, commandBlock=repcap.CommandBlock.Default) -> None:
		commandBlock_cmd_val = self._base.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:INSert \n
		Snippet: driver.source.bb.nfc.cblock.insert.set_with_opc(commandBlock = repcap.CommandBlock.Default) \n
		Inserts a default command block before the selected command block. The command block with this position must be existing,
		otherwise an error is returned. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:INSert')
