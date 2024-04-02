#pragma once
#include <Arduino.h>
#include "gpio.h"

// TODO: set correctly
//  time it takes for the disk to get from the shooter to the wall in milliseconds
#define TRAVEL_TIME 1000

/*
 * wait until a card is detected and return the card id
 */
String waitForCard();

/*
 * wait until the trigger is pressed
 * illuminates the target button if there is one while waiting
 * return the target button id or Button::NONE if there is no target
 */
Button waitForTrigger();

/*
 * wait until the target button is hit or the TRAVEL_TIME has passed
 * return the target button id or Button::NONE if the TRAVEL_TIME has passed
 */
Button waitForHit(Button targetId);