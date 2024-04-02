#pragma once
#include <MFRC522.h>
#include "serial.h"

//TODO: set correctly
// NFC reader setup
#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

enum class Button
{
  NONE,
  BUTTON_1,
  BUTTON_2,
  BUTTON_3,
  BUTTON_4,
  BUTTON_5,
  BUTTON_6,
};

// set pin modes and initialize the RFID reader
void gpio_init();

// check the RFID reader, returns the card id if a card is detected, returns "none" otherwise
String readNFC215();

// check the button with the given id, returns True if the button is pressed, False otherwise
bool readButton(Button button_id);

// check the trigger, returns True if the trigger is pressed, False otherwise
bool triggerPressed();

// illuminate the button with the given id, if button_id is Button::NONE, don't illuminate any button
void illuminateButton(Button buttonId, bool on);