from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	@property
	def moving(self):
		"""moving commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_moving'):
			from .Moving import Moving
			self._moving = Moving(self._core, self._base)
		return self._moving

	def clone(self) -> 'All':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = All(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
