#include <MFRC522.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

MFRC522 mfrc522(SS_PIN, RST_PIN);

int getButtonPin(Button buttonId)
{
  return buttonPinMap[static_cast<int>(buttonId)];
}

int getButtonLedPin(Button buttonId)
{
  return buttonLedPinMap[static_cast<int>(buttonId)];
}

void gpio_init()
{
  //TODO: switch everything to use internal pullups!
  pinMode(TRIGGER_PIN, INPUT);
  for (int i = 0; i < NUM_BUTTONS; i++)
  {
    pinMode(buttonPinMap[i], INPUT);
    pinMode(buttonLedPinMap[i], OUTPUT);
  }

  turnOffAllLeds();
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

bool readButton(Button button_id)
{
  if (button_id == Button::NONE)
  {
    return false;
  }

  if (digitalRead(getButtonPin(button_id)) == HIGH)
  {
    writeSerial(Cmd::LOGGING, "button " + String(static_cast<int>(button_id)) + " pressed");
    return true;
  }

  return false;
}

bool triggerPressed()
{
  if (digitalRead(TRIGGER_PIN) == HIGH)
  {
    writeSerial(Cmd::LOGGING, "trigger pressed");
    return true;
  }

  return false;
}

void illuminateButton(Button buttonId, bool state)
{
  if (buttonId == Button::NONE)
  {
    return;
  }

  int ledPin = getButtonLedPin(buttonId);

  writeSerial(Cmd::LOGGING, "illuminating button " + String(static_cast<int>(buttonId)) + " with state " + state);

  digitalWrite(ledPin, state);
}
