from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort:REMove:ALL \n
		Snippet: driver.source.bb.gnss.atmospheric.ionospheric.mops.importPy.remove.all.set() \n
		Remove all or one particular file at the n-th position from an import file list. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort:REMove:ALL')

	def set_with_opc(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort:REMove:ALL \n
		Snippet: driver.source.bb.gnss.atmospheric.ionospheric.mops.importPy.remove.all.set_with_opc() \n
		Remove all or one particular file at the n-th position from an import file list. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort:REMove:ALL')
