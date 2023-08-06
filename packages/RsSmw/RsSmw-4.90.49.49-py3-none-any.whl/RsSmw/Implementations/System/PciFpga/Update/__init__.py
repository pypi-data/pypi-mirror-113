from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("update", core, parent)

	@property
	def needed(self):
		"""needed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_needed'):
			from .Needed import Needed
			self._needed = Needed(self._core, self._base)
		return self._needed

	def set(self) -> None:
		"""SCPI: SYSTem:PCIFpga:UPDate \n
		Snippet: driver.system.pciFpga.update.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:PCIFpga:UPDate')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:PCIFpga:UPDate \n
		Snippet: driver.system.pciFpga.update.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:PCIFpga:UPDate')

	def clone(self) -> 'Update':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Update(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
