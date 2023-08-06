from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coefficients:
	"""Coefficients commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coefficients", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:CATalog \n
		Snippet: value: List[str] = driver.source.iq.doherty.shaping.polynomial.coefficients.get_catalog() \n
		Queries the available polynomial files in the default directory. Only files with the file extension *.dpd_poly are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:LOAD \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.load(filename = '1') \n
		Loads the selected polynomial file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:STORe \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.set_store(filename = '1') \n
		Saves the polynomial function as polynomial file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients:STORe {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ipart_0: List[float]: No parameter help available
			- J_0: float: float Range: -1E6 to 1E6
			- I_1: float: No parameter help available
			- J_1: float: float Range: -1E6 to 1E6"""
		__meta_args_list = [
			ArgStruct('Ipart_0', DataType.FloatList, None, False, True, 1),
			ArgStruct.scalar_float('J_0'),
			ArgStruct.scalar_float('I_1'),
			ArgStruct.scalar_float('J_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ipart_0: List[float] = None
			self.J_0: float = None
			self.I_1: float = None
			self.J_1: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients \n
		Snippet: value: ValueStruct = driver.source.iq.doherty.shaping.polynomial.coefficients.get_value() \n
		Sets the polynomial coefficients as a list of up to 10 comma separated value pairs. In Cartesian coordinates system, the
		coefficients bn are expressed in degrees. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: [SOURce<HW>]:IQ:DOHerty:SHAPing:POLYnomial:COEFficients \n
		Snippet: driver.source.iq.doherty.shaping.polynomial.coefficients.set_value(value = ValueStruct()) \n
		Sets the polynomial coefficients as a list of up to 10 comma separated value pairs. In Cartesian coordinates system, the
		coefficients bn are expressed in degrees. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:IQ:DOHerty:SHAPing:POLYnomial:COEFficients', value)
