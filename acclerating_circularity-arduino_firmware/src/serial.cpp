#include <Arduino.h>
#include "serial.h"

void serial_init()
{
    Serial.begin(9600);
    while (!Serial);
}