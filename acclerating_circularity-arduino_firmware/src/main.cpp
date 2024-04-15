#include <Arduino.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

void setup()
{
  serial_init();
  gpio_init();
}

//TODO: add functionality rto turn the tech on and off which basically means deciding wheter we should illuminate the target button or not
void loop()
{
  //TODO: only send READY at the beginning of the game, right after the flashing start button is pressed. implement all that
  writeSerial(Cmd::STATUS, Status::READY);
  waitForStatus();

  waitForCard();

  Button targetId = waitForTarget();
  waitForTrigger();
  waitForHit(targetId);
}
