import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from PID.pid import PID
import asyncio


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


def sensorToLux(val):
    Ra = 10.9
    Rr = 10
    Ea = 351.0
    Y = 0.8
    Uref = 5

    U2 = Uref * (val / 1024.0)  # Sensor data to voltage
    Rb = (Rr * Uref) / U2 - Rr  # Resistor data
    lux = pow(10, (log10(Ra / Rb) / Y + log10(Ea)))  # Calculating num of lux
    return lux

loop = asyncio.get_event_loop()

hal = HAL("/tmp/hal")
loop.create_task(modifyTemperature(hal))
hal.run(loop=loop)
