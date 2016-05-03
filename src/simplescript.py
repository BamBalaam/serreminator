import logging
from math import *
from sys import stdout
from halpy.halpy import HAL
from Control.pid import PID
from Control.bangbang import BangBang
import converters
import os
import collections
import statistics
from time import sleep, time
import matplotlib.pyplot as plt

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

ITERATIONS = 50


def luxmeter(analogRead):
    resistance = converters.tension2resistance(analogRead, 10000)
    #print("res:", resistance)
    lux = converters.resistance2lux(resistance, **LUXMETER)
    return lux

def thermistor(analogRead):
    resistance = converters.tension2resistance(analogRead, 10000)
    temp = converters.resistance2celcius(resistance, **THERMISTANCE)
    return temp

def humidity(analogRead):
    return round(analogRead * 100)


MAX_COMMANDS_PER_SEC = 10
SENSORS = ["lux"]
TRANSFORMERS = [luxmeter]

ANIMATIONS = ["strip_white"]

def get_lux(hal):
    return statistics.mean([luxmeter(hal.sensors.lux.value)] * 3)

def simule(hal, controller):
    MEAN_OVER_N = 3
    PERTURBATION = 50
    start = time()
    hist = []

    for i in range(ITERATIONS):
        lux = get_lux(hal)
        hist.append((lux, time() - start))
        res = int(controller.compute(lux))
        hal.animations.strip_white.upload([res])
        sleep(0.1)

    for i in range(ITERATIONS):
        lux = get_lux(hal)
        hist.append((lux, time() - start))
        res = int(controller.compute(lux)) + PERTURBATION
        res = min(res, 255)
        hal.animations.strip_white.upload([res])
        sleep(0.1)

    return hist

def start(hal):
    hal.animations.strip_white.upload([0])
    hal.animations.strip_white.looping = True
    hal.animations.strip_white.playing = True
    sleep(1)

def mse(datas, target):
    return statistics.mean(map(lambda x:(target - x[0])**2, datas))

def itae(datas, target):
    return sum(map(lambda x:x[1] * abs(x[0] - target), datas))

def iae(datas, target):
    return sum(map(lambda x:abs(x[0] - target), datas))

def ise(datas, target):
    return sum(map(lambda x:(target - x[0])**2, datas))

def itse(datas, target):
    return sum(map(lambda x:x[1] * (target - x[0])**2, datas))

FNS = [mse, itae, iae, ise, itse]
def score(simulation, target):
    score = {}
    for fn in FNS:
        score[fn] = fn(simulation, target)
    return score

if __name__ == '__main__':
    target = 200
    hal = HAL("/tmp/hal")
    start(hal)
    pid = PID(target, 0.115, min=0, max=255)
    res = simule(hal, pid)
    plt.plot([x[0] for x in res])
    plt.plot([target for x in res])
    plt.title(score(res, target))
    plt.savefig("lalala.png")
    print(score(res, target))
