from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Patt:
	"""Patt commands group definition. 4 total commands, 4 Sub-groups, 0 group commands
	Repeated Capability: PatternNull, default value after init: PatternNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("patt", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_patternNull_get', 'repcap_patternNull_set', repcap.PatternNull.Nr0)

	def repcap_patternNull_set(self, enum_value: repcap.PatternNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to PatternNull.Default
		Default value after init: PatternNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_patternNull_get(self) -> repcap.PatternNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def cbw(self):
		"""cbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbw'):
			from .Cbw import Cbw
			self._cbw = Cbw(self._core, self._base)
		return self._cbw

	@property
	def nap(self):
		"""nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nap'):
			from .Nap import Nap
			self._nap = Nap(self._core, self._base)
		return self._nap

	@property
	def pointA(self):
		"""pointA commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pointA'):
			from .PointA import PointA
			self._pointA = PointA(self._core, self._base)
		return self._pointA

	@property
	def vshift(self):
		"""vshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vshift'):
			from .Vshift import Vshift
			self._vshift = Vshift(self._core, self._base)
		return self._vshift

	def clone(self) -> 'Patt':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Patt(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
