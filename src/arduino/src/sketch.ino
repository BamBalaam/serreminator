#include "hal.h"

Trigger triggers[] = {
};

Switch switchs[] = {
};

Animation animations[] = {
    Animation("ventilo", 5),
    Animation("led", 6)
};

Sensor sensors[] = {
    Sensor("lux", 0),
    Sensor("temp", 1),
    Sensor("ground", 2)
};

Rgb rgbs[] = {
};

//DHT dht = DHT(7, DHT11);
//DHTSensor DHTSensors[] = {
//    DHTSensor("temp", dht, TEMPERATURE, 7),
//    DHTSensor("humid", dht, HUMIDITY, 7)
//};

// ServoAnim servosAnim[] = {
//     // ServoAnim("volets", 6)
// };


HAL_CREATE(hal, sensors, triggers, switchs, animations, rgbs);

void setup(){
    hal.setup();
}

void loop(){
    hal.loop();
}
