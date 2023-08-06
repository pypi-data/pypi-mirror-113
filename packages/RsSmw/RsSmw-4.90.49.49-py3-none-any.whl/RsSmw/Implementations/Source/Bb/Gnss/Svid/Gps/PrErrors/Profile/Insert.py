from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:PRERrors:PROFile<GR>:INSert \n
		Snippet: driver.source.bb.gnss.svid.gps.prErrors.profile.insert.set(satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Inserts a row befor the selected pseudorange error. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._base.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:PRERrors:PROFile{index_cmd_val}:INSert')

	def set_with_opc(self, satelliteSvid=repcap.SatelliteSvid.Default, index=repcap.Index.Default) -> None:
		satelliteSvid_cmd_val = self._base.get_repcap_cmd_value(satelliteSvid, repcap.SatelliteSvid)
		index_cmd_val = self._base.get_repcap_cmd_value(index, repcap.Index)
		"""SCPI: [SOURce<HW>]:BB:GNSS:SVID<CH>:GPS:PRERrors:PROFile<GR>:INSert \n
		Snippet: driver.source.bb.gnss.svid.gps.prErrors.profile.insert.set_with_opc(satelliteSvid = repcap.SatelliteSvid.Default, index = repcap.Index.Default) \n
		Inserts a row befor the selected pseudorange error. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param satelliteSvid: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:SVID{satelliteSvid_cmd_val}:GPS:PRERrors:PROFile{index_cmd_val}:INSert')
