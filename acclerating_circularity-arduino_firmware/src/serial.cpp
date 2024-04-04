#include <Arduino.h>
#include "serial.h"
#include <SPI.h>

void serial_init()
{
    Serial.begin(9600);
    SPI.begin();
}

void writeSerial(Cmd cmd, String message)
{
    Serial.print(static_cast<int>(cmd));
    Serial.print(",");
    Serial.println(message);
}

void writeSerial(Cmd cmd, bool targetHit)
{
    Serial.print(static_cast<int>(cmd));
    Serial.print(",");
    Serial.println(targetHit);
}

void writeSerial(Cmd cmd, Button buttonId)
{
    Serial.print(static_cast<int>(cmd));
    Serial.print(",");
    Serial.println(static_cast<int>(buttonId));
}

void writeSerial(Cmd cmd, Status status)
{
    Serial.print(static_cast<int>(cmd));
    Serial.print(",");
    Serial.println(static_cast<int>(status));
}