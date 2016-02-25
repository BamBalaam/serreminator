class BangBang:
    def __init__(self, setpoint, deviation=0., positive_feedback=True):
        self.setpoint = setpoint
        self.deviation = deviation
        self.run = self._run_pos if positive_feedback else self._run_neg

    def _run_pos(self, state):
        return state < self.setpoint - self.deviation

    def _run_neg(self, state):
        return state > self.setpoint + self.deviation
