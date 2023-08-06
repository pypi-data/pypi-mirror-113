from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToaData:
	"""ToaData commands group definition. 7 total commands, 0 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("toaData", core, parent)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Year: int: integer Range: 1980 to 9999
			- Month: int: integer Range: 1 to 12
			- Day: int: integer Range: 1 to 31"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get_date(self) -> DateStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:DATE \n
		Snippet: value: DateStruct = driver.source.bb.gnss.adGeneration.gps.toaData.get_date() \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the date for the
		assistance data in DMS format of the Gregorian calendar. \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:DATE?', self.__class__.DateStruct())

	def set_date(self, value: DateStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:DATE \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_date(value = DateStruct()) \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the date for the
		assistance data in DMS format of the Gregorian calendar. \n
			:param value: see the help for DateStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:DATE', value)

	def get_duration(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:DURation \n
		Snippet: value: float = driver.source.bb.gnss.adGeneration.gps.toaData.get_duration() \n
		Sets the duration of the assistance data. \n
			:return: duration: float Range: 1E-3 to 5E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, duration: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:DURation \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_duration(duration = 1.0) \n
		Sets the duration of the assistance data. \n
			:param duration: float Range: 1E-3 to 5E3
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:DURation {param}')

	def get_resolution(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:RESolution \n
		Snippet: value: float = driver.source.bb.gnss.adGeneration.gps.toaData.get_resolution() \n
		Sets the resolution of the assistance data. \n
			:return: resolution: float Range: 1E-3 to 5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:RESolution?')
		return Conversions.str_to_float(response)

	def set_resolution(self, resolution: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:RESolution \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_resolution(resolution = 1.0) \n
		Sets the resolution of the assistance data. \n
			:param resolution: float Range: 1E-3 to 5
		"""
		param = Conversions.decimal_value_to_str(resolution)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:RESolution {param}')

	# noinspection PyTypeChecker
	def get_tbasis(self) -> enums.TimeBasis:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis \n
		Snippet: value: enums.TimeBasis = driver.source.bb.gnss.adGeneration.gps.toaData.get_tbasis() \n
		Determines the timebase used to enter the time of assistance data parameters. \n
			:return: time_basis: UTC| GPS| GST| GLO| BDT| NAV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TBASis?')
		return Conversions.str_to_scalar_enum(response, enums.TimeBasis)

	def set_tbasis(self, time_basis: enums.TimeBasis) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_tbasis(time_basis = enums.TimeBasis.BDT) \n
		Determines the timebase used to enter the time of assistance data parameters. \n
			:param time_basis: UTC| GPS| GST| GLO| BDT| NAV
		"""
		param = Conversions.enum_scalar_to_str(time_basis, enums.TimeBasis)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TBASis {param}')

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Hour: int: integer Range: 0 to 23
			- Minute: int: integer Range: 0 to 59
			- Second: float: float Range: 0 to 59.999"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Minute'),
			ArgStruct.scalar_float('Second')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Minute: int = None
			self.Second: float = None

	def get_time(self) -> TimeStruct:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TIME \n
		Snippet: value: TimeStruct = driver.source.bb.gnss.adGeneration.gps.toaData.get_time() \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the exact start time
		for the assistance data in UTC time format. \n
			:return: structure: for return value, see the help for TimeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TIME?', self.__class__.TimeStruct())

	def set_time(self, value: TimeStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TIME \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_time(value = TimeStruct()) \n
		Enabled for UTC or GLONASS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Enters the exact start time
		for the assistance data in UTC time format. \n
			:param value: see the help for TimeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TIME', value)

	def get_to_week(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TOWeek \n
		Snippet: value: int = driver.source.bb.gnss.adGeneration.gps.toaData.get_to_week() \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Determines the Time of Week (TOW) the
		assistance data is generated for. \n
			:return: tow: integer Range: -604800 to 604800
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TOWeek?')
		return Conversions.str_to_int(response)

	def set_to_week(self, tow: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:TOWeek \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_to_week(tow = 1) \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:GPS:TOAData:TBASis) . Determines the Time of Week (TOW) the
		assistance data is generated for. \n
			:param tow: integer Range: -604800 to 604800
		"""
		param = Conversions.decimal_value_to_str(tow)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:TOWeek {param}')

	def get_wnumber(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:WNUMber \n
		Snippet: value: int = driver.source.bb.gnss.adGeneration.gps.toaData.get_wnumber() \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:QZSS:TOAData:TBASis) . Sets the week number (WN) the
		assistance data is generated for. \n
			:return: week_number: integer Range: 0 to 9999.0*53
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:WNUMber?')
		return Conversions.str_to_int(response)

	def set_wnumber(self, week_number: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ADGeneration:GPS:TOAData:WNUMber \n
		Snippet: driver.source.bb.gnss.adGeneration.gps.toaData.set_wnumber(week_number = 1) \n
		Enabled for GPS timebase ([:SOURce<hw>]:BB:GNSS:ADGeneration:QZSS:TOAData:TBASis) . Sets the week number (WN) the
		assistance data is generated for. \n
			:param week_number: integer Range: 0 to 9999.0*53
		"""
		param = Conversions.decimal_value_to_str(week_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GPS:TOAData:WNUMber {param}')
