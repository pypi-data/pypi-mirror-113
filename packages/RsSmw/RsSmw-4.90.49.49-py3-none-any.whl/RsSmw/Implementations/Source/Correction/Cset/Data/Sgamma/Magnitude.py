from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Magnitude:
	"""Magnitude commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("magnitude", core, parent)

	def get_points(self) -> int:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude:POINts \n
		Snippet: value: int = driver.source.correction.cset.data.sgamma.magnitude.get_points() \n
		No command help available \n
			:return: points: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude:POINts?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Magnitude_1: List[float]: No parameter help available
			- Magnitude_N: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Magnitude_1', DataType.FloatList, None, False, True, 1),
			ArgStruct.scalar_float_optional('Magnitude_N')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Magnitude_1: List[float] = None
			self.Magnitude_N: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude \n
		Snippet: value: ValueStruct = driver.source.correction.cset.data.sgamma.magnitude.get_value() \n
		No command help available \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:MAGNitude \n
		Snippet: driver.source.correction.cset.data.sgamma.magnitude.set_value(value = ValueStruct()) \n
		No command help available \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:MAGNitude', value)
