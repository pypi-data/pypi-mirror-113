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
	"""Data commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def get_dselection(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA:DSELection \n
		Snippet: value: str = driver.source.bb.huwb.fconfig.data.get_dselection() \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the DLIS is selected. \n
			:return: dselection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA:DSELection \n
		Snippet: driver.source.bb.huwb.fconfig.data.set_dselection(dselection = '1') \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the DLIS is selected. \n
			:param dselection: string
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:DSELection {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Dpattern: List[str]: numeric
			- Bitcount: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Dpattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dpattern: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.huwb.fconfig.data.get_pattern() \n
		Sets the data pattern, if pattern is selected as the data source. See [:SOURce<hw>]:BB:HUWB:FCONfig:DATA. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA:PATTern \n
		Snippet: driver.source.bb.huwb.fconfig.data.set_pattern(value = PatternStruct()) \n
		Sets the data pattern, if pattern is selected as the data source. See [:SOURce<hw>]:BB:HUWB:FCONfig:DATA. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:PATTern', value)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.HrpUwbDataSource:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA \n
		Snippet: value: enums.HrpUwbDataSource = driver.source.bb.huwb.fconfig.data.get_value() \n
		Sets the data source for the payload data in a frame. \n
			:return: data_source: PN9| PN11| PN15| PN20| PN16| PN21| PN23| ONE| ZERO| DLISt| PATT PNxx The pseudo-random sequence generator is used as the data source. There is a choice of different lengths of random sequence. DLISt A data list is used. The data list is selected with the aid of command SOURce1:BB:HUWB:DATA DLISt. ALL0 | ALL1 Internal 0 or 1 data is used. PATT Internal data is used. The bit pattern for the data is defined with the aid of command SOURce1:BB:HUWB:DATA:PATTern.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbDataSource)

	def set_value(self, data_source: enums.HrpUwbDataSource) -> None:
		"""SCPI: [SOURce<HW>]:BB:HUWB:FCONfig:DATA \n
		Snippet: driver.source.bb.huwb.fconfig.data.set_value(data_source = enums.HrpUwbDataSource.DLISt) \n
		Sets the data source for the payload data in a frame. \n
			:param data_source: PN9| PN11| PN15| PN20| PN16| PN21| PN23| ONE| ZERO| DLISt| PATT PNxx The pseudo-random sequence generator is used as the data source. There is a choice of different lengths of random sequence. DLISt A data list is used. The data list is selected with the aid of command SOURce1:BB:HUWB:DATA DLISt. ALL0 | ALL1 Internal 0 or 1 data is used. PATT Internal data is used. The bit pattern for the data is defined with the aid of command SOURce1:BB:HUWB:DATA:PATTern.
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.HrpUwbDataSource)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:DATA {param}')
