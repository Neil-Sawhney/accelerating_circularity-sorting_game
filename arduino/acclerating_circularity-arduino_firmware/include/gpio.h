#pragma once
#include <MFRC522.h>

//TODO: set correctly
// NFC reader setup
#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

// set pin modes and initialize the RFID reader
void gpio_init();

// check the RFID reader, returns the card id if a card is detected, returns "none" otherwise
String readNFC215();

// check the button with the given id, returns True if the button is pressed, False otherwise
bool readButton(int button_id);

// check the trigger, returns True if the trigger is pressed, False otherwise
void readTrigger();

// Turns on the light for the button with the given id
void setTarget(int button_id);

// Turns off the light for the button with the given id
void resetTarget(int button_id);