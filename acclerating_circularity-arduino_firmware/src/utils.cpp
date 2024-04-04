#include <Arduino.h>
#include "utils.h"
#include "gpio.h"
#include "serial.h"

void waitForCard() {
  String nfcInfo = "";
  while (nfcInfo.length() == 0) {
    nfcInfo = readNFC215();
  }
  if (nfcInfo != "none")
  {
    writeSerial(Cmd::CARD_INFO, nfcInfo);
  }
}

Button waitForTrigger() {
  Button targetId = Button::NONE;

  while (!triggerPressed())
  {
    targetId = getTarget();

    // don't turn off an illuminated button
    if (targetId != Button::NONE)
    {
      illuminateButton(targetId, true);
    }
  }

  return targetId;
}

void waitForHit(Button targetId) {
  unsigned long startTime = millis();
  while (millis() - startTime < TRAVEL_TIME)
  {
    if (readButton(targetId))
    {
      writeSerial(Cmd::TARGET_HIT, true);
    }
  }

  writeSerial(Cmd::TARGET_HIT, false);
}