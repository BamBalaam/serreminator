import math


def tension2resistance(analogRead, resistance):
    """
    Convert sensor value (between 0 and 1) into a sensor resistance
     - analogRead : sensor value
     - resistance : pull-down resistance value (in Ohm)
    """

    Rr = resistance
    Uref = 5

    U2 = Uref * analogRead  # Sensor data to voltage
    Rb = (Rr * Uref) / U2 - Rr  # Resistor data
    return Rb


def resistance2lux(resistance, Ra, Ea, Y):
    """
    Convert a sensor resistance in Lux
    - resistance : photoresistance current resistance (in Ohm)
    """

    lux = math.pow(10, (math.log10(Ra / resistance) / Y + math.log10(Ea)))
    return round(lux, 2)


def resistance2celcius(resistance, Rat25, A1, B1, C1, D1):
    """
    Convert a sensor resistance in °C
    - resistance : thermistance current resistance (in Ohm)
    """

    lnRRref = math.log(resistance / Rat25)

    K = (A1 + B1 * lnRRref + C1 * lnRRref ** 2 + D1 * lnRRref ** 3) ** -1
    T = K - 273.15
    return round(T, 2)
