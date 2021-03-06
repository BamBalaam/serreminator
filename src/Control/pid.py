from time import time


class MultiPID:
    def __init__(self, pidA, pidB):
        self.pidA = pidA
        self.pidB = pidB
        self.current_is_A = True

    def toggle(self):
        self.current = not self.current

    def run(self, measured):
        if self.current_is_A:
            stateA = self.pidA.compute(measured)
            if stateA == self.pidA.min:
                self.toggle()
                return stateA, self.pidB.compute(measured)
            else:
                return stateA, self.pidB.min
        else:
            stateB = self.pidB.compute(measured)
            if stateB == self.pidB.min:
                self.toggle()
                return self.pidA.compute(measured), stateB
            else:
                return self.pidA.min, stateB


class PID:
    def __init__(self,
                 defaultPoint,
                 kp=0.,
                 ki=0.,
                 kd=0.,
                 min=float("-inf"),
                 max=float("inf")):
        self.defaultPoint = defaultPoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min = min
        self.max = max
        self.lastMeasured = 0.
        self.integral = 0.
        self.lastTime = time()
        self.previous_error = 0
        self.previous_state = 0
        self.lastTime = time()
        self.errors = []

    def compute(self, measured, now=None, genetic=False):
        self.measured = measured
        if now is None:
            now = time()
        deltaTime = now - self.lastTime
        error = self.defaultPoint - measured
        if genetic: self.errors.append((error, now))
        self.integral += error * deltaTime
        derivative = (error - self.previous_error) / (deltaTime * 1000)
        res = self.kp * error + self.ki * self.integral + self.kd * derivative

        res = self.previous_state + res
        res = min(max(self.min, res), self.max)
        self.previous_state = res
        self.previous_error = error

        self.lastMeasured = measured
        self.lastTime = now

        return res

    def setKp(self, inputKp):
        self.kp = inputKp

    def setParameters(self, inputKp, inputKi, inputKd):
        self.kp, self.ki, self.kd = inputKp, inputKi, inputKd

    def getSavedPoints(self):
        return self.savedPoints
