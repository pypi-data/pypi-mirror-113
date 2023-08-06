from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tap:
	"""Tap commands group definition. 3 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: MimoTap, default value after init: MimoTap.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tap", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_mimoTap_get', 'repcap_mimoTap_set', repcap.MimoTap.Nr1)

	def repcap_mimoTap_set(self, enum_value: repcap.MimoTap) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MimoTap.Default
		Default value after init: MimoTap.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_mimoTap_get(self) -> repcap.MimoTap:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def subCluster(self):
		"""subCluster commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_subCluster'):
			from .SubCluster import SubCluster
			self._subCluster = SubCluster(self._core, self._base)
		return self._subCluster

	def clone(self) -> 'Tap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
