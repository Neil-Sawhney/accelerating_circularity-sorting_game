#include <Arduino.h>
#include "utils.h"
#include "gpio.h"

String waitForCard() {
  String nfcInfo = "";
  while (nfcInfo.length() == 0) {
    nfcInfo = readNFC215();
  }
  return nfcInfo;
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