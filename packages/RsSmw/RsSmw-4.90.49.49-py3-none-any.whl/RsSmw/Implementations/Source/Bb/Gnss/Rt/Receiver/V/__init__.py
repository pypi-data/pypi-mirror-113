from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class V:
	"""V commands group definition. 5 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: Vehicle, default value after init: Vehicle.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("v", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_vehicle_get', 'repcap_vehicle_set', repcap.Vehicle.Nr1)

	def repcap_vehicle_set(self, enum_value: repcap.Vehicle) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Vehicle.Default
		Default value after init: Vehicle.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_vehicle_get(self) -> repcap.Vehicle:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def hilPosition(self):
		"""hilPosition commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hilPosition'):
			from .HilPosition import HilPosition
			self._hilPosition = HilPosition(self._core, self._base)
		return self._hilPosition

	@property
	def rlocation(self):
		"""rlocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rlocation'):
			from .Rlocation import Rlocation
			self._rlocation = Rlocation(self._core, self._base)
		return self._rlocation

	@property
	def rvelocity(self):
		"""rvelocity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvelocity'):
			from .Rvelocity import Rvelocity
			self._rvelocity = Rvelocity(self._core, self._base)
		return self._rvelocity

	def clone(self) -> 'V':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = V(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
