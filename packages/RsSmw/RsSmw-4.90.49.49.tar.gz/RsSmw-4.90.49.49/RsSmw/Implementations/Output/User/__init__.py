from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 3 total commands, 3 Sub-groups, 0 group commands
	Repeated Capability: UserIx, default value after init: UserIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_userIx_get', 'repcap_userIx_set', repcap.UserIx.Nr1)

	def repcap_userIx_set(self, enum_value: repcap.UserIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserIx.Default
		Default value after init: UserIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_userIx_get(self) -> repcap.UserIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Direction import Direction
			self._direction = Direction(self._core, self._base)
		return self._direction

	@property
	def signal(self):
		"""signal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import Signal
			self._signal = Signal(self._core, self._base)
		return self._signal

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
