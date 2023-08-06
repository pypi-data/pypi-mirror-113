from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sgamma:
	"""Sgamma commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sgamma", core, parent)

	@property
	def magnitude(self):
		"""magnitude commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_magnitude'):
			from .Magnitude import Magnitude
			self._magnitude = Magnitude(self._core, self._base)
		return self._magnitude

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	def delete(self) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:DELete \n
		Snippet: driver.source.correction.cset.data.sgamma.delete() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:DELete')

	def delete_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:CSET:DATA:SGAMma:DELete \n
		Snippet: driver.source.correction.cset.data.sgamma.delete_with_opc() \n
		No command help available \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:CSET:DATA:SGAMma:DELete')

	def clone(self) -> 'Sgamma':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sgamma(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
