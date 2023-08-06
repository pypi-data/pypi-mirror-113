from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: NoisePoint, default value after init: NoisePoint.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_noisePoint_get', 'repcap_noisePoint_set', repcap.NoisePoint.Nr1)

	def repcap_noisePoint_set(self, enum_value: repcap.NoisePoint) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to NoisePoint.Default
		Default value after init: NoisePoint.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_noisePoint_get(self) -> repcap.NoisePoint:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, phase_noise_freq: int, noisePoint=repcap.NoisePoint.Default) -> None:
		"""SCPI: [SOURce<HW>]:NOISe:PHASenoise:FREQuency<CH> \n
		Snippet: driver.source.noise.phasenoise.frequency.set(phase_noise_freq = 1, noisePoint = repcap.NoisePoint.Default) \n
		Sets the frequency value of the points, where the points are designated by the suffix <ch>. \n
			:param phase_noise_freq: integer Range: 10 to 10E6
			:param noisePoint: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')"""
		param = Conversions.decimal_value_to_str(phase_noise_freq)
		noisePoint_cmd_val = self._base.get_repcap_cmd_value(noisePoint, repcap.NoisePoint)
		self._core.io.write(f'SOURce<HwInstance>:NOISe:PHASenoise:FREQuency{noisePoint_cmd_val} {param}')

	def get(self, noisePoint=repcap.NoisePoint.Default) -> int:
		"""SCPI: [SOURce<HW>]:NOISe:PHASenoise:FREQuency<CH> \n
		Snippet: value: int = driver.source.noise.phasenoise.frequency.get(noisePoint = repcap.NoisePoint.Default) \n
		Sets the frequency value of the points, where the points are designated by the suffix <ch>. \n
			:param noisePoint: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
			:return: phase_noise_freq: integer Range: 10 to 10E6"""
		noisePoint_cmd_val = self._base.get_repcap_cmd_value(noisePoint, repcap.NoisePoint)
		response = self._core.io.query_str(f'SOURce<HwInstance>:NOISe:PHASenoise:FREQuency{noisePoint_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
