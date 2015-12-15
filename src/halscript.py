import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
import asyncio

logging.basicConfig(
    stream=stdout, level=logging.INFO,
    format="%(asctime)s %(levelname)7s: %(message)s")
logger = logging.getLogger(__name__)


class HALScript():

    def __init__(self):
        """
        Setpoints have to be modified!!
        """
        GHBOTTOM = 100
        AHBOTTOM = 100
        TEMPBOTTOM = 20
        TEMPUPPER = 40
        LIGHTBOTTOM = 100
        LIGHTUPPER = 300
        hal = HAL("/tmp/hal")
        #asyncio.async(self.modifyAirHumidity())
        asyncio.async(self.modifyTemperature())
        #asyncio.async(self.modifyLightIntake())

    def modifyAirHumidity(self):
        while True:
            try:
                airHumidity = HAL.sensors.ahs.value
                # Feed to PID -->

                if airHumidity <= AHBOTTOM:
                    # Will puff until higher
                    # Humidifier.activate()
                    pass
                yield from asyncio.sleep(1)
            except:
                logger.exception("Error in air humidity.")

    def modifyTemperature(self):
        tempPID = PID(10)
        while True:
            try:
                temperature = HAL.DHTsensor.value
                res = tempPID.compute(temperature)
                hal.animations.ventilo.upload([res])
                hal.animations.ventilo.looping = True
                hal.animations.ventilo.playing = True
                logger.debug("Set ventilation at %s" %res)
                yield from asyncio.sleep(1)
            except:
                logger.exception("Error in temperature modifier.")

    def modifyLightIntake(self):
        while True:
            try:
                luminosity = HAL.sensors.luminosity.value
                lux = sensorsToLux(luminosity)
                # Feed to PID -->

                if lux <= LIGHTBOTTOM:
                    # Control Servo to open blinds
                    pass
                elif lux >= LIGHTUPPER:
                    # Control Servo to close blinds
                    pass
                yield from asyncio.sleep(1)
            except:
                logger.exception("Error in shades triggering.")

    def sensorToLux(self, val):
        Ra = 10.9
        Rr = 10
        Ea = 351.0
        Y = 0.8
        Uref = 5

        U2 = Uref * (val/1024.0)  # Sensor data to voltage
        Rb = (Rr * Uref)/U2 - Rr  # Resistor data
        lux = pow(10, (log10(Ra/Rb)/Y + log10(Ea)))  # Calculating num of lux
        return lux

    """
    # TO DO NEXT QUADRI
    def modifyGroundHumidity():
        while True:
            try:
                groundHumidity = HAL.sensors.ghs.value

                if groundHumidity <= GHBOTTOM:
                    # Irrigation.activate()
                    pass
                yield from asyncio.sleep(1)
            except:
                logger.exception("Error in irrigation.")
    """

HALScript()
