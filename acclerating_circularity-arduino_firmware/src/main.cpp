#include <Arduino.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

void setup()
{
  serial_init();
  gpio_init();
}

void loop()
{
  writeSerial(Cmd::STATUS, Status::READY);
  waitForStatus();

  waitForCard();

  Button targetId = waitForTarget();
  waitForTrigger();
  waitForHit(targetId);
}
