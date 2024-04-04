#include <MFRC522.h>
#include "gpio.h"
#include "serial.h"

MFRC522 mfrc522(SS_PIN, RST_PIN);

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

  int blockAddr = 4; // Block address to read from
  byte data[18];
  byte size = 18;
  MFRC522::StatusCode status = mfrc522.MIFARE_Read(blockAddr, data, &size);

  if (status == MFRC522::StatusCode::STATUS_OK)
  {
    // convert the data to a string
    for (byte i = 9; i < 16; i++)
    {
      // if the data is a letter or a number
      if ((41 <= data[i] && data[i] <= 0x5A) || (61 <= data[i] && data[i] <= 0x7A))
      {
        nfcInfo += (char)data[i];
      }
    }
    mfrc522.PICC_HaltA();
  }

  return nfcInfo;
}
