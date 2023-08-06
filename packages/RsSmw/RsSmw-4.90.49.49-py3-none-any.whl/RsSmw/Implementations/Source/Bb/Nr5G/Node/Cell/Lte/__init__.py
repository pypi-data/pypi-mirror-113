from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lte:
	"""Lte commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lte", core, parent)

	@property
	def npat(self):
		"""npat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npat'):
			from .Npat import Npat
			self._npat = Npat(self._core, self._base)
		return self._npat

	@property
	def patt(self):
		"""patt commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_patt'):
			from .Patt import Patt
			self._patt = Patt(self._core, self._base)
		return self._patt

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._base)
		return self._state

	def clone(self) -> 'Lte':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lte(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
