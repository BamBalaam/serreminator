from time import time


class PID():
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
        self.previous_error = 0

    def compute(self, measured):
        now = time()
        deltaTime = now - self.lastTime
        error = self.defaultPoint - measured
        self.integral += error * deltaTime
        derivative = (error - self.previous_error)/ (deltaTime * 1000)
        res = self.kp * error + self.ki * self.integral + self.kd * derivative

        res = self.previous_state + res
        res = min(max(self.min, res), self.max)
        self.previous_state = res
        self.previous_error = error

        self.lastMeasured = measured
        self.lastTime = now
        return res
