from os import listdir
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

import re

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
variant = board.get("build.variant")

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinonordicnrf52-zb-sdk")
assert isdir(FRAMEWORK_DIR)

ZB_SDK_DIR = join(FRAMEWORK_DIR, "cores", "zigbee-sdk")
assert isdir(ZB_SDK_DIR)

config = configparser.ConfigParser()
config.read("platformio.ini")

enable_features = ""

if config.has_option("env:" + env["PIOENV"], "custom_enable_features"):
    enable_features = config.get("env:" + env["PIOENV"], "custom_enable_features", [])



useZigbee = False

# not used, just to store the minimal c files
useNrfxCore = False


print("EXTRA FEATURES: ")

if "ZIGBEE" in enable_features:
    print " - ZIGBEE"
    useZigbee = True

if "HYPERLOOP" in enable_features:
    print " - HYPERLOOP"

if "NRFX_CORE" in enable_features:
    print " - NRFX_CORE"
    useNrfxCore = True


libs = []

env.Append(
    CPPPATH=[
        join(ZB_SDK_DIR),

        join(ZB_SDK_DIR, "external", "fprintf"),

        join(ZB_SDK_DIR, "integration", "nrfx"),
        join(ZB_SDK_DIR, "integration", "nrfx", "legacy"),

        join(ZB_SDK_DIR, "components"),
        join(ZB_SDK_DIR, "components", "boards"),
        join(ZB_SDK_DIR, "components", "softdevice", "common"),

        join(ZB_SDK_DIR, "components", "libraries", "assert"),
        join(ZB_SDK_DIR, "components", "libraries", "atomic"),
        join(ZB_SDK_DIR, "components", "libraries", "atomic_fifo"),
        join(ZB_SDK_DIR, "components", "libraries", "balloc"),
        join(ZB_SDK_DIR, "components", "libraries", "bsp"),
        join(ZB_SDK_DIR, "components", "libraries", "button"),
        join(ZB_SDK_DIR, "components", "libraries", "delay"),
        join(ZB_SDK_DIR, "components", "libraries", "experimental_section_vars"),
        join(ZB_SDK_DIR, "components", "libraries", "fstorage"),
        join(ZB_SDK_DIR, "components", "libraries", "gpiote"),
        join(ZB_SDK_DIR, "components", "libraries", "log"),
        join(ZB_SDK_DIR, "components", "libraries", "log", "src"),
        join(ZB_SDK_DIR, "components", "libraries", "memobj"),
        join(ZB_SDK_DIR, "components", "libraries", "mutex"),
        join(ZB_SDK_DIR, "components", "libraries", "pwm"),
        join(ZB_SDK_DIR, "components", "libraries", "pwr_mgmt"),
        join(ZB_SDK_DIR, "components", "libraries", "queue"),
        join(ZB_SDK_DIR, "components", "libraries", "ringbuf"),
        join(ZB_SDK_DIR, "components", "libraries", "scheduler"),
        join(ZB_SDK_DIR, "components", "libraries", "sortlist"),
        join(ZB_SDK_DIR, "components", "libraries", "strerror"),
        join(ZB_SDK_DIR, "components", "libraries", "timer"),
        join(ZB_SDK_DIR, "components", "libraries", "util"),
    ]
)

# Add the ZIGBEE stuff
if useZigbee:

    env.Append(
        CPPPATH=[
            join(ZB_SDK_DIR, "components", "zigbee","common"),

            join(ZB_SDK_DIR, "external", "nRF-IEEE-802.15.4-radio-driver", "src"),
            join(ZB_SDK_DIR, "external", "nRF-IEEE-802.15.4-radio-driver", "src", "fem"),
            join(ZB_SDK_DIR, "external", "nRF-IEEE-802.15.4-radio-driver", "src", "fem", "three_pin_gpio"),

            join(ZB_SDK_DIR, "external", "zboss", "include"),
            join(ZB_SDK_DIR, "external", "zboss", "include", "ha"),
            join(ZB_SDK_DIR, "external", "zboss", "include", "osif"),
            join(ZB_SDK_DIR, "external", "zboss", "include", "zcl"),
            join(ZB_SDK_DIR, "external", "zboss", "osif"),
            join(ZB_SDK_DIR, "external", "zboss", "addons"),
            join(ZB_SDK_DIR, "external", "zboss", "zb_error"),
        ]
    )

    env.Append(
        LIBPATH = [
            join(ZB_SDK_DIR, "external", "zboss", "lib", "gcc"),
            join(ZB_SDK_DIR, "external", "zboss", "lib", "gcc", "nrf52840")
        ],
    )

    libs.append([
        "zboss",
        "nrf_radio_driver",
    ])

    libs.append(
        env.StaticLibrary(
            env.subst(join("$BUILD_DIR", "FrameworkSDK-ZB")), [
                join(ZB_SDK_DIR, "external", "zboss","zb_error", "zb_error_to_string.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_common.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_nrf_logger.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_nvram.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_sdk_config_deps.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_timer.c"),
                join(ZB_SDK_DIR, "external", "zboss","osif", "zb_nrf52_transceiver.c"),
                join(ZB_SDK_DIR, "external", "zboss","addons", "zcl", "zb_zcl_common_addons.c"),
                join(ZB_SDK_DIR, "external", "zboss","addons", "zcl", "zb_zcl_ota_upgrade_addons.c"),
                join(ZB_SDK_DIR, "components", "zigbee","common", "zigbee_helpers.c"),
                join(ZB_SDK_DIR, "components", "zigbee","common", "zigbee_logger_eprxzcl.c"),
            ]
        )
    )

