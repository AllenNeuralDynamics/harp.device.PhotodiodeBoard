#ifndef CONFIG_H
#define CONFIG_H

#define UART_TX_PIN (0)
#define HARP_SYNC_RX_PIN (5)
#define HARP_CORE_LED_PIN (25)

#define HARP_DEVICE_ID (1412)
#define HARP_DEVICE_NAME "PhotodiodeBoard"

#define HW_VERSION_MAJOR (0)
#define HW_VERSION_MINOR (0)
#define HW_VERSION_PATCH (0)

#define FW_VERSION_MAJOR (0)
#define FW_VERSION_MINOR (0)
#define FW_VERSION_PATCH (0)

// Photodiode inputs, named by board signal (ADC0/ADC1 in device.yml).
// RP2040 ADC input N is fixed to GPIO 26 + N, so these are hardware
// ADC inputs 1 and 2.
#define ADC0_PIN (27)
#define ADC1_PIN (28)
#define ADC0_INPUT (ADC0_PIN - 26)
#define ADC1_INPUT (ADC1_PIN - 26)
#define ADC_CHANNEL_COUNT (2)

#define SAMPLE_RATE_HZ (1000)

#endif // CONFIG_H
