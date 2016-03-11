#include "hal.h"

Trigger triggers[] = {
};

Switch switchs[] = {
    Switch("led_blue", 13),
    Switch("led_green", 8),
    Switch("led_red", 12),
    Switch("heater_house", 2),
    Switch("heater_box", 4),
};

Animation animations[] = {
    Animation("fan_box", 11),
    Animation("fan_house", 9),
    Animation("strip_white", 5),
    Animation("strip_blue", 3),
    Animation("strip_red", 6)
};

Sensor sensors[] = {
    Sensor("lux", 0),
    Sensor("temp_box", 5),
    Sensor("temp_house", 1),
    Sensor("humudity_ground", 3)
};

Rgb rgbs[] = {};

DHT dht = DHT(7, DHT11);

DHTSensor DHTSensors[] = {
    DHTSensor("temp", dht, TEMPERATURE, 7),
    DHTSensor("humid", dht, HUMIDITY, 7)
};


HAL_CREATE(hal, sensors, triggers, switchs, animations, rgbs, DHTSensors);

void setup(){
    hal.setup();
}

void loop(){
    hal.loop();
}