libs.append(
    env.StaticLibrary(
        env.subst(join("$BUILD_DIR", "FrameworkSDK")), [

            join(ZB_SDK_DIR, "integration", "nrfx", "legacy", "nrf_drv_clock.c"),
            join(ZB_SDK_DIR, "integration", "nrfx", "legacy", "nrf_drv_ppi.c"),
            join(ZB_SDK_DIR, "integration", "nrfx", "legacy", "nrf_drv_rng.c"),
            join(ZB_SDK_DIR, "integration", "nrfx", "legacy", "nrf_drv_uart.c"),

# BASIC BLINKY
            join(ZB_SDK_DIR, "components", "libraries","log", "src", "nrf_log_frontend.c"),
            join(ZB_SDK_DIR, "components", "libraries","log", "src", "nrf_log_str_formatter.c"),
            join(ZB_SDK_DIR, "components", "boards","boards.c"),
            join(ZB_SDK_DIR, "components", "libraries","util", "app_error.c"),
            join(ZB_SDK_DIR, "components", "libraries","util", "app_error_handler_gcc.c"),
            join(ZB_SDK_DIR, "components", "libraries","util", "app_error_weak.c"),
            join(ZB_SDK_DIR, "components", "libraries","util", "app_util_platform.c"),
            join(ZB_SDK_DIR, "components", "libraries","util", "nrf_assert.c"),
            join(ZB_SDK_DIR, "components", "libraries","atomic", "nrf_atomic.c"),
            join(ZB_SDK_DIR, "components", "libraries","balloc", "nrf_balloc.c"),
            join(ZB_SDK_DIR, "external", "fprintf", "nrf_fprintf.c"),
            join(ZB_SDK_DIR, "external", "fprintf", "nrf_fprintf_format.c"),
            join(ZB_SDK_DIR, "components", "libraries","memobj", "nrf_memobj.c"),
            join(ZB_SDK_DIR, "components", "libraries","ringbuf", "nrf_ringbuf.c"),
            join(ZB_SDK_DIR, "components", "libraries","strerror", "nrf_strerror.c"),
# ZIGBEE

            
            join(ZB_SDK_DIR, "components", "libraries","bsp", "bsp.c"),

            join(ZB_SDK_DIR, "components", "libraries","timer", "app_timer.c"),
            join(ZB_SDK_DIR, "components", "libraries","sortlist", "nrf_sortlist.c"),
            join(ZB_SDK_DIR, "components", "libraries","button", "app_button.c"),
            
            
            join(ZB_SDK_DIR, "components", "libraries","gpiote", "app_gpiote.c"),
            join(ZB_SDK_DIR, "components", "libraries","pwm", "app_pwm.c"),
            join(ZB_SDK_DIR, "components", "libraries","scheduler", "app_scheduler.c"),
            join(ZB_SDK_DIR, "components", "libraries","timer", "app_timer2.c"),

            join(ZB_SDK_DIR, "components", "libraries","assert", "assert.c"),
            join(ZB_SDK_DIR, "components", "libraries","timer", "drv_rtc.c"),
            
            join(ZB_SDK_DIR, "components", "libraries","atomic_fifo", "nrf_atfifo.c"),

            join(ZB_SDK_DIR, "components", "libraries","log", "src", "nrf_log_backend_serial.c"),
            join(ZB_SDK_DIR, "components", "libraries","log", "src", "nrf_log_backend_uart.c"),
            join(ZB_SDK_DIR, "components", "libraries","log", "src", "nrf_log_default_backends.c"),

            join(ZB_SDK_DIR, "components", "libraries","fstorage", "nrf_fstorage.c"),
            join(ZB_SDK_DIR, "components", "libraries","fstorage", "nrf_fstorage_nvmc.c"),
            
            join(ZB_SDK_DIR, "components", "libraries","pwr_mgmt", "nrf_pwr_mgmt.c"),
            join(ZB_SDK_DIR, "components", "libraries","queue", "nrf_queue.c"),
            
            join(ZB_SDK_DIR, "components", "libraries","experimental_section_vars", "nrf_section_iter.c"),
            

            # # from nrfx
            join(ZB_SDK_DIR, "components", "libraries","strerror", "nrf_strerror.c"),
        ]
    )
)

if useNrfxCore:
    libs.append(
        env.StaticLibrary(
            env.subst(join("$BUILD_DIR", "FrameworkNRFXCore")), [
                # Add nrfx core module
                join(NORDIC_DIR, "nrfx","mdk", "gcc_startup_nrf52840.S"),
                join(NORDIC_DIR, "nrfx","mdk", "system_nrf52840.c"),

                # compile non SOFTDEVICE
                join(NORDIC_DIR, "components", "drivers_nrf","nrf_soc_nosd", "nrf_nvic.c"),
                join(NORDIC_DIR, "components", "drivers_nrf","nrf_soc_nosd", "nrf_soc.c"),

                join(NORDIC_DIR, "nrfx","hal", "nrf_ecb.c"),
                join(NORDIC_DIR, "nrfx","hal", "nrf_nvmc.c"),

                join(NORDIC_DIR, "nrfx","soc", "nrfx_atomic.c"),

                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_clock.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_gpiote.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_ppi.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "prs", "nrfx_prs.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_pwm.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_rng.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_systick.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_timer.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_uart.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_uarte.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_timer.c"),

                # for TinyUSB and Arduino Setup?
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_power.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_qspi.c"),
                join(NORDIC_DIR, "nrfx","drivers", "src", "nrfx_spim.c"),
            ]
        )
    )

# env.Prepend(LIBS=libs)
env.Append(LIBS=libs)
