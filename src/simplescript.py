import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from PID.pid import PID
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
SENSORS = ["temp", "lux"]
TRANSFORMERS = [thermistor, luxmeter]

class MyComponent(ApplicationSession):
    async def onJoin(self, details):
        self.hal = HAL("/tmp/hal")
        self.hal.animations.led.upload([0])
        self.hal.animations.led.looping = True
        self.hal.animations.led.playing = True

        values = {sensor: collections.deque(maxlen=100) for sensor in SENSORS}

        self.glob = {
            "light.pid" : PID(800, 0.15, 0.1, 0.005, min=0, max=255)
        }

        yield from self.register(set_target, u'pid.light.set_target')

        loop = asyncio.get_event_loop()
        loop.create_task(send_data(values, self.publish))
        loop.create_task(adjust(values, self.publish, self.hal, glob))

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
        self.glob["light.pid"] = PID(target, 0.15, 0.1, 0.005, min=0, max=255)

async def send_data(values_dict, publisher):
    while True:
        if len(values_dict['lux']) > 0 and len(values_dict['temp']):
            publisher('sensor.lux', values_dict['lux'][-1])
            publisher('sensor.temp', values_dict['temp'][-1])

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
        publisher('pid.input.light', 800)

        hal.animations.led.upload([res])
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
