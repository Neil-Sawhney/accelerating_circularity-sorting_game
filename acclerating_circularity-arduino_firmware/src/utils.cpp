#include <Arduino.h>
#include "utils.h"
#include "gpio.h"
#include "serial.h"

Status waitForStatus()
{
  Status status = Status::NONE;
  while (status == Status::NONE)
  {
    status = getStatus();
  }

  return status;
}

void waitForStartButton()
{
  // This toggle allows us to block for less time so that the button is more responsive
  bool toggle_light = HIGH;
  while (!startButtonPressed())
  {
    digitalWrite(START_BUTTON_LED_PIN, toggle_light);
    toggle_light = !toggle_light;
    delay(50);
  }
  clearBasket();
  writeSerial(Cmd::STATUS, Status::READY);
}

void waitForCard()
{
  String nfcInfo = "none";
  while (nfcInfo == "none")
  {
    nfcInfo = readNFC215();
  }
  writeSerial(Cmd::CARD_INFO, nfcInfo);
}

Button waitForTarget()
{
  Button targetId = Button::NONE;

  while (targetId == Button::NONE)
  {
    targetId = getTarget();
  }

  return targetId;
}

void waitForTrigger(Button targetId)
{
  while (!triggerPressed())
  {
    //FIXME: BLOCKING
    illuminateButton(targetId, true);
    delay(50);
    illuminateButton(targetId, false);
    delay(50);
  }
}

void waitForHit(Button targetId)
{
  unsigned long startTime = millis();
  while (millis() - startTime < TRAVEL_TIME)
  {
    if (readButton(targetId))
    {
      writeSerial(Cmd::TARGET_HIT, true);
      illuminateButton(targetId, false);
      return;
    }
  }

  writeSerial(Cmd::TARGET_HIT, false);
  illuminateButton(targetId, false);
}

void turnOffAllLeds()
{
  for (int i = 0; i < NUM_BUTTONS; i++)
  {
    illuminateButton(static_cast<Button>(i), false);
  }
}

void clearBasket()
{
  setMotorState(MotorState::OPENING);
  delay(DOOR_TIME);
  setMotorState(MotorState::CLOSING);
  delay(DOOR_TIME);
  setMotorState(MotorState::IDLE);
}