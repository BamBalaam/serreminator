import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from Control.pid import PID
import asyncio
import converters
import os

import matplotlib.pyplot as plt


logging.basicConfig(
    stream=stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)7s: %(message)s"
)

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


def pid(HAL):
    pid = PID(800, 0.15, min=0, max=255)

    hal.animations.led.upload([0])
    hal.animations.led.looping = True
    hal.animations.led.playing = True

    history = []
    i = 0
    while True:
        mean = 0
        for _ in range(5):
            analogRead = HAL.sensors.lux.value
            resistance = converters.tension2resistance(analogRead, 10000)
            lux = converters.resistance2lux(resistance, **LUXMETER)
            mean += lux
            yield from asyncio.sleep(0.1)
        lux = round(mean / 5, 2)

        res = int(pid.compute(lux))
        logger.info("Obs=%s, PID asks %s", lux, res)

        hal.animations.led.upload([res])

        history.append((800, lux))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax2 = fig.add_subplot(111)
        ax.plot(history)
        ax2.plot(history)
        plt.show()
        plt.savefig('myfig')
        os.rename('myfig.png', 'my.png')
        yield from asyncio.sleep(0.5)
        i += 1


def dump(HAL):


    while True:
        dht = HAL.DHTsensors.temp.value
        analogRead = HAL.sensors.temp.value
        resistance = converters.tension2resistance(analogRead, 10000)
        temp = converters.resistance2celcius(resistance, **THERMISTANCE)

        analogRead = HAL.sensors.lux.value
        resistance = converters.tension2resistance(analogRead, 10000)
        lux = converters.resistance2lux(resistance, **LUXMETER)

        logger.debug("Temp=%s DHT=%s lux=%s", temp, dht, lux)
        yield from asyncio.sleep(1)


def demo(HAL):
    logger.setLevel(logging.INFO)
    print("T° %s" % hal.DHTsensors.temp.value)
    print("Humidity %s" % hal.DHTsensors.humid.value)

    analogRead = HAL.sensors.temp.value
    resistance = converters.tension2resistance(analogRead, 10000)
    temp = converters.resistance2celcius(resistance, **THERMISTANCE)

    print("Analog T° %s" % temp)

    analogRead = HAL.sensors.lux.value
    resistance = converters.tension2resistance(analogRead, 10000)
    lux = converters.resistance2lux(resistance, **LUXMETER)

    print("Lux %s" % lux)

    hal.animations.led.playing = False

    hal.animations.ventilo.looping = True
    hal.animations.ventilo.playing = True
    hal.animations.ventilo.upload([126])
    yield from asyncio.sleep(3)
    hal.animations.ventilo.upload([255])
    yield from asyncio.sleep(3)
    hal.animations.ventilo.upload([0])
    yield from asyncio.sleep(3)

    hal.animations.led.looping = True
    hal.animations.led.playing = True
    hal.animations.led.upload([126])
    yield from asyncio.sleep(3)
    hal.animations.led.upload([255])
    yield from asyncio.sleep(3)

    hal.animations.led.upload([0])


loop = asyncio.get_event_loop()

hal = HAL("/tmp/hal")
loop.create_task(pid(hal))
# loop.create_task(dump(hal))
# loop.create_task(demo(hal))

hal.run(loop=loop)
