from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubPath:
	"""SubPath commands group definition. 5 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: SubPath, default value after init: SubPath.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subPath", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subPath_get', 'repcap_subPath_set', repcap.SubPath.Nr1)

	def repcap_subPath_set(self, enum_value: repcap.SubPath) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubPath.Default
		Default value after init: SubPath.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subPath_get(self) -> repcap.SubPath:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def phase(self):
		"""phase commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'SubPath':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubPath(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
