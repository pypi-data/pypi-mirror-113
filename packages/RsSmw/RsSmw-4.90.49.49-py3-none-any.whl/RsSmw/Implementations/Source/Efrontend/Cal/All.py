from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:CAL:ALL \n
		Snippet: driver.source.efrontend.cal.all.set() \n
		Starts all internal calibration routines to adjust the connected external frontend. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:CAL:ALL')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:CAL:ALL \n
		Snippet: driver.source.efrontend.cal.all.set_with_opc() \n
		Starts all internal calibration routines to adjust the connected external frontend. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:EFRontend:CAL:ALL')
