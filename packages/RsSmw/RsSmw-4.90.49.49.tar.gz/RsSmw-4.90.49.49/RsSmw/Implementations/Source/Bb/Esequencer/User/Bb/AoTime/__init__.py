from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AoTime:
	"""AoTime commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: AttenuationList, default value after init: AttenuationList.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aoTime", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_attenuationList_get', 'repcap_attenuationList_set', repcap.AttenuationList.Nr1)

	def repcap_attenuationList_set(self, enum_value: repcap.AttenuationList) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AttenuationList.Default
		Default value after init: AttenuationList.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_attenuationList_get(self) -> repcap.AttenuationList:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def file(self):
		"""file commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'AoTime':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AoTime(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
