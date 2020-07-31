# Fork for PlatformIO nRF52840 with Arduino and Zigbee Support

This project is part of multiple git repositories for an Android framework with Zigbee support. The aim is to include the support in the fantastic work of Adafruit and all other contrubutors.

- [platform-nordicnrf52](https://github.com/csowada/platform-nordicnrf52)
- [Adafruit_nRF52_Arduino](https://github.com/csowada/Adafruit_nRF52_Arduino)
- [Adafruit_TinyUSB_ArduinoCore](https://github.com/csowada/Adafruit_TinyUSB_ArduinoCore)

### Known Limitations

- Not working with Arduino IDE
- No clue if TinyUSB is working
- Bootloader/MBR is untested
- Some Serial stuff is disabled, see ``Uart.c`` file.
- SOFTDEVICE as in Adafruits version is not working
- Only nRF52840-DK is supported/tested yet

### Modifications to ``platform-nordicnrf52``

- Add clone of Adafruit ``adafruit.py`` builder with NO-SD support
- Add build scripts for additional features like Zigbee
- Add new ``nrf52840_dk_zb`` board
- Add ``xxx`` Zigbee bulb example

### Modifications to ``Adafruit_nRF52_Arduino``

- Backport ``nrfx`` from 2.1.0 to 1.8.0 from Zigbee SDK 1.4.1
- Change RTC1 to RTC0 for FreeRTOS
- Fix some functions for NON-SOFTDEVICE
- Remove from lines for Serial
- Add required Zigbee stuff and libraries

### Modifications to ``Adafruit_TinyUSB_ArduinoCore``

- Backport some function calls due to ``nrfx`` backport

## Usage

Add the forked platform etc. to your ``platformio.ini`` file. This works without any downloads, PlatformIO will do that for you.

```ini
platform = https://github.com/csowada/platform-nordicnrf52.git
platform_packages = framework-arduinonordicnrf52-zb-sdk @ https://github.com/csowada/Adafruit_nRF52_Arduino.git

board = nrf52840_dk_zb
framework = arduino

custom_enable_features = 
  ; Add Zigbee support to the core build
  ZIGBEE

build_flags =
  ; Add SDK relevant flags here
  -DZIGBEE_CHANNEL=11
  -DZB_TRACE_LEVEL=0
  -DZB_TRACE_MASK=0
  -DUSE_APP_CONFIG
  -DAPP_TIMER_V2
  -DAPP_TIMER_V2_RTC1_ENABLED
  -DCONFIG_GPIO_AS_PINRESET
  -DENABLE_FEM
  -DFLOAT_ABI_HARD
```

To run this framework, add an ``config`` folder to your project to place the ``sdk_config.h`` file there.

## Examples

See the ``arduino-zigbee-bulb`` in [Adafruit_nRF52_Arduino](https://github.com/csowada/Adafruit_nRF52_Arduino).



***

# Nordic nRF52: development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://github.com/platformio/platform-nordicnrf52/workflows/Examples/badge.svg)](https://github.com/platformio/platform-nordicnrf52/actions)

The nRF52 Series are built for speed to carry out increasingly complex tasks in the shortest possible time and return to sleep, conserving precious battery power. They have a Cortex-M4F processor and are the most capable Bluetooth Smart SoCs on the market.

* [Home](http://platformio.org/platforms/nordicnrf52) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/nordicnrf52.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = nordicnrf52
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-nordicnrf52.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/nordicnrf52.html).
