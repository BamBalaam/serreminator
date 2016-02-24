import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from Control.pid import PID
import asyncio
import converters
import os
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


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


class MyComponent(ApplicationSession):
    def __init__(self, *args, **kwargs):
        self.hal = HAL("/tmp/hal")
        self.hal.animations.led.upload([0])
        self.hal.animations.led.looping = True
        self.hal.animations.led.playing = True

        self.pid = PID(800, 0.15, min=0, max=255)
        asyncio.async(self.adjust())

        super().__init__(*args, **kwargs)

    async def onJoin(self, details):
        while True:
            self.send_data()
            await asyncio.sleep(0.1)

    def luxmeter(self):
        analogRead = None
        while analogRead is None:
            try:
                analogRead = self.hal.sensors.lux.value
            except TypeError:
                pass
        resistance = converters.tension2resistance(analogRead, 10000)
        lux = converters.resistance2lux(resistance, **LUXMETER)
        return lux

    def thermistor(self):
        analogRead = self.hal.sensors.temp.value
        resistance = converters.tension2resistance(analogRead, 10000)
        temp = converters.resistance2celcius(resistance, **THERMISTANCE)
        return temp

    def send_data(self):
        self.publish('sensor.lux', self.luxmeter())
        self.publish('sensor.temp', self.thermistor())

    async def adjust(self):
        while True:
            mean = 0
            for _ in range(3):
                mean += self.luxmeter()
                await asyncio.sleep(0.05)
            lux = round(mean / 3, 2)

            res = int(self.pid.compute(lux))
            self.publish('pid.light', res)

            self.hal.animations.led.upload([res])
            await asyncio.sleep(0.1)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", debug=True)
    runner.run(MyComponent)
