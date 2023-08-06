from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 3 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: CellNull, default value after init: CellNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_cellNull_get', 'repcap_cellNull_set', repcap.CellNull.Nr0)

	def repcap_cellNull_set(self, enum_value: repcap.CellNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CellNull.Default
		Default value after init: CellNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_cellNull_get(self) -> repcap.CellNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .AnPattern import AnPattern
			self._anPattern = AnPattern(self._core, self._base)
		return self._anPattern

	@property
	def group(self):
		"""group commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_group'):
			from .Group import Group
			self._group = Group(self._core, self._base)
		return self._group

	@property
	def noGroups(self):
		"""noGroups commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noGroups'):
			from .NoGroups import NoGroups
			self._noGroups = NoGroups(self._core, self._base)
		return self._noGroups

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
