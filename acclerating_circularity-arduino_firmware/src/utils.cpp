#include <Arduino.h>
#include "utils.h"
#include "gpio.h"
#include "serial.h"

void waitForCard() {
  String nfcInfo = "none";
  while (nfcInfo == "none") {
    nfcInfo = readNFC215();
  }
  writeSerial(Cmd::CARD_INFO, nfcInfo);
}

Button waitForTarget() {
  Button targetId = Button::NONE;

  while (targetId == Button::NONE)
  {
    targetId = getTarget();
  }

  illuminateButton(targetId, true);
  return targetId;
}

void waitForTrigger() {
  while (!triggerPressed())
  {
  }
}

void waitForHit(Button targetId) {
  unsigned long startTime = millis();
  while (millis() - startTime < TRAVEL_TIME)
  {
    if (readButton(targetId))
    {
      writeSerial(Cmd::TARGET_HIT, true);
      return;
    }
  }

  writeSerial(Cmd::TARGET_HIT, false);
  illuminateButton(targetId, false);
}

void turnOffAllLeds() {
  for (int i = 0; i < NUM_BUTTONS; i++)
  {
    illuminateButton(static_cast<Button>(i), false);
  }
}