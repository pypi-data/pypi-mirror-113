from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sbyte:
	"""Sbyte commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sbyte", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sync: List[str]: numeric
			- Bitcount: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Sync', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sync: List[str] = None
			self.Bitcount: int = None

	def get_pattern(self) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:BHConfig:SBYTe:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.dvb.dvbx.bhConfig.sbyte.get_pattern() \n
		Sets the user packet synchronization byte. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:DVB:DVBX:BHConfig:SBYTe:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""SCPI: [SOURce<HW>]:BB:DVB:DVBX:BHConfig:SBYTe:PATTern \n
		Snippet: driver.source.bb.dvb.dvbx.bhConfig.sbyte.set_pattern(value = PatternStruct()) \n
		Sets the user packet synchronization byte. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:DVB:DVBX:BHConfig:SBYTe:PATTern', value)
