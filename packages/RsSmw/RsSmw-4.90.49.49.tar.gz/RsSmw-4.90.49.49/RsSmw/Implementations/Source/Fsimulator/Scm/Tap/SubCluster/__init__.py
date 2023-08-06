from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubCluster:
	"""SubCluster commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: SubCluster, default value after init: SubCluster.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subCluster", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subCluster_get', 'repcap_subCluster_set', repcap.SubCluster.Nr1)

	def repcap_subCluster_set(self, enum_value: repcap.SubCluster) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubCluster.Default
		Default value after init: SubCluster.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subCluster_get(self) -> repcap.SubCluster:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'SubCluster':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubCluster(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
