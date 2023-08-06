Rohde & Schwarz SMW200A Vector Signal Generator RsSmw instrument driver.

Supported instruments: SMW200A, SMM100A, SMBV100B

The package is hosted here: https://pypi.org/project/RsSmw/

Documentation: https://rohde-schwarz.github.io/RsSmw_PythonDocumentation/

Examples: https://github.com/Rohde-Schwarz/Examples/tree/main/SignalGenerators/Python/RsSmw_ScpiPackage

----------------------------------------------------------------------------------

Release Notes:

Latest release notes summary: Update for SMW FW 4.90.049, added Logger

Version 4.90.49.49

- Update for SMW FW 4.90.049
- Added Logger interface
- Improved documentation

Version 4.80.2.45

- Fixed several misspelled arguments and command headers

Version 4.80.2.42

- Complete rework of the Repeated capabilities. Before, the driver used extensively the RepCaps Channel, Stream, Subframe, User, Group. Now, they have more fitting names, and also proper ranges and default values.
All the repcaps ending with Null have ranges starting with 0. 0 is also their default value.
For example, ChannelNull starts from 0, while Channel starts from 1. Since this is a breaking change, please make sure your code written in the previous version of the driver is compatible with this new version.
This change was necessary in order to assure all the possible settings.

Version 4.80.1.31

- Fixed NR5G Repeated Capabilities

Version 4.80.1.30

- Added new supported instrument: SMM100A

Version 4.80.0.29

- Added Documentation
- Added method RsSmw.list_resources()

Version 4.80.0.25

- Added arb_files interface

Version 4.80.0.24

- Included GNSS subsystem

Version 4.80.0.19

- Fixed several enum names

Version 4.80.0.17

- First released version