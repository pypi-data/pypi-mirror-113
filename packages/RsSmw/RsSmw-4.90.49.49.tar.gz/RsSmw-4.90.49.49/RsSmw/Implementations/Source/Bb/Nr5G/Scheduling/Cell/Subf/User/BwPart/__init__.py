from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwPart:
	"""BwPart commands group definition. 408 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: BwPartNull, default value after init: BwPartNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bwPart", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bwPartNull_get', 'repcap_bwPartNull_set', repcap.BwPartNull.Nr0)

	def repcap_bwPartNull_set(self, enum_value: repcap.BwPartNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BwPartNull.Default
		Default value after init: BwPartNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bwPartNull_get(self) -> repcap.BwPartNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def alloc(self):
		"""alloc commands group. 30 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Alloc import Alloc
			self._alloc = Alloc(self._core, self._base)
		return self._alloc

	@property
	def nalloc(self):
		"""nalloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nalloc'):
			from .Nalloc import Nalloc
			self._nalloc = Nalloc(self._core, self._base)
		return self._nalloc

	@property
	def resulting(self):
		"""resulting commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_resulting'):
			from .Resulting import Resulting
			self._resulting = Resulting(self._core, self._base)
		return self._resulting

	def clone(self) -> 'BwPart':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwPart(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
