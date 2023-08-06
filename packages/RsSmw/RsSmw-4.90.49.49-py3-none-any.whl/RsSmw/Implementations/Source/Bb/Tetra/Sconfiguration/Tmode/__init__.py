from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 18 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: TestMode, default value after init: TestMode.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_testMode_get', 'repcap_testMode_set', repcap.TestMode.Nr1)

	def repcap_testMode_set(self, enum_value: repcap.TestMode) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TestMode.Default
		Default value after init: TestMode.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_testMode_get(self) -> repcap.TestMode:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def slot(self):
		"""slot commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	def clone(self) -> 'Tmode':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tmode(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
