#pragma once
#include <Arduino.h>
#include "gpio.h"

// TODO: set correctly
//  time it takes for the disk to get from the shooter to the wall in milliseconds
#define TRAVEL_TIME 1000

/*
 * wait until a card is detected and send its information to the serial port
 */
void waitForCard();

/*
 * wait until we get the target button id from the serial port
 * illuminates the target button if there is one
 * return the target button id or Button::NONE if there is no target
 */
Button waitForTarget();

/*
 * wait until the trigger is pressed
 */
void waitForTrigger();

/*
 * wait until the target button is hit or the TRAVEL_TIME has passed
 * send via serial true if the correct button was hit or false if the TRAVEL_TIME has passed
 */
void waitForHit(Button targetId);

/*
 * turn off the leds on all the buttons
 */
void turnOffAllLeds();