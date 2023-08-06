from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Row:
	"""Row commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: RowNull, default value after init: RowNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("row", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_rowNull_get', 'repcap_rowNull_set', repcap.RowNull.Nr0)

	def repcap_rowNull_set(self, enum_value: repcap.RowNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RowNull.Default
		Default value after init: RowNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_rowNull_get(self) -> repcap.RowNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def imaginary(self):
		"""imaginary commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imaginary'):
			from .Imaginary import Imaginary
			self._imaginary = Imaginary(self._core, self._base)
		return self._imaginary

	@property
	def magnitude(self):
		"""magnitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_magnitude'):
			from .Magnitude import Magnitude
			self._magnitude = Magnitude(self._core, self._base)
		return self._magnitude

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def real(self):
		"""real commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_real'):
			from .Real import Real
			self._real = Real(self._core, self._base)
		return self._real

	def clone(self) -> 'Row':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Row(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
