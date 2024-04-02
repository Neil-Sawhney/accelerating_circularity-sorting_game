#pragma once

#include <Arduino.h>
#include "gpio.h"

enum class Cmd
{
  STATUS,
  TARGET,
  CARD_INFO,
  TARGET_HIT,
  LOGGING,
};

enum class Status
{
  READY,
  WAITING_FOR_CARD,
  WAITING_FOR_TRIGGER,
  ERROR,
};


/*
 * Sets up the serial port.
 * Blocks until the serial port is ready.
 */
void serial_init();

/*
 * Writes a message to the serial port.
 */
void writeSerial(Cmd, String message);
void writeSerial(Cmd, Button buttonId);
void writeSerial(Cmd, bool targetHit);

/*
 * Reads from the serial port and returns the target button id.
 * If there is nothing to read or if there is no target, return Button:NONE.
 */
Button getTarget();
