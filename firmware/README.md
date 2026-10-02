There are two sets of instructions, one for [Windows](#windows-setup) and one for [Linux](#linux-setup).

> [!IMPORTANT]
> Requirements:
> * pico-sdk **2.x**. Verified with 2.2.0, which the VS Code Pico extension installs to `~/.pico-sdk/sdk/2.2.0`.
> * arm-none-eabi-gcc **11 or newer**, because harp core.pico needs C++23. Verified with 14.2.
> * The `harp.core.rp2040` submodule, pinned to [harp-tech/core.pico](https://github.com/harp-tech/core.pico) commit `4654245`. Run `git submodule update --init` after cloning.
>
> The build also hashes `../device.yml` into the firmware (the `interface_hash` in the core R_VERSION register). Rebuild after any change to `device.yml`.


# Windows Setup

Windows has two sub-options for developing:
* Option A: use Visual Studio Code (easy way)
* Option B: develop with any IDE and compile from the command line.

> [!NOTE]
> For Option B, simply install [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install), and then follow the directions in the [Linux](#linux-setup) section of this guide. The rest of this section covers Option A.
  
## Pre-requisites
1. Install [Visual Studio Code](https://code.visualstudio.com/).
2. Install the [Pico Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico)

## Project Setup
In Visual Studio, click on the Pico icon that appears after installing the Pico Extension. Select _Import Project_ and import the _firmware_ folder of this repository.
Choose the default options.

## Compiling the Firmware
Click the _compile_ button at the corner of the screen. When the compilation finishes, you're ready to [flash the firmware](#flashing-the-firmware).

# Linux Setup

## Pre-requisites

You will need CMake, make, and the gcc-arm-embedded toolchain.

On Linux, install the following:
```bash
sudo apt install cmake python3 build-essential gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib
```

### Install Submodules
This project uses the Harp [core.pico](https://github.com/harp-tech/core.pico) library as a submodule, pinned to a specific commit. Upstream changes its API without notice, so upgrade the pin on purpose.
Install it with:
````
git submodule update --init
````

### Install Pico SDK
This project uses the [Pico SDK](https://github.com/raspberrypi/pico-sdk/tree/master).
The SDK needs to be downloaded and installed to a known folder on your PC.
Note that the PICO SDK also contains submodules (including TinyUSB), so you must ensure that they are also fetched with:
````
git clone https://github.com/raspberrypi/pico-sdk.git
git submodule update --init --recursive
````

### Point to Pico SDK
Optional: define the `PICO_SDK_PATH` environment variable to point to the location where the pico-sdk was downloaded. i.e:
````
PICO_SDK_PATH=/home/username/projects/pico-sdk
````
On Linux, you can define it in your `.bashrc` file.
On Windows, you can define it via System Properties ([tutorial](https://www.computerhope.com/issues/ch000549.htm)).

Confirm that the environment variable is applied to your system by opening a terminal (Powershell on Windows) and
entering (with the `$` sign)
```bash
$PICO_SDK_PATH
```
to confirm that the path was defined correctly.
(Windows may require a restart for the environment variable to take effect.)

## Compiling the Firmware

### With the Visual Studio Code Extension
Using the Pico extension, import the *firmware* folder with the default options.

Click the compile button.

### Without an IDE
From within this folder, create a new folder called *build*, enter it, and invoke cmake with:
````
mkdir build
cd build
cmake ..
````
If you did not define the `PICO_SDK_PATH` as an environment variable, you must pass it in here like so:
````
mkdir build
cd build
cmake -DPICO_SDK_PATH=/path/to/pico-sdk ..
````
After this point, you can invoke the auto-generated Makefile with `make`

## Flashing the Firmware
Press-and-hold the Pico's BOOTSEL button and power it up (i.e: plug it into usb).
At this point you do one of the following:
* drag-and-drop the created **\*.uf2** file into the mass storage device that appears on your pc.
* flash with [picotool](https://github.com/raspberrypi/picotool)

To reboot a running device into the bootloader without pressing BOOTSEL, write `UPDATE_FIRMWARE` to the core `ResetDevice` register. The device then appears as a mass storage device and you can copy the **\*.uf2** file onto it.

# References
* [YouTube: How to Set Up Visual Studio Code to Program the Pi Pico (Windows)](https://www.youtube.com/watch?v=mUF9xjDtFfY&t=55s)
* [Pico SDK: Unix Command Line](https://github.com/raspberrypi/pico-sdk?tab=readme-ov-file#unix-command-line) Setup
