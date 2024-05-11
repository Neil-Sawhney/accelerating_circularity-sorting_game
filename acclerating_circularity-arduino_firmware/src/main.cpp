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

void loop()
{
  if (game_state == Status::RESET)
  {
    waitForStatus();
    waitForStartButton();
    writeSerial(Cmd::LOGGING, "Start button pressed");
    game_state = Status::TECH_OFF;
  }

  writeSerial(Cmd::LOGGING, "Waiting for card");
  waitForCard();

  writeSerial(Cmd::LOGGING, "Waiting for target");
  Button targetId = waitForTarget();

  writeSerial(Cmd::LOGGING, "Waiting for trigger");
  waitForTrigger(targetId, game_state);
  waitForHit(targetId);

  writeSerial(Cmd::LOGGING, "Waiting for status");
  game_state = waitForStatus();
}
