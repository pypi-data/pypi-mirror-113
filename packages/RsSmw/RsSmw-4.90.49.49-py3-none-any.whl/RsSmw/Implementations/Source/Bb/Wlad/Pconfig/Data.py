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
class Data:
	"""Data commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def get_dselection(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:DSELection \n
		Snippet: value: str = driver.source.bb.wlad.pconfig.data.get_dselection() \n
		Selects a data list, for the DLIST data source selection. The lists are stored as files with the fixed file extensions *.
		dm_iqd in a directory of the user's choice. The directory applicable to the following commands is defined with the
		command method RsSmw.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name without the path and the file extension. \n
			:return: dselection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:DSELection \n
		Snippet: driver.source.bb.wlad.pconfig.data.set_dselection(dselection = '1') \n
		Selects a data list, for the DLIST data source selection. The lists are stored as files with the fixed file extensions *.
		dm_iqd in a directory of the user's choice. The directory applicable to the following commands is defined with the
		command method RsSmw.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name without the path and the file extension. \n
			:param dselection: string
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:DSELection {param}')

	def get_length(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:LENGth \n
		Snippet: value: int = driver.source.bb.wlad.pconfig.data.get_length() \n
		Sets the size of the data field in bytes. The data length is related to the number of data symbols that is set with
		method RsSmw.Source.Bb.Wlad.Pconfig.Data.symbols. Whenever the data length changes, the number of data symbols is updated
		and vice versa. \n
			:return: length: integer Range: 1 to 262107
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:LENGth?')
		return Conversions.str_to_int(response)

	def set_length(self, length: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:LENGth \n
		Snippet: driver.source.bb.wlad.pconfig.data.set_length(length = 1) \n
		Sets the size of the data field in bytes. The data length is related to the number of data symbols that is set with
		method RsSmw.Source.Bb.Wlad.Pconfig.Data.symbols. Whenever the data length changes, the number of data symbols is updated
		and vice versa. \n
			:param length: integer Range: 1 to 262107
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:LENGth {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.wlad.pconfig.data.get_pattern() \n
		Sets the data pattern if BB:WLAD:PCON:DATA PATT. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:PATTern \n
		Snippet: driver.source.bb.wlad.pconfig.data.set_pattern(value = PatternStruct()) \n
		Sets the data pattern if BB:WLAD:PCON:DATA PATT. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:PATTern', value)

	def get_rate(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:RATE \n
		Snippet: value: float = driver.source.bb.wlad.pconfig.data.get_rate() \n
		Queries the PPDU data rate. \n
			:return: rate: float Range: 0 to LONG_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:RATE?')
		return Conversions.str_to_float(response)

	def get_symbols(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:SYMBols \n
		Snippet: value: int = driver.source.bb.wlad.pconfig.data.get_symbols() \n
		No command help available \n
			:return: symbols: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:SYMBols?')
		return Conversions.str_to_int(response)

	def set_symbols(self, symbols: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA:SYMBols \n
		Snippet: driver.source.bb.wlad.pconfig.data.set_symbols(symbols = 1) \n
		No command help available \n
			:param symbols: No help available
		"""
		param = Conversions.decimal_value_to_str(symbols)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:DATA:SYMBols {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.WlannDataSource:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA \n
		Snippet: value: enums.WlannDataSource = driver.source.bb.wlad.pconfig.data.get_value() \n
		Sets the data source. \n
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAD:PCONfig:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.WlannDataSource)

	def set_value(self, data: enums.WlannDataSource) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAD:PCONfig:DATA \n
		Snippet: driver.source.bb.wlad.pconfig.data.set_value(data = enums.WlannDataSource.AMPDU) \n
		Sets the data source. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU
		"""
		param = Conversions.enum_scalar_to_str(data, enums.WlannDataSource)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAD:PCONfig:DATA {param}')
