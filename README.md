# harp.device.photodiode_board

**PhotodiodeBoard**: an RP2040-based [Harp](https://harp-tech.org/) device that samples two photodiode channels (ADC0 on GPIO27 and ADC1 on GPIO28, which are RP2040 ADC inputs 1 and 2) and streams timestamped readings to the host at 1 kHz.

* WhoAmI: `1412`
* Register definitions: [device.yml](./device.yml) (the authoritative register contract)
* Firmware build/flash instructions: [firmware/README.md](./firmware/README.md)
* Harp core library: [harp-tech/core.pico](https://github.com/harp-tech/core.pico), as a submodule pinned to commit `4654245`

## Registers
| Address | Name | Type | Access | Description |
|---|---|---|---|---|
| 32 | `ADC` | U8[2] | Event | Raw readings for ADC0 and ADC1: the top 8 bits of each 12-bit conversion (0-255). |

Events are sent at a fixed 1 kHz while the device is in Active mode (`OperationControl`) and replies are not muted. Start and stop the stream with Active/Standby. `ADC` can also be read on demand, which returns a fresh sample.

## Testing
With the device connected, run:
```
uv run software/test_adc_stream.py <port>
```
This checks identity, event rate and timestamp spacing, channel values, and that no events are sent in Standby. It uses the official [harp-tech/python](https://github.com/harp-tech/python) packages (`harp-serial`, `harp-device`).

# Github Release Conventions
Releases specify any vetted changes to the hardware or firmware.

Each release specifies:
* semantic versions of changed elements: hardware or firmware.
* SIPE part number (or part numbers if multiple are compatible)

Each hardware release includes:
* STEP file of the PCB (or link to corresponding CAD files) named with the SIPE part number
* schematic (PDF)
* Gerber files (with logos removed) of the PCBA
* Position files for component placement
* Bill-of-Materials for the PCBA

Each hardware release specifies:
* compatible SIPE part number(s)

> [!NOTE]
> SIPE part numbers only encode hardware semantic version major number, so multiple minor/patch hardware releases may point to the same SIPE part number.

> [!NOTE]
> It is possible for a project to have PCBA variants--possibly with very different functionality. In this case, reserve a hardware major version range (>100 suggested) for this variant and treat it as a distinct hardware release (i.e: with all corresponding included hardware files).


Each firmware release specifies:
* firmware semantic version
* compatible hardware (SIPE part number or part number range).

Each firmware release includes:
* compiled binary file (**\*.uf2**) of the firmware.

## Release Title
The release title is specified as follows:

`hw{hw major}.{hw minor}.{hw patch}-fw{fw major}.{fw minor}.{fw patch}`

If the release has firmware-only changes, you can drop the `hw*` section, and vice versa.

> [!NOTE]
> After Oct 2024, hardware major fields on all future releases will be equivalent to the major version number of the SIPE part number. See the [SIPE PCBA part numbering standard](https://alleninstitute.sharepoint.com/:w:/s/Instrumentation/EYsRN8q4jHJDmG5DNf-gaM0Bq418YMXollFxtB9d_NZ6pg?e=joLAvU) for more details.

The above field spec enables automation utilities to find the latest firmware version and automatically update compatible hardware. Since releases can include changes to some, but not other fields, unchanged fields are omitted. (i.e: firmware-only changes would be titled `fw{fw major}.{fw minor}.{fw patch}`.)

## Creating a New Release
1. Make a [git tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) based on the commit in the main branch that you'd like to create the release from. Use the naming convention specified in the [Release Title](#release-title) section.
2. Push the tag to Github.
3. From the repository's corresponding *Release* page, create a new release from the tag you just added. Give it the same title as the tag.
4. If the release includes new _firmware_, compile it locally, and upload a copy of the *.uf2* file as an attachment.
5. If the release includes new _hardware_, upload:
    1. the gerber files (zipped)
    2. the position files
    3. any manufacturing notes (component orientations)
    4. the bill-of-materials
    5. a PDF of the schematic.
