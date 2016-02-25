#include "hal.h"

Trigger triggers[] = {
};

Switch switchs[] = {
    Switch("LED_bleu", 2),
    Switch("LED_vert", 8),
    Switch("LED_rouge", 9)
};

Animation animations[] = {
    Animation("ventilo", 3),
    Animation("led_strip", 6)
};

Sensor sensors[] = {
    Sensor("lux", 0),
    Sensor("temp", 1),
    Sensor("ground", 2),
    Sensor("box_temp", 3)
};

Rgb rgbs[] = {
};

DHT dht = DHT(7, DHT11);
DHTSensor DHTSensors[] = {
    DHTSensor("temp", dht, TEMPERATURE, 7),
    DHTSensor("humid", dht, HUMIDITY, 7)
};

// ServoAnim servosAnim[] = {
//     // ServoAnim("volets", 6)
// };


HAL_CREATE(hal, sensors, triggers, switchs, animations, rgbs, DHTSensors);

void setup(){
    hal.setup();
}

void loop(){
    hal.loop();
}
