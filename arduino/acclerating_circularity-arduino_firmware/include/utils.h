#pragma once
#include <Arduino.h>

//TODO: set correctly
// time it takes for the disk to get from the shooter to the wall in milliseconds
#define TRAVEL_TIME 1000

/*
 * wait until a card is detected and return the card id
 */
String waitForCard();