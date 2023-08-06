from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfg:
	"""Cfg commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: ConfigurationNull, default value after init: ConfigurationNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfg", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_configurationNull_get', 'repcap_configurationNull_set', repcap.ConfigurationNull.Nr0)

	def repcap_configurationNull_set(self, enum_value: repcap.ConfigurationNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ConfigurationNull.Default
		Default value after init: ConfigurationNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_configurationNull_get(self) -> repcap.ConfigurationNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def perd(self):
		"""perd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perd'):
			from .Perd import Perd
			self._perd = Perd(self._core, self._base)
		return self._perd

	@property
	def rep(self):
		"""rep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rep'):
			from .Rep import Rep
			self._rep = Rep(self._core, self._base)
		return self._rep

	@property
	def scof(self):
		"""scof commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scof'):
			from .Scof import Scof
			self._scof = Scof(self._core, self._base)
		return self._scof

	@property
	def sttm(self):
		"""sttm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sttm'):
			from .Sttm import Sttm
			self._sttm = Sttm(self._core, self._base)
		return self._sttm

	@property
	def subc(self):
		"""subc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subc'):
			from .Subc import Subc
			self._subc = Subc(self._core, self._base)
		return self._subc

	def clone(self) -> 'Cfg':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cfg(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
