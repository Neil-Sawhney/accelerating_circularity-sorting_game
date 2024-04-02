#include <Arduino.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

void setup()
{
  serial_init();
  gpio_init();

  String msg = "ready";
  writeSerial(Cmd::STATUS, msg);
}

void loop()
{
  String currCard = waitForCard();
  writeSerial(Cmd::CARD_ID, currCard);

  Button targetId = waitForTrigger();

  Button hit = waitForHit(targetId);
  writeSerial(Cmd::BUTTON_HIT, hit);
}
