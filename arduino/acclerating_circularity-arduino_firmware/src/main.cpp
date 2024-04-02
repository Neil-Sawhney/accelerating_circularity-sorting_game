#include <Arduino.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

void setup()
{
  serial_init();
  gpio_init();

  writeSerial(Cmd::STATUS, Status::READY);
}

void loop()
{
  waitForCard();

  Button targetId = waitForTrigger();
  waitForHit(targetId);
}
