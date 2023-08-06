from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PatternStruct, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DG:GPOLynomial:PATTern \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.dg.gpolynomial.pattern.set(value = [PROPERTY_STRUCT_NAME](), vdbTransmitter = repcap.VdbTransmitter.Default) \n
		No command help available \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DG:GPOLynomial:PATTern', structure)

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> PatternStruct:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DG:GPOLynomial:PATTern \n
		Snippet: value: PatternStruct = driver.source.bb.gbas.vdb.mconfig.dg.gpolynomial.pattern.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		No command help available \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		vdbTransmitter_cmd_val = self._base.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DG:GPOLynomial:PATTern?', self.__class__.PatternStruct())
