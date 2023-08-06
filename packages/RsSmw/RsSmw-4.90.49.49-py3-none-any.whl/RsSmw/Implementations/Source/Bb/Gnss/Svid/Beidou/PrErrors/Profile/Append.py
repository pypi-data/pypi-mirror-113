from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Append:
	"""Append commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("append", core, parent)

	def set(self, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou:PRERrors:PROFile:APPend \n
		Snippet: driver.source.bb.gnss.svid.beidou.prErrors.profile.append.set(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Appends a row in the profile table. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')"""
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:BEIDou:PRERrors:PROFile:APPend')

	def set_with_opc(self, satelliteSvid=repcap.SatelliteSvid.Default) -> None:
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:BEIDou:PRERrors:PROFile:APPend \n
		Snippet: driver.source.bb.gnss.svid.beidou.prErrors.profile.append.set_with_opc(satelliteSvid = repcap.SatelliteSvid.Default) \n
		Appends a row in the profile table. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:BEIDou:PRERrors:PROFile:APPend')
