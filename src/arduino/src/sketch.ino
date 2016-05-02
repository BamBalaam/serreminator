#include "hal.h"

Trigger triggers[] = {
};

Switch switchs[] = {
};

Animation animations[] = {
    Animation("strip_white", 3),
};

Sensor sensors[] = {
    Sensor("lux", 0),
};

Rgb rgbs[] = {};


DHTSensor DHTSensors[] = {
};


HAL_CREATE(hal, sensors, triggers, switchs, animations, rgbs, DHTSensors);

void setup(){
    hal.setup();
}

void loop(){
    hal.loop();
}
