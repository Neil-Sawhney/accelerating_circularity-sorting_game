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
 * wait until the trigger is pressed
 * illuminates the target button if there is one while waiting
 * return the target button id or Button::NONE if there is no target
 * writes Status::ERROR to the serial port if the trigger is pressed without a target
 */
Button waitForTrigger();

/*
 * wait until the target button is hit or the TRAVEL_TIME has passed
 * send via serial true if the correct button was hit or false if the TRAVEL_TIME has passed
 */
void waitForHit(Button targetId);