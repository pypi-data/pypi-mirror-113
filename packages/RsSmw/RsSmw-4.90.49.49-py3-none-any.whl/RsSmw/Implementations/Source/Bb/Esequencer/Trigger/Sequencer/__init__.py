from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequencer:
	"""Sequencer commands group definition. 5 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Sequencer, default value after init: Sequencer.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequencer", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_sequencer_get', 'repcap_sequencer_set', repcap.Sequencer.Nr1)

	def repcap_sequencer_set(self, enum_value: repcap.Sequencer) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Sequencer.Default
		Default value after init: Sequencer.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_sequencer_get(self) -> repcap.Sequencer:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def output(self):
		"""output commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def clone(self) -> 'Sequencer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sequencer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
