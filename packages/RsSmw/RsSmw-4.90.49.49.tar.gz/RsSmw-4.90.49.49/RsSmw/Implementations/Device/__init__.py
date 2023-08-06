from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("device", core, parent)

	@property
	def settings(self):
		"""settings commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_settings'):
			from .Settings import Settings
			self._settings = Settings(self._core, self._base)
		return self._settings

	def get_idn(self) -> str:
		"""SCPI: DEVice<HW>:IDN \n
		Snippet: value: str = driver.device.get_idn() \n
		No command help available \n
			:return: idn: No help available
		"""
		response = self._core.io.query_str('DEVice<HwInstance>:IDN?')
		return trim_str_response(response)

	def get_options(self) -> str:
		"""SCPI: DEVice<HW>:OPTions \n
		Snippet: value: str = driver.device.get_options() \n
		No command help available \n
			:return: opt: No help available
		"""
		response = self._core.io.query_str('DEVice<HwInstance>:OPTions?')
		return trim_str_response(response)

	def preset(self) -> None:
		"""SCPI: DEVice:PRESet \n
		Snippet: driver.device.preset() \n
		Presets all parameters which are not related to the signal path, including the LF generator. \n
		"""
		self._core.io.write(f'DEVice:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: DEVice:PRESet \n
		Snippet: driver.device.preset_with_opc() \n
		Presets all parameters which are not related to the signal path, including the LF generator. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DEVice:PRESet')

	# noinspection PyTypeChecker
	def get_rc_state(self) -> enums.SigmaGuiDeviceAccessibility:
		"""SCPI: DEVice<HW>:RCSTate \n
		Snippet: value: enums.SigmaGuiDeviceAccessibility = driver.device.get_rc_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('DEVice<HwInstance>:RCSTate?')
		return Conversions.str_to_scalar_enum(response, enums.SigmaGuiDeviceAccessibility)

	def clone(self) -> 'Device':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Device(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
