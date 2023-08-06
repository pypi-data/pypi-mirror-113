from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Id:
	"""Id commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("id", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBT:TPS:ID:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dvb.dvbt.tps.id.get_pattern() \n
		Sets the pattern for cell identification. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:DVB:DVBT:TPS:ID:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBT:TPS:ID:PATTern \n
		Snippet: driver.source.bb.dvb.dvbt.tps.id.set_pattern(value = PatternStruct()) \n
		Sets the pattern for cell identification. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:DVB:DVBT:TPS:ID:PATTern', value)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBT:TPS:ID:STATe \n
		Snippet: value: bool = driver.source.bb.dvb.dvbt.tps.id.get_state() \n
		Activates/deactivates the TPS cell identification. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DVB:DVBT:TPS:ID:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBT:TPS:ID:STATe \n
		Snippet: driver.source.bb.dvb.dvbt.tps.id.set_state(state = False) \n
		Activates/deactivates the TPS cell identification. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DVB:DVBT:TPS:ID:STATe {param}')
