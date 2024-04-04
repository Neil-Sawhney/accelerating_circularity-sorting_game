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

void writeSerial(Cmd cmd, const char *message)
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

Button getTarget()
{
    if (Serial.available() > 0)
    {
        // incoming message should be in the format "Cmd::TARGET,Button::ID"
        String message = Serial.readStringUntil('\n');
        if (message.startsWith(String(static_cast<int>(Cmd::TARGET))))
        {
            int buttonId = message.substring(message.indexOf(',') + 1).toInt();
            return static_cast<Button>(buttonId);
        }
    }
    return Button::NONE;
}

Status getStatus()
{
    if (Serial.available() > 0)
    {
        // incoming message should be in the format "Cmd::STATUS,Status::ID"
        String message = Serial.readStringUntil('\n');
        if (message.startsWith(String(static_cast<int>(Cmd::STATUS))))
        {
            int status = message.substring(message.indexOf(',') + 1).toInt();
            return static_cast<Status>(status);
        }
    }
    return Status::NONE;
}
