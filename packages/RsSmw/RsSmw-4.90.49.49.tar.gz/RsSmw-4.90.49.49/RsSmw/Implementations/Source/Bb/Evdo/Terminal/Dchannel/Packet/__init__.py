from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Packet:
	"""Packet commands group definition. 13 total commands, 11 Sub-groups, 0 group commands
	Repeated Capability: Packet, default value after init: Packet.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("packet", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_packet_get', 'repcap_packet_set', repcap.Packet.Nr1)

	def repcap_packet_set(self, enum_value: repcap.Packet) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Packet.Default
		Default value after init: Packet.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_packet_get(self) -> repcap.Packet:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ccoding(self):
		"""ccoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccoding'):
			from .Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def drate(self):
		"""drate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_drate'):
			from .Drate import Drate
			self._drate = Drate(self._core, self._base)
		return self._drate

	@property
	def fcs(self):
		"""fcs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcs'):
			from .Fcs import Fcs
			self._fcs = Fcs(self._core, self._base)
		return self._fcs

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def infinite(self):
		"""infinite commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_infinite'):
			from .Infinite import Infinite
			self._infinite = Infinite(self._core, self._base)
		return self._infinite

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def psize(self):
		"""psize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psize'):
			from .Psize import Psize
			self._psize = Psize(self._core, self._base)
		return self._psize

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def subPackets(self):
		"""subPackets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_subPackets'):
			from .SubPackets import SubPackets
			self._subPackets = SubPackets(self._core, self._base)
		return self._subPackets

	def clone(self) -> 'Packet':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Packet(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
