from time import time


class MultiPID:
    def __init__(self, pidA, pidB):
        self.pidA = pidA
        self.pidB = pidB
        self.current = self.pidA

    def toggle(self):
        self.current = self.pidA if self.current is self.pidA else self.pidB

    def run(self, measured):
        state = self.current.compute(measured)
        if state == self.current.min: self.toggle()
        return state

class PID:
    def __init__(self, defaultPoint, kp=0., ki=0., kd=0., min=float("-inf"), max=float("inf")):
        self.defaultPoint = defaultPoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min = min
        self.max = max
        self.lastMeasured = 0.
        self.integral = 0.
        self.lastTime = time()
        self.previous_state = 0

    def compute(self, measured):
        now = time()
        deltaTime = now - self.lastTime
        error = self.defaultPoint - measured
        self.integral += error * deltaTime
        deltaMeasured = measured - self.lastMeasured
        res = self.kp * error + self.ki * self.integral - self.kd * deltaMeasured / deltaTime

        res = self.previous_state + res
        res = min(max(self.min, res), self.max)
        self.previous_state = res

        self.lastMeasured = measured
        self.lastTime = now
        return res
