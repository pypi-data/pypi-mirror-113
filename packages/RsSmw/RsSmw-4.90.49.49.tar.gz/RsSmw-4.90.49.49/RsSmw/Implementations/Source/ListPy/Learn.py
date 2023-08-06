from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Learn:
	"""Learn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("learn", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:LIST:LEARn \n
		Snippet: driver.source.listPy.learn.set() \n
		Learns the selected list to determine the hardware setting for all list entries. The results are saved with the list. See
		also 'Learn List Mode Data list processing mode'. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:LIST:LEARn')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:LIST:LEARn \n
		Snippet: driver.source.listPy.learn.set_with_opc() \n
		Learns the selected list to determine the hardware setting for all list entries. The results are saved with the list. See
		also 'Learn List Mode Data list processing mode'. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:LIST:LEARn')
