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



MAX_COMMANDS_PER_SEC = 10
SENSORS = ["temp_house", "lux", "temp_box"]
TRANSFORMERS = [thermistor, luxmeter, thermistor]

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
            "light.pid" : PID(300, 0.005, min=0, max=255),
            "temp.bang" : BangBang(30, 2, False)
        }

        await self.register(self.set_target, u'pid.light.set_target')
        await self.register(self.set_bang_target, u'pid.temp.set_target')

        loop = asyncio.get_event_loop()
        loop.create_task(send_data(values, self.publish))
        loop.create_task(adjust(values, self.publish, self.hal, self.glob))

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

async def send_data(values_dict, publisher):
    while True:
        if len(values_dict['lux']) > 0 and len(values_dict['temp_house']) and len(values_dict['temp_box']):
            publisher('sensor.lux', values_dict['lux'][-1])
            publisher('sensor.temp', values_dict['temp_house'][-1])
            publisher('sensor.box_temp', values_dict['temp_box'][-1])

        await asyncio.sleep(0.2)

async def adjust(values_dict, publisher, hal, glob):
    MEAN_OVER_N = 3

    while True:
        pid = glob["light.pid"]
        if len(values_dict['lux']) < MEAN_OVER_N:
            await asyncio.sleep(0.1)
            continue

        val = [values_dict['lux'][-(i+1)] for i in range(MEAN_OVER_N)]
        lux = statistics.mean(val)

        res = int(pid.compute(lux))
        publisher('pid.output.light', res)
        publisher('pid.input.light', pid.defaultPoint)

        hal.animations.strip_white.upload([res])

        bang = glob["temp.bang"]
        if len(values_dict['temp_box']) < MEAN_OVER_N:
            await asyncio.sleep(0.1)
            continue

        val = [values_dict['temp_box'][-(i+1)] for i in range(MEAN_OVER_N)]
        temp = statistics.mean(val)

        res = 255 if bang.run(temp) else 0
        publisher('pid.output.temp', res)
        publisher('pid.input.temp', bang.setpoint)

        hal.animations.fan_box.upload([res])

        await asyncio.sleep(0.1)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
