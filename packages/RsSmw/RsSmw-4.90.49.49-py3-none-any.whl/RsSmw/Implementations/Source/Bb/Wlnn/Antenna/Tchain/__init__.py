from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tchain:
	"""Tchain commands group definition. 6 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: TransmissionChain, default value after init: TransmissionChain.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tchain", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_transmissionChain_get', 'repcap_transmissionChain_set', repcap.TransmissionChain.Nr1)

	def repcap_transmissionChain_set(self, enum_value: repcap.TransmissionChain) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TransmissionChain.Default
		Default value after init: TransmissionChain.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_transmissionChain_get(self) -> repcap.TransmissionChain:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def tx(self):
		"""tx commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tx'):
			from .Tx import Tx
			self._tx = Tx(self._core, self._base)
		return self._tx

	def clone(self) -> 'Tchain':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tchain(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
