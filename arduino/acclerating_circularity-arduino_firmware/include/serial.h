#pragma once

enum class cmd {
  STATUS,
  TARGET,
  CARD_ID,
  BUTTON_ID,
};

/*
 * Sets up the serial port.
 * Blocks until the serial port is ready.
 */
void serial_init();

/*
 * Writes a message to the serial port.
 */
void writeSerial(cmd, char* message);

/*
 * Reads from the serial port and returns the target button id.
 * If the target button id is -1, there is no target.
 * If there is nothing to read, return 0
 */
int getTarget();
