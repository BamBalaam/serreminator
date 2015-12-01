from time import time

class PID():
    def __init__(self, defaultPoint, kp=0., ki=0., kd=0.):
        self.defaultPoint = defaultPoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.lastErr = 0.
        self.integral = 0.
        self.lastTime = time()

    def compute(self, measured):
        now = time()
        deltaTime = now - lastTime
        error = defaultPoint - measured
        self.integral += error * deltaTime
        res = self.kp * error + self.ki * self.integral +
                self.kd * (error - self.lastErr) / deltaTime
        self.lastErr = error
        self.lastTime = now
        return res
