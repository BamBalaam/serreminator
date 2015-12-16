import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from PID.pid import PID
import asyncio
import converters


logging.basicConfig(
    stream=stdout,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)7s: %(message)s"
)

logger = logging.getLogger(__name__)


def modifyTemperature(HAL):
    tempPID = PID(10)
    while True:
        temperature = HAL.DHTsensors.temp.value
        res = tempPID.compute(temperature)
        hal.animations.ventilo.upload([res])
        hal.animations.ventilo.looping = True
        hal.animations.ventilo.playing = True
        logger.debug("Set ventilation at %s with actual=%i" % (res, temperature))
        yield from asyncio.sleep(1)


def dump(HAL):
    themristance = {
        "Rat25": 2200,
        "A1": 3.354016E-03,
        "B1": 2.569850E-04,
        "C1": 2.620131E-06,
        "D1": 6.383091E-08,
    }

    luxmeter = {
        "Ra": 10900,
        "Ea": 351.0,
        "Y": 0.8,
    }

    while True:
        dht = HAL.DHTsensors.temp.value
        analogRead = HAL.sensors.temp.value
        resistance = converters.tension2resistance(analogRead, 10000)
        temp = converters.resistance2celcius(resistance, **themristance)

        analogRead = HAL.sensors.lux.value
        resistance = converters.tension2resistance(analogRead, 10000)
        lux = converters.resistance2lux(resistance, **luxmeter)

        logger.debug("Temp=%s DHT=%s lux=%s", temp, dht, lux)
        yield from asyncio.sleep(1)


loop = asyncio.get_event_loop()

hal = HAL("/tmp/hal")
# loop.create_task(modifyTemperature(hal))
loop.create_task(dump(hal))
hal.run(loop=loop)
