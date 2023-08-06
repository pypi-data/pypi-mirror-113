from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Port:
	"""Port commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: PortNull, default value after init: PortNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("port", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_portNull_get', 'repcap_portNull_set', repcap.PortNull.Nr0)

	def repcap_portNull_set(self, enum_value: repcap.PortNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PortNull.Default
		Default value after init: PortNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_portNull_get(self) -> repcap.PortNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	# noinspection PyTypeChecker
	class PortStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bitcount: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bitcount')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bitcount: int = None

	def set(self, structure: PortStruct, portNull=repcap.PortNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:WS:CQIPattern:PORT<CH0> \n
		Snippet: driver.source.bb.eutra.tcw.ws.cqiPattern.port.set(value = [PROPERTY_STRUCT_NAME](), portNull = repcap.PortNull.Default) \n
		In performance test cases, sets the CQI Pattern. \n
			:param structure: for set value, see the help for PortStruct structure arguments.
			:param portNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Port')"""
		portNull_cmd_val = self._base.get_repcap_cmd_value(portNull, repcap.PortNull)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:EUTRa:TCW:WS:CQIPattern:PORT{portNull_cmd_val}', structure)

	def get(self, portNull=repcap.PortNull.Default) -> PortStruct:
		"""SCPI: [SOURce<HW>]:BB:EUTRa:TCW:WS:CQIPattern:PORT<CH0> \n
		Snippet: value: PortStruct = driver.source.bb.eutra.tcw.ws.cqiPattern.port.get(portNull = repcap.PortNull.Default) \n
		In performance test cases, sets the CQI Pattern. \n
			:param portNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Port')
			:return: structure: for return value, see the help for PortStruct structure arguments."""
		portNull_cmd_val = self._base.get_repcap_cmd_value(portNull, repcap.PortNull)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:EUTRa:TCW:WS:CQIPattern:PORT{portNull_cmd_val}?', self.__class__.PortStruct())

	def clone(self) -> 'Port':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Port(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
