from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alpha:
	"""Alpha commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: AlphaNull, default value after init: AlphaNull.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alpha", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_alphaNull_get', 'repcap_alphaNull_set', repcap.AlphaNull.Nr0)

	def repcap_alphaNull_set(self, enum_value: repcap.AlphaNull) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AlphaNull.Default
		Default value after init: AlphaNull.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_alphaNull_get(self) -> repcap.AlphaNull:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def clone(self) -> 'Alpha':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alpha(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
