from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scrambler:
	"""Scrambler commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scrambler", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:SCRambler:MODE \n
		Snippet: value: bool = driver.source.bb.wlad.pconfig.scrambler.get_mode() \n
		Sets the mode for the scrambler. \n
			:return: mode: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:SCRambler:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, mode: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:SCRambler:MODE \n
		Snippet: driver.source.bb.wlad.pconfig.scrambler.set_mode(mode = False) \n
		Sets the mode for the scrambler. \n
			:param mode: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:SCRambler:MODE {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 4"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:SCRambler:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.wlad.pconfig.scrambler.get_pattern() \n
		Sets the scrambler initialization value when BB:WLAD:PCON:SCR:MODE ON. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:WLAD:PCONfig:SCRambler:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:SCRambler:PATTern \n
		Snippet: driver.source.bb.wlad.pconfig.scrambler.set_pattern(value = PatternStruct()) \n
		Sets the scrambler initialization value when BB:WLAD:PCON:SCR:MODE ON. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:WLAD:PCONfig:SCRambler:PATTern', value)
