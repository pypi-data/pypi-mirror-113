from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 42 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: ChannelNull, default value after init: ChannelNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channelNull_get', 'repcap_channelNull_set', repcap.ChannelNull.Nr0)

	def repcap_channelNull_set(self, enum_value: repcap.ChannelNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelNull.Default
		Default value after init: ChannelNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channelNull_get(self) -> repcap.ChannelNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def dpch(self):
		"""dpch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpch'):
			from .Dpch import Dpch
			self._dpch = Dpch(self._core, self._base)
		return self._dpch

	@property
	def hsdpa(self):
		"""hsdpa commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsdpa'):
			from .Hsdpa import Hsdpa
			self._hsdpa = Hsdpa(self._core, self._base)
		return self._hsdpa

	def clone(self) -> 'Channel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Channel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
