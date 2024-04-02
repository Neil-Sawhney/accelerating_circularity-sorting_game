#include <MFRC522.h>
#include "gpio.h"
#include "serial.h"

void gpio_init()
{
  // TODO: setup the pins
  mfrc522.PCD_Init();
}

String readNFC215()
{
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent())
  {
    return "none";
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial())
  {
    return "none";
  }

  String nfcInfo = "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    nfcInfo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    nfcInfo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  nfcInfo.toUpperCase();

  return nfcInfo;
}
