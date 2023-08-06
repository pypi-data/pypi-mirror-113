from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mpdu:
	"""Mpdu commands group definition. 5 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: MacPdu, default value after init: MacPdu.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mpdu", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_macPdu_get', 'repcap_macPdu_set', repcap.MacPdu.Nr1)

	def repcap_macPdu_set(self, enum_value: repcap.MacPdu) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MacPdu.Default
		Default value after init: MacPdu.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_macPdu_get(self) -> repcap.MacPdu:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def clone(self) -> 'Mpdu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mpdu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
