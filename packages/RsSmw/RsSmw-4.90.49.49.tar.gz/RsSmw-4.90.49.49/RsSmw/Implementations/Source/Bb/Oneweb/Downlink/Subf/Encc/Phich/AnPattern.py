from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnPattern:
	"""AnPattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: AntennaPattern, default value after init: AntennaPattern.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("anPattern", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antennaPattern_get', 'repcap_antennaPattern_set', repcap.AntennaPattern.Nr0)

	def repcap_antennaPattern_set(self, enum_value: repcap.AntennaPattern) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaPattern.Default
		Default value after init: AntennaPattern.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antennaPattern_get(self) -> repcap.AntennaPattern:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class AnPatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- An_Pattern: List[str]: No parameter help available
			- Bitcount: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct('An_Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.An_Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: AnPatternStruct, subframeNull=repcap.SubframeNull.Default, antennaPattern=repcap.AntennaPattern.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:[SUBF<ST0>]:ENCC:PHICh:ANPattern<GR0> \n
		Snippet: driver.source.bb.oneweb.downlink.subf.encc.phich.anPattern.set(value = [PROPERTY_STRUCT_NAME](), subframeNull = repcap.SubframeNull.Default, antennaPattern = repcap.AntennaPattern.Default) \n
		No command help available \n
			:param structure: for set value, see the help for AnPatternStruct structure arguments.
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param antennaPattern: optional repeated capability selector. Default value: Nr0 (settable in the interface 'AnPattern')"""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		antennaPattern_cmd_val = self._base.get_repcap_cmd_value(antennaPattern, repcap.AntennaPattern)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:ONEWeb:DL:SUBF{subframeNull_cmd_val}:ENCC:PHICh:ANPattern{antennaPattern_cmd_val}', structure)

	def get(self, subframeNull=repcap.SubframeNull.Default, antennaPattern=repcap.AntennaPattern.Default) -> AnPatternStruct:
		"""SCPI: [SOURce<HW>]:BB:ONEWeb:DL:[SUBF<ST0>]:ENCC:PHICh:ANPattern<GR0> \n
		Snippet: value: AnPatternStruct = driver.source.bb.oneweb.downlink.subf.encc.phich.anPattern.get(subframeNull = repcap.SubframeNull.Default, antennaPattern = repcap.AntennaPattern.Default) \n
		No command help available \n
			:param subframeNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Subf')
			:param antennaPattern: optional repeated capability selector. Default value: Nr0 (settable in the interface 'AnPattern')
			:return: structure: for return value, see the help for AnPatternStruct structure arguments."""
		subframeNull_cmd_val = self._base.get_repcap_cmd_value(subframeNull, repcap.SubframeNull)
		antennaPattern_cmd_val = self._base.get_repcap_cmd_value(antennaPattern, repcap.AntennaPattern)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:ONEWeb:DL:SUBF{subframeNull_cmd_val}:ENCC:PHICh:ANPattern{antennaPattern_cmd_val}?', self.__class__.AnPatternStruct())

	def clone(self) -> 'AnPattern':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnPattern(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
