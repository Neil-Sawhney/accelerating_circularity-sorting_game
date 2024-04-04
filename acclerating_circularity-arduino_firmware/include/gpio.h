#pragma once
#include <MFRC522.h>

//TODO: set correctly
// NFC reader setup
#define SS_PIN 9
#define RST_PIN 8

#define BUTTON_0_PIN 3
#define BUTTON_1_PIN 0
#define BUTTON_2_PIN 0
#define BUTTON_3_PIN 0
#define BUTTON_4_PIN 0
#define BUTTON_5_PIN 0

#define BUTTON_0_LED_PIN 22
#define BUTTON_1_LED_PIN 0
#define BUTTON_2_LED_PIN 0
#define BUTTON_3_LED_PIN 0
#define BUTTON_4_LED_PIN 0
#define BUTTON_5_LED_PIN 0

#define TRIGGER_PIN 2

#define NUM_BUTTONS 6
enum class Button
{
  BUTTON_0,
  BUTTON_1,
  BUTTON_2,
  BUTTON_3,
  BUTTON_4,
  BUTTON_5,
  NONE,
};

//maps button ids to pins
const int buttonPinMap[] = {BUTTON_0_PIN, BUTTON_1_PIN, BUTTON_2_PIN, BUTTON_3_PIN, BUTTON_4_PIN, BUTTON_5_PIN};
const int buttonLedPinMap[] = {BUTTON_0_LED_PIN, BUTTON_1_LED_PIN, BUTTON_2_LED_PIN, BUTTON_3_LED_PIN, BUTTON_4_LED_PIN, BUTTON_5_LED_PIN};

int getButtonPin(Button buttonId);
int getButtonLedPin(Button buttonId);

// set pin modes and initialize the RFID reader
void gpio_init();

// check the RFID reader, returns the card id if a card is detected, returns "none" otherwise
String readNFC215();

// check the button with the given id, returns True if the button is pressed, False otherwise
bool readButton(Button button_id);

// check the trigger, returns True if the trigger is pressed, False otherwise
bool triggerPressed();

// illuminate the button with the given id, if button_id is Button::NONE, don't illuminate any button
void illuminateButton(Button buttonId, bool state);