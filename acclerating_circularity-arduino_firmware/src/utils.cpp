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

  writeSerial(Cmd::LOGGING, "Received status " + String(static_cast<int>(status)));
  return status;
}

void waitForStartButton()
{
  unsigned long previousMillis = millis();
  bool toggle = false;
  while (!startButtonPressed())
  {
    if (millis() - previousMillis >= FLASH_PERIOD)
    {
      previousMillis = millis();
      toggle = !toggle;
      digitalWrite(START_BUTTON_LED_PIN, toggle);
    }
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
  unsigned long previousMillis = millis();
  bool toggle = false;
  while (!triggerPressed())
  {
    if (millis() - previousMillis >= FLASH_PERIOD)
    {
      previousMillis = millis();
      toggle = !toggle;
      illuminateButton(targetId, toggle);
    }
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

      // wait the remaining time (RFID reader breaks if we dont do this)
      delay(TRAVEL_TIME - (millis() - startTime));
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