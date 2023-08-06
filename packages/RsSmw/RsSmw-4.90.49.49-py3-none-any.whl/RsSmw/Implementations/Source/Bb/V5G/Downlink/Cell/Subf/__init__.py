from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subf:
	"""Subf commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: SubframeNull, default value after init: SubframeNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subf", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subframeNull_get', 'repcap_subframeNull_set', repcap.SubframeNull.Nr0)

	def repcap_subframeNull_set(self, enum_value: repcap.SubframeNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubframeNull.Default
		Default value after init: SubframeNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subframeNull_get(self) -> repcap.SubframeNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def alloc(self):
		"""alloc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Alloc import Alloc
			self._alloc = Alloc(self._core, self._base)
		return self._alloc

	def clone(self) -> 'Subf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Subf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
