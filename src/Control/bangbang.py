class BangBang:
    def __init__(self, setpoint, deviation=0., positive_feedback=True, true=True, false=False):
        self.setpoint = setpoint
        self.deviation = deviation
        self.run = self._run_pos if positive_feedback else self._run_neg
        self.compute = self.run
        self.true = true
        self.false = false

    def _run_pos(self, state):
        return self.true if state < self.setpoint - self.deviation else self.false

    def _run_neg(self, state):
        return self.true if state > self.setpoint + self.deviation else self.false
