from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


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

	def set(self, structure: PatternStruct, commandBlock=repcap.CommandBlock.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DATA:PATTern \n
		Snippet: driver.source.bb.nfc.cblock.data.pattern.set(value = [PROPERTY_STRUCT_NAME](), commandBlock = repcap.CommandBlock.Default) \n
		Defines a bit pattern. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		commandBlock_cmd_val = self._base.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:DATA:PATTern', structure)

	def get(self, commandBlock=repcap.CommandBlock.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:NFC:CBLock<CH>:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.nfc.cblock.data.pattern.get(commandBlock = repcap.CommandBlock.Default) \n
		Defines a bit pattern. \n
			:param commandBlock: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		commandBlock_cmd_val = self._base.get_repcap_cmd_value(commandBlock, repcap.CommandBlock)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NFC:CBLock{commandBlock_cmd_val}:DATA:PATTern?', self.__class__.PatternStruct())
