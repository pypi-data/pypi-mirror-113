from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Column:
	"""Column commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: Column, default value after init: Column.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("column", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_column_get', 'repcap_column_set', repcap.Column.Nr1)

	def repcap_column_set(self, enum_value: repcap.Column) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Column.Default
		Default value after init: Column.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_column_get(self) -> repcap.Column:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def imagin(self):
		"""imagin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imagin'):
			from .Imagin import Imagin
			self._imagin = Imagin(self._core, self._base)
		return self._imagin

	@property
	def real(self):
		"""real commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_real'):
			from .Real import Real
			self._real = Real(self._core, self._base)
		return self._real

	def clone(self) -> 'Column':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Column(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
