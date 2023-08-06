from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:REGenerator:OBJect:COPY:EXECute \n
		Snippet: driver.source.regenerator.object.copy.execute.set() \n
		Copies the settings of one selected object to the other one. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:REGenerator:OBJect:COPY:EXECute')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:REGenerator:OBJect:COPY:EXECute \n
		Snippet: driver.source.regenerator.object.copy.execute.set_with_opc() \n
		Copies the settings of one selected object to the other one. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:REGenerator:OBJect:COPY:EXECute')
