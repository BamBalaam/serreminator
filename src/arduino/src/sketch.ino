#include "hal.h"

Trigger triggers[] = {
};

Switch switchs[] = {
};

Animation animations[] = {
    Animation("ventilo", 3),
};

Sensor sensors[] = {
    Sensor("lux", 0)
};

Rgb rgbs[] = {
};

DHT dht = DHT(2, DHT11);
DHTSensor DHTSensors[] = {
    DHTSensor("temp", dht, TEMPERATURE, 2),
    DHTSensor("humid", dht, HUMIDITY, 2)
};

ServoAnim servosAnim[] = {
    ServoAnim("volets", 6)
};


HAL_CREATE(hal, sensors, triggers, switchs, animations, rgbs, DHTSensors, servosAnim);

void setup(){
    hal.setup();
}

void loop(){
    hal.loop();
}
