import random
from halpy.halpy import HAL
import asyncio
from Control.pid import PID
import converters
import logging
from sys import stdout
from time import sleep

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

class Chromosome:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def get(self):
        return self.kp, self.ki, self.kd

class Genetic:
    def __init__(self, pop_size=150, mut_prob=0.1, cross_rate=0.9, max_gain=5.):
        self.pop_size = pop_size
        self.mut_prob = mut_prob
        self.cross_rate = cross_rate
        self.max_gain = max_gain

    def mutation(self, c):
        choice = random.random()
        if choice < self.mut_prob / 3:
            c.kp += random.random() * self.max_gain
        elif choice < 2 * self.mut_prob / 3:
            c.ki += random.random() * self.max_gain
        elif choice < self.mut_prob:
            c.kd += random.random() * self.max_gain
        return c

    def crossover(self, c1, c2):
        if random.random() > self.cross_rate:
            return c1
        return Chromosome(*{1: (c2.kp, c1.ki, c1.kd),
                2: (c2.kp, c2.ki, c1.kd),
                3: (c1.kp, c1.ki, c2.kd),
                4: (c1.kp, c2.ki, c1.kd),
                5: (c2.kp, c2.ki, c2.kd)
                }[random.randint(1,5)])

    def fitness(self, dx):
        print(dx)
        return 1 / sum(d*d for d in dx)**.5

    def selection(self, fs):
        norm = (lambda s: [f / s for f in fs])(sum(fs))

        cumul = [norm[0]]
        for i in norm[1:]:
            cumul.append(cumul[-1]+i)

        newPop, parents = [], 0
        while parents < 2:
            r, i = random.random(), 0
            while i < self.pop_size:
                if r >= cumul[i] and r < cumul[i+1]:
                    newPop.append(i)
                    parents += 1
                    i = self.pop_size
                i += 1
        return newPop

class geneticPID:
    def __init__(self, genetic, defaultPoint, timesteps=20, max_runs=30, hal=HAL("/tmp/hal")):
        self.genetic = genetic
        self.defaultPoint = defaultPoint
        self.timesteps = timesteps
        self.max_runs = max_runs
        self.population = [Chromosome(random.random()*3, random.random()*2, random.random()*1) for _ in range(self.genetic.pop_size)]
        self.hal = hal

    def runPID(self, index):
        """It's just a simple PID that virtually runs a lot of times"""
        c = self.population[index]
        pid = PID(self.defaultPoint, *c.get(), min=0, max=255)
        print("Testing with", *c.get())
        hal = self.hal

        hal.animations.led.upload([0])
        sleep(0.1)
        hal.animations.led.loopin2 = True
        hal.animations.led.playing = True

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

            res = int(pid.compute(lux))
            logger.info("Obs=%s, PID asks %s", lux, res)


            hal.animations.led.upload([res])
            sleep(0.3)
            i += 1
        return self.genetic.fitness(pid.errors)

    def next_generation(self):
        next_gen = []
        fitnesses = []
        for i in range(self.genetic.pop_size):
            fitnesses.append(self.runPID(i))

        for i in range(self.genetic.pop_size):
            p1, p2 = self.genetic.selection(fitnesses)
            next_gen.append(self.genetic.mutation(self.genetic.crossover(self.population[p1], self.population[p2])))

        self.fitnesses = fitnesses
        self.population = next_gen

    def find_parameters(self):
        for _ in range(self.max_runs):
            self.next_generation()
        max_index = self.fitnesses.index(max(self.fitness))
        return self.population[max_index].kp, self.population[max_index].ki, self.population[max_index].kd

    async def run(self):
        await asyncio.sleep(0.1)
        print(self.find_parameters())
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    g = Genetic()
    hal = HAL("/tmp/hal")
    gpid = geneticPID(g, 800, hal=hal)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gpid.run())
    hal.run(loop=loop)
