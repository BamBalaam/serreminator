

class PID():
    def __init__(self, defaultPoint, kp=2., ki=0., kd=1.):
        self.defaultPoint = defaultPoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.lastErr = 0.
        self.integral = 0.

    
