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