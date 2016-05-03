import asyncio
import logging
import random
from statistics import mean
from sys import stdout
from time import sleep, time

import converters
import names
import yaml
from Control.pid import PID
from halpy.halpy import HAL

logging.basicConfig(stream=stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)7s: %(message)s")

logger = logging.getLogger(__name__)

LUXMETER = {"Ra": 10900, "Ea": 351.0, "Y": 0.8, }


class Chromosome:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.name = names.get_full_name()

    def get(self):
        return self.kp, self.ki, self.kd


class Genetic:
    def __init__(self, pop_size=30, mut_prob=0.1, cross_rate=0.9, max_gain=5.):
        self.pop_size = pop_size
        self.mut_prob = mut_prob
        self.cross_rate = cross_rate
        self.max_gain = max_gain

    def mutation(self, c):
        choice = random.random()
        r = random.uniform(-self.max_gain, self.max_gain)
        if choice < self.mut_prob / 3:
            if c.kp + r > 0: c.kp += r
        elif choice < 2 * self.mut_prob / 3:
            if c.ki + r > 0: c.ki += r
        elif choice < self.mut_prob:
            if c.kd + r > 0: c.kd += r
        return c

    def crossover(self, c1, c2):
        if random.random() > self.cross_rate:
            return c1
        return Chromosome(*{1: (c2.kp, c1.ki, c1.kd),
                            2: (c2.kp, c2.ki, c1.kd),
                            3: (c1.kp, c1.ki, c2.kd),
                            4: (c1.kp, c2.ki, c1.kd),
                            5: (c2.kp, c2.ki, c2.kd)}[random.randint(1, 5)])

    def fitness(self, dx, score):
        return 1. / eval("%s(dx)" % score)

    def selection(self, fs):
        norm = (lambda s: [f / s for f in fs])(sum(fs))

        cumul = [norm[0]]
        for i in norm[1:]:
            cumul.append(cumul[-1] + i)

        newPop, parents = [], 0
        while parents < 2:
            r, i = random.random(), 0
            while i < self.pop_size:
                if r <= cumul[i]:
                    newPop.append(i)
                    parents += 1
                    i = self.pop_size
                i += 1
        return newPop


class geneticPID:
    def __init__(self,
                 genetic,
                 defaultPoint,
                 kp_max,
                 ki_max,
                 kd_max,
                 timesteps=15,
                 max_runs=1,
                 hal=HAL("/tmp/hal"),
                 score_func="ISE"):
        self.genetic = genetic
        self.defaultPoint = defaultPoint
        self.timesteps = timesteps
        self.max_runs = max_runs
        self.score_func = score_func
        self.population = [Chromosome(
            random.uniform(0, kp_max), random.uniform(0, ki_max),
            random.uniform(0, kd_max)) for _ in range(self.genetic.pop_size)]
        self.hal = hal

    def runPID(self, index):
        """It's just a simple PID that virtually runs a lot of times"""
        c = self.population[index]
        pid = PID(self.defaultPoint, *c.get(), min=0, max=255)
        print("Testing with: ", c.name, " ", *c.get())
        hal = self.hal

        hal.animations.strip_white.upload([0])
        sleep(0.1)
        hal.animations.strip_white.loopin2 = True
        hal.animations.strip_white.playing = True

        i = 0
        while i < self.timesteps:
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
                sleep(0.01)
            lux = round(mean / 3, 2)

            res = int(pid.compute(lux, genetic=True))
            logger.info("Obs=%s, PID asks %s", lux, res)

            hal.animations.strip_white.upload([res])
            sleep(0.1)
            i += 1
        return self.genetic.fitness(pid.errors, self.score_func)

    def next_generation(self):
        next_gen = []
        fitnesses = []
        now = time()
        for i in range(self.genetic.pop_size):
            fitnesses.append(self.runPID(i))

        for i in range(self.genetic.pop_size):
            p1, p2 = self.genetic.selection(fitnesses)
            print("Sélectionné: {}, {}".format(self.population[p1].name,
                                               self.population[p2].name))
            next_gen.append(self.genetic.mutation(self.genetic.crossover(
                self.population[p1], self.population[p2])))

        self.fitnesses = fitnesses
        self.population = next_gen

    def find_parameters(self):
        for _ in range(self.max_runs - 1):
            self.next_generation()
        fitnesses = []
        for i in range(self.genetic.pop_size):
            fitnesses.append(self.runPID(i))
        max_index = fitnesses.index(max(fitnesses))
        print("The best:", self.population[max_index].name)
        return self.population[max_index].kp, self.population[
            max_index].ki, self.population[max_index].kd

    def run(self):
        sleep(0.1)
        print(self.find_parameters())
        sleep(0.1)


def from_config(yaml_file):
    try:
        with open(yaml_file) as f:
            conf = yaml.load(f)
    except FileNotFoundError:
        print("No such file")
    else:
        g = Genetic(conf['pop_size'], conf['mut_prob'], conf['cross_rate'],
                    conf['mut_gain'])
        hal = HAL(conf['hal_path'])
        gpid = geneticPID(g, conf['default_point'], conf['kp_max'],
                          conf['ki_max'], conf['kd_max'], conf['lifetime'],
                          conf['max_runs'], hal, conf['score_func'])
        gpid.run()
        #hal.run(loop=loop)


def MSE(dx):
    return mean(d * d for d, _ in dx)


def ITAE(dx):
    return sum(t * abs(d) for d, t in dx)


def IAE(dx):
    return sum(abs(d) for d, _ in dx)


def ISE(dx):
    return sum(d * d for d, _ in dx)


def ITSE(dx):
    return sum(t * d * d for d, t in dx)


if __name__ == '__main__':
    from_config("Control/config.yaml")
    #g = Genetic()
    #hal = HAL("/tmp/hal")
    #gpid = geneticPID(g, 800, hal=hal)
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(gpid.run())
    #hal.run(loop=loop)
