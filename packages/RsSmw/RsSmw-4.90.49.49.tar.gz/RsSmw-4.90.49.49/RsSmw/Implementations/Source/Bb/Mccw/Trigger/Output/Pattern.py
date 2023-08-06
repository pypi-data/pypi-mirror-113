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
			- Bitcount: int: integer 0 = marker off, 1 = marker on Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, output=repcap.Output.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:MCCW:TRIGger:OUTPut<CH>:PATTern \n
		Snippet: driver.source.bb.mccw.trigger.output.pattern.set(value = [PROPERTY_STRUCT_NAME](), output = repcap.Output.Default) \n
		Defines the bit pattern used to generate the marker signal. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		output_cmd_val = self._base.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:MCCW:TRIGger:OUTPut{output_cmd_val}:PATTern', structure)

	def get(self, output=repcap.Output.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:MCCW:TRIGger:OUTPut<CH>:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.mccw.trigger.output.pattern.get(output = repcap.Output.Default) \n
		Defines the bit pattern used to generate the marker signal. \n
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		output_cmd_val = self._base.get_repcap_cmd_value(output, repcap.Output)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:MCCW:TRIGger:OUTPut{output_cmd_val}:PATTern?', self.__class__.PatternStruct())
