import logging
from math import *
from sys import stdout
from halpy import HAL

logging.basicConfig(
    stream=stdout, level=logging.INFO,
    format="%(asctime)s %(levelname)7s: %(message)s")
logger = logging.getLogger(__name__)


class HALScript():

    def __init__():
        """
        Setpoints have to be modified!!
        """
        this.GHBOTTOM = 100
        this.AHBOTTOM = 100
        this.TEMPBOTTOM = 20
        this.TEMPUPPER = 40
        this.LIGHTBOTTOM = 100
        this.LIGHTUPPER = 300
        hal = HAL("/tmp/hal")
        hal.run()

    def modifyAirHumidity():
        while True:
            try:
                airHumidity = HAL.sensors.ahs.value
                # Feed to PID -->

                if airHumidity <= AHBOTTOM:
                    # Will puff until higher
                    # Humidifier.activate()
                    pass
            except:
                logger.exception("Error in air humidity.")

    def modifyTemperature():
        while True:
            try:
                temperature = HAL.sensors.temp.value
                # Feed to PID -->

                if temperature <= TEMPBOTTOM:
                    # Ventilation.deactivate()
                    # Resistance.activate()
                    pass
                elif temperature >= TEMPUPPER:
                    # Resistance.deactivate()
                    # Ventilation.activate()
                    pass
            except:
                logger.exception("Error in temperature modifier.")

    def modifyLightIntake():
        while True:
            try:
                luminosity = HAL.sensors.luminosity.value
                lux = sensorsToLux(luminosity)
                # Feed to PID -->

                if lux <= LIGHTBOTTOM:
                    # Control Servo to open
                    pass
                elif lux >= LIGHTUPPER:
                    # Control Servo to close
                    pass
            except:
                logger.exception("Error in shades triggering.")

    def sensorToLux(val):
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
            except:
                logger.exception("Error in irrigation.")
    """
