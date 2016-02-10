class BangBang:
    def __init__(self, downlimit, uplimit):
        self.downlimit = downlimit
        self.uplimit = uplimit
        self.on = False
    def run(self, state):
        self.on = self.downlimit <= state <= self.uplimit
        return self.on
