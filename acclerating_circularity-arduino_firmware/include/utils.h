#pragma once
#include <Arduino.h>
#include "gpio.h"
#include "serial.h"

//  time it takes for the disk to get from the shooter to the wall in milliseconds
#define TRAVEL_TIME 500

// time it takes for the disks to slide under the door in milliseconds
#define DOOR_TIME 1000

#define FLASH_PERIOD 100


/*
 * wait until we get Cmd::STATUS from the serial port and return the Status
 */
Status waitForStatus();

/*
 * wait until the start button is pressed and send Cmd::STATUS, Status::READY to the serial port and clear the basket
 */
void waitForStartButton();

/*
 * wait until a card is detected and send its information to the serial port
 */
void waitForCard();

/*
 * wait until we get the target button id from the serial port
 * return the target button id or Button::NONE if there is no target
 */
Button waitForTarget();

/*
 * wait until the trigger is pressed
 * flashes the target button if tech is on
 */
void waitForTrigger(Button targetId, Status techState);

/*
 * wait until the target button is hit or the TRAVEL_TIME has passed
 * send via serial true if the correct button was hit or false if the TRAVEL_TIME has passed
 */
void waitForHit(Button targetId);

/*
 * turn off the leds on all the buttons
 */
void turnOffAllLeds();

/*
 * open the door for DOOR_TIME milliseconds
 */
void clearBasket();