import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from Control.pid import PID
from Control.bangbang import BangBang
import asyncio
import converters
import os
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import collections
import statistics

logging.basicConfig(
    stream=stdout, level=logging.DEBUG,
    format="%(asctime)s %(levelname)7s: %(message)s %(traceback)s")
logger = logging.getLogger(__name__)


LUXMETER = {
    "Ra": 10900,
    "Ea": 351.0,
    "Y": 0.8,
}
THERMISTANCE = {
    "Rat25": 2200,
    "A1": 3.354016E-03,
    "B1": 2.569850E-04,
    "C1": 2.620131E-06,
    "D1": 6.383091E-08,
}


def luxmeter(analogRead):
    resistance = converters.tension2resistance(analogRead, 10000)
    lux = converters.resistance2lux(resistance, **LUXMETER)
    return lux

def thermistor(analogRead):
    resistance = converters.tension2resistance(analogRead, 10000)
    temp = converters.resistance2celcius(resistance, **THERMISTANCE)
    return temp

def humidity(analogRead):
    return round(analogRead * 100)


MAX_COMMANDS_PER_SEC = 10
SENSORS = ["temp_house", "lux", "temp_box", "humudity_ground"]
TRANSFORMERS = [thermistor, luxmeter, thermistor, humidity]

ANIMATIONS = ["fan_box", "fan_house", "strip_blue", "strip_red", "strip_white"]

class MyComponent(ApplicationSession):
    async def onJoin(self, details):
        self.hal = HAL("/tmp/hal")
        for anim in ANIMATIONS:
            getattr(self.hal.animations, anim).upload([0])
            getattr(self.hal.animations, anim).looping = True
            getattr(self.hal.animations, anim).playing = True

        values = {sensor: collections.deque(maxlen=100) for sensor in SENSORS}

        self.glob = {
            "light.pid" : PID(300, 0.005, min=0, max=511),
            "temp.bang" : BangBang(30, 2, False),
            "box.is_manual": False,
        }

        await self.register(self.set_target, u'house.light.set_target')
        await self.register(self.set_bang_target, u'box.temp.set_target')

        await self.register(self.box_set_manual, u'box.controller.set_is_manual')
        await self.register(self.box_is_manual, u'box.controller.get_is_manual')

        await self.register(self.set_box_fan, u'box.control.fan')
        await self.register(self.set_box_heater, u'box.control.heater')

        loop = asyncio.get_event_loop()
        loop.create_task(send_data(values, self.publish, self.glob))
        loop.create_task(adjust(values, self.publish, self.hal, self.glob))
        loop.create_task(handle_leds(values, self.publish, self.hal, self.glob))

        while True:
            for i, sensor in enumerate(SENSORS):
                try:
                    analog = getattr(self.hal.sensors, sensor).value
                    val = TRANSFORMERS[i](analog)
                except TypeError:
                    if len(values[sensor]) > 0:
                        val = values[sensor][-1]
                    else:
                        val = None

                if val is not None:
                    values[sensor].append(val)

                await asyncio.sleep(1 / MAX_COMMANDS_PER_SEC)

    def set_target(self, target):
        self.glob["light.pid"].defaultPoint = target

    def set_bang_target(self, target):
        self.glob["temp.bang"].setpoint = target

    def box_set_manual(self, is_manual):
        self.glob['box.is_manual'] = is_manual

    def box_is_manual(self):
        return bool(self.glob['box.is_manual'])

    def set_box_fan(self, enable):
        if self.glob['box.is_manual']:
            self.hal.animations.fan_box.upload([255 if enable else 0])

    def set_box_heater(self, enable):
        if self.glob['box.is_manual']:
            self.hal.switchs.heater_box.on = bool(enable)

async def send_data(values_dict, publisher, glob):
    while True:
        if all(map(lambda x: len(x) > 0, values_dict.values())):
            publisher('house.light.value', values_dict['lux'][-1])
            publisher('house.temp.value', values_dict['temp_house'][-1])
            publisher('box.temp.value', values_dict['temp_box'][-1])
            publisher('house.ground_humidity.value', values_dict['humudity_ground'][-1])


        publisher('box.temp.target', glob["temp.bang"].setpoint)
        publisher('house.light.target', glob["light.pid"].defaultPoint)

        await asyncio.sleep(0.2)

async def adjust(values_dict, publisher, hal, glob):
    MEAN_OVER_N = 3

    while True:
        if all(map(lambda x: len(x) > MEAN_OVER_N, values_dict.values())):
            pid = glob["light.pid"]
            lux = statistics.mean(list(values_dict['lux'])[-MEAN_OVER_N:])
            res = int(pid.compute(lux))

            if res < 256:
                hal.animations.strip_red.upload([res])
                hal.animations.strip_blue.upload([res])
                hal.animations.strip_white.upload([0])
            else:
                hal.animations.strip_red.upload([255])
                hal.animations.strip_blue.upload([255])
                hal.animations.strip_white.upload([res - 256])

            if not glob['box.is_manual']:
                bang = glob["temp.bang"]
                temp = statistics.mean(list(values_dict['temp_box'])[-MEAN_OVER_N:])
                res = 255 if bang.run(temp) else 0
                hal.animations.fan_box.upload([res])

        await asyncio.sleep(0.1)


async def handle_leds(values_dict, publisher, hal, glob):
    MEAN_OVER_N = 9

    while True:
        if all(map(lambda x: len(x) > MEAN_OVER_N, values_dict.values())):
            bang = glob["temp.bang"]
            temp = statistics.mean(list(values_dict['temp_box'])[-MEAN_OVER_N:])
            hal.switchs.led_blue.on = False
            hal.switchs.led_green.on = False
            hal.switchs.led_red.on = False

            modifier = 1 if glob["box.is_manual"] else 2

            if temp < bang.setpoint - (bang.deviation * modifier):
                hal.switchs.led_blue.on = True
            elif temp < bang.setpoint + (bang.deviation * modifier):
                hal.switchs.led_green.on = True
            else:
                hal.switchs.led_red.on = True

        await asyncio.sleep(0.3)

if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
