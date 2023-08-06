from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ue:
	"""Ue commands group definition. 3 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: UserEquipment, default value after init: UserEquipment.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ue", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_userEquipment_get', 'repcap_userEquipment_set', repcap.UserEquipment.Nr1)

	def repcap_userEquipment_set(self, enum_value: repcap.UserEquipment) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserEquipment.Default
		Default value after init: UserEquipment.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_userEquipment_get(self) -> repcap.UserEquipment:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def frc(self):
		"""frc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frc'):
			from .Frc import Frc
			self._frc = Frc(self._core, self._base)
		return self._frc

	@property
	def plevel(self):
		"""plevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plevel'):
			from .Plevel import Plevel
			self._plevel = Plevel(self._core, self._base)
		return self._plevel

	@property
	def ueId(self):
		"""ueId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueId'):
			from .UeId import UeId
			self._ueId = UeId(self._core, self._base)
		return self._ueId

	def clone(self) -> 'Ue':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ue(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
