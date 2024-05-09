#include <MFRC522.h>
#include "gpio.h"
#include "serial.h"
#include "utils.h"

MFRC522 mfrc522(SS_PIN, RST_PIN);

void gpio_init()
{
  pinMode(TRIGGER_PIN, INPUT_PULLUP);
  for (int i = 0; i < NUM_BUTTONS; i++)
  {
    pinMode(buttonPinMap[i], INPUT_PULLUP);
    pinMode(buttonLedPinMap[i], OUTPUT);
    pinMode(START_BUTTON_PIN, INPUT_PULLUP);
    pinMode(START_BUTTON_LED_PIN, OUTPUT);
  }

  turnOffAllLeds();
  mfrc522.PCD_Init();
}

int getButtonPin(Button buttonId)
{
  return buttonPinMap[static_cast<int>(buttonId)];
}

int getButtonLedPin(Button buttonId)
{
  return buttonLedPinMap[static_cast<int>(buttonId)];
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

  if (digitalRead(getButtonPin(button_id)) == LOW)
  {
    writeSerial(Cmd::LOGGING, "button " + String(static_cast<int>(button_id)) + " pressed");
    return true;
  }

  return false;
}

bool startButtonPressed()
{
  if (digitalRead(START_BUTTON_PIN) == LOW)
  {
    writeSerial(Cmd::LOGGING, "start button pressed");
    return true;
  }

  return false;
}

bool triggerPressed()
{
  if (digitalRead(TRIGGER_PIN) == LOW)
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
  digitalWrite(ledPin, state);

}

void setMotorState(MotorState state)
{
  switch (state)
  {
  case MotorState::IDLE:
    digitalWrite(MOTOR_FORWARD_PIN, LOW);
    digitalWrite(MOTOR_BACKWARD_PIN, LOW);
    break;
  case MotorState::OPENING:
    digitalWrite(MOTOR_FORWARD_PIN, HIGH);
    digitalWrite(MOTOR_BACKWARD_PIN, LOW);
    break;
  case MotorState::CLOSING:
    digitalWrite(MOTOR_FORWARD_PIN, LOW);
    digitalWrite(MOTOR_BACKWARD_PIN, HIGH);
    break;
  }
}
