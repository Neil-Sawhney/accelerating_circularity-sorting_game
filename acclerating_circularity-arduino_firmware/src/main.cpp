#include <Arduino.h>
#include "gpio.h"
#include "utils.h"
#include "serial.h"

Status game_state = Status::RESET;

void setup()
{
  serial_init();
  gpio_init();
}

//TODO: add functionality rto turn the tech on and off which basically means deciding wheter we should illuminate the target button or not
void loop()
{
  if (game_state == Status::RESET)
  {
    waitForStartButton();
    game_state = Status::READY;
  }

  waitForCard();

  Button targetId = waitForTarget();
  waitForTrigger(targetId);
  waitForHit(targetId);

  game_state = waitForStatus();
}
