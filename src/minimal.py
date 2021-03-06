import logging
from math import *
from sys import stdout, argv
from halpy.halpy import HAL
from Control.pid import PID
import asyncio
import converters
import os

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

savedData = []

async def pid(hal, pid=None, times=float('inf')):
    #f = open('testfile.txt','w')
    Ku = 0.015
    Tu = 0.00001

    Kp = 0.6*Ku
    Ki = (2*Ku)/Tu
    Kd = (Kp*Tu)/8

    if not pid: pid = PID(800, Kp, Ki , Kd, min=0, max=255)
    #pid = PID(800, Ku*0.6, 0 , 0, min=0, max=255)

    hal.animations.led.upload([0])
    hal.animations.led.loopin2 = True
    hal.animations.led.playing = True

    i = 0
    while times:
        mean = 0
        for _ in range(3):
            analogRead = None
            while analogRead is None:
                try:
                    analogRead = hal.sensors.lux.value
                except TypeError:
                    pass
            resistance = converters.tension2resistance(analogRead, 10000)
            lux = converters.resistance2lux(resistance, **LUXMETER)
            mean += lux
            await asyncio.sleep(0.02)
        lux = round(mean / 3, 2)

        res = int(pid.compute(lux))
        logger.info("Obs=%s, PID asks %s", lux, res)

        #toWrite = str(i) + " " + str(lux) + "\n"
        #f.write(toWrite)

        hal.animations.led.upload([res])

        await asyncio.sleep(0.5)
        i += 1

        times -= 1
    print("end loop")

loop = asyncio.get_event_loop()

hal = HAL("/tmp/hal")

if __name__ == '__main__':
    loop.create_task(pid(hal))
    hal.run(loop=loop)
