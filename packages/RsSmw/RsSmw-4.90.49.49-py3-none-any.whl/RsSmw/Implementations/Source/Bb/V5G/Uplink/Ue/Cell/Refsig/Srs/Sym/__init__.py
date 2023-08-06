from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sym:
	"""Sym commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: IndexNull, default value after init: IndexNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sym", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_indexNull_get', 'repcap_indexNull_set', repcap.IndexNull.Nr0)

	def repcap_indexNull_set(self, enum_value: repcap.IndexNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndexNull.Default
		Default value after init: IndexNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_indexNull_get(self) -> repcap.IndexNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ntrans(self):
		"""ntrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntrans'):
			from .Ntrans import Ntrans
			self._ntrans = Ntrans(self._core, self._base)
		return self._ntrans

	@property
	def subf(self):
		"""subf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subf'):
			from .Subf import Subf
			self._subf = Subf(self._core, self._base)
		return self._subf

	def clone(self) -> 'Sym':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sym(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
