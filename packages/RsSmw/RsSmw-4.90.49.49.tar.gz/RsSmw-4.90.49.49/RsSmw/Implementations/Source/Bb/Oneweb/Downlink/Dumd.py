from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.Utilities import trim_str_response
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dumd:
	"""Dumd commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dumd", core, parent)

	# noinspection PyTypeChecker
	def get_data(self) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.oneweb.downlink.dumd.get_data() \n
		No command help available \n
			:return: data: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)

	def set_data(self, data: enums.DataSourceA) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:DATA \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_data(data = enums.DataSourceA.DLISt) \n
		No command help available \n
			:param data: No help available
		"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSourceA)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:DATA {param}')

	def get_dselect(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:DSELect \n
		Snippet: value: str = driver.source.bb.oneweb.downlink.dumd.get_dselect() \n
		No command help available \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:DSELect?')
		return trim_str_response(response)

	def set_dselect(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:DSELect \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_dselect(filename = '1') \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:DSELect {param}')

	# noinspection PyTypeChecker
	def get_modulation(self) -> enums.ModulationB:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:MODulation \n
		Snippet: value: enums.ModulationB = driver.source.bb.oneweb.downlink.dumd.get_modulation() \n
		No command help available \n
			:return: modulation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationB)

	def set_modulation(self, modulation: enums.ModulationB) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:MODulation \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_modulation(modulation = enums.ModulationB.QAM16) \n
		No command help available \n
			:param modulation: No help available
		"""
		param = Conversions.enum_scalar_to_str(modulation, enums.ModulationB)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:MODulation {param}')

	def get_op_sub_frames(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:OPSubframes \n
		Snippet: value: bool = driver.source.bb.oneweb.downlink.dumd.get_op_sub_frames() \n
		No command help available \n
			:return: omit_prs_sf: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:OPSubframes?')
		return Conversions.str_to_bool(response)

	def set_op_sub_frames(self, omit_prs_sf: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:OPSubframes \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_op_sub_frames(omit_prs_sf = False) \n
		No command help available \n
			:param omit_prs_sf: No help available
		"""
		param = Conversions.bool_to_str(omit_prs_sf)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:OPSubframes {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.oneweb.downlink.dumd.get_pattern() \n
		No command help available \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:PATTern \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_pattern(value = PatternStruct()) \n
		No command help available \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:PATTern', value)

	def get_power(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:POWer \n
		Snippet: value: float = driver.source.bb.oneweb.downlink.dumd.get_power() \n
		No command help available \n
			:return: power: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:POWer?')
		return Conversions.str_to_float(response)

	def set_power(self, power: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:DUMD:POWer \n
		Snippet: driver.source.bb.oneweb.downlink.dumd.set_power(power = 1.0) \n
		No command help available \n
			:param power: No help available
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'SOURce<HwInstance>:BB:ONEWeb:DL:DUMD:POWer {param}')
