from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 5 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: Cell, default value after init: Cell.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_cell_get', 'repcap_cell_set', repcap.Cell.Nr1)

	def repcap_cell_set(self, enum_value: repcap.Cell) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Cell.Default
		Default value after init: Cell.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_cell_get(self) -> repcap.Cell:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def csi(self):
		"""csi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi'):
			from .Csi import Csi
			self._csi = Csi(self._core, self._base)
		return self._csi

	@property
	def dmrs(self):
		"""dmrs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import Dmrs
			self._dmrs = Dmrs(self._core, self._base)
		return self._dmrs

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
