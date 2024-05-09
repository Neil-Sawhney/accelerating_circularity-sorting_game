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
    writeSerial(Cmd::LOGGING, "Start button pressed");
    game_state = Status::READY;
  }

  writeSerial(Cmd::LOGGING, "Waiting for card");
  waitForCard();

  writeSerial(Cmd::LOGGING, "Waiting for target");
  Button targetId = waitForTarget();

  writeSerial(Cmd::LOGGING, "Waiting for trigger");
  waitForTrigger(targetId);
  waitForHit(targetId);

  writeSerial(Cmd::LOGGING, "Waiting for status");
  game_state = waitForStatus();
}
