#include <Arduino.h>
#include "gpio.h"
#include "serial.h"

void setup()
{
  serial_init();
  gpio_init();
  writeSerial(cmd::STATUS, "ready");
}

void loop()
{
}
