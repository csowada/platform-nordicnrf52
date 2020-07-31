#ifndef APP_CONFIG_H
#define APP_CONFIG_H

//==========================================================
// <o> APP_BULB_USE_WS2812_LED_CHAIN - Configures the application to use the WS2812 LED chain as bulb (for example, the Adafruit NeoPixel Shield (for Arduino)). 
#ifndef APP_BULB_USE_WS2812_LED_CHAIN
#define APP_BULB_USE_WS2812_LED_CHAIN 0
#endif

// </h> 
//==========================================================

// <h> zigbee_stack - ZBOSS Zigbee stack

//==========================================================
// <o> ZIGBEE_CHANNEL - 802.15.4 channel used by Zigbee  <11-26> 


// <i> 802.15.4 channel used by Zigbee. Defaults to 16.

#ifndef ZIGBEE_CHANNEL
#define ZIGBEE_CHANNEL 11
#endif

// <o> ZIGBEE_TRACE_LEVEL - Trace level of Zigbee stack logs.  <0-4> 


// <i> Trace level of Zigbee stack binary logs. Possible values: 0 - disable, 1 - error, 2 - warning, 3 - info, 4 - debug. Disabled by default.

#ifndef ZIGBEE_TRACE_LEVEL
#define ZIGBEE_TRACE_LEVEL 3
#endif

// <o> NRF_LOG_BACKEND_UART_BAUDRATE  - Default Baudrate
 
// <323584=> 1200 baud 
// <643072=> 2400 baud 
// <1290240=> 4800 baud 
// <2576384=> 9600 baud 
// <3862528=> 14400 baud 
// <5152768=> 19200 baud 
// <7716864=> 28800 baud 
// <10289152=> 38400 baud 
// <15400960=> 57600 baud 
// <20615168=> 76800 baud 
// <30801920=> 115200 baud 
// <61865984=> 230400 baud 
// <67108864=> 250000 baud 
// <121634816=> 460800 baud 
// <251658240=> 921600 baud 
// <268435456=> 1000000 baud 

#ifndef NRF_LOG_BACKEND_UART_BAUDRATE
#define NRF_LOG_BACKEND_UART_BAUDRATE 30801920
#endif


// # TinyUSB ?

#define NRFX_POWER_ENABLED              1
#define NRFX_POWER_CONFIG_IRQ_PRIORITY  6
// #define NRFX_CLOCK_CONFIG_IRQ_PRIORITY 6

// Setup for Arduino ?!
#define NRFX_SPIM_ENABLED            1
#define NRFX_SPIM_MISO_PULL_CFG      1 // pulldown
#define NRFX_SPIM_EXTENDED_ENABLED   0

#define NRFX_SPIM0_ENABLED           0 // used as I2C
#define NRFX_SPIM1_ENABLED           0 // used as I2C
#define NRFX_SPIM2_ENABLED           1

#ifdef NRF52840_XXAA
  #define NRFX_QSPI_ENABLED   1
  #define NRFX_SPIM3_ENABLED  1
#else
  #define NRFX_QSPI_ENABLED   0
  #define NRFX_SPIM3_ENABLED  0
#endif

#ifndef NRFX_PRS_ENABLED
#define NRFX_PRS_ENABLED 1
#endif

// #define NRFX_UART_ENABLED 1
// #define NRFX_UARTE_ENABLED 1

#endif