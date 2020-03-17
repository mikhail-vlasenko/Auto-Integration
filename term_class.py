import re
import sys

class Term:
    def __init__(self, coef=0, power=0, log=False):
        try:
            self.coef = int(coef)
            self.power = int(power)
        except ValueError:
            self.from_str(coef)
        self.int_power = 0
        self.int_coef = 0
        self.diff_coef = 0
        self.diff_power = 0
        self.log = log
        self.integrated = False

    def from_str(self, s):
        self.coef = int(re.search(r'[\-0-9]*', s)[0])
        coef_end = re.search(r'[\-0-9]*', s).end()
        assert s[coef_end] == '*'
        assert s[coef_end+1] == 'x'
        if coef_end+2 < len(s) and s[coef_end+2] == '^':
            self.power = int(re.search(r'[\-0-9]*', s[coef_end+3:])[0])
        else:
            self.power = 1

    def integrate(self, advanced=False):
        if self.power == -1:
            self.log = True
            self.int_coef = self.coef
        else:
            self.int_power = self.power + 1
            self.int_coef = self.coef / self.int_power
        self.integrated = True

    def differentiate(self):
        if not self.log:
            self.diff_coef = self.coef * self.power
            self.diff_power = self.power - 1
            return self.diff_coef, self.diff_power
        else:
            raise NotImplementedError

    def to_str(self, integrate=True):
        if not self.integrated and integrate:
            self.integrate()
        res = ''
        if not integrate:
            res = str(self.coef)
            if self.power == 0:
                return res
            if self.power == 1:
                return res + '*x'
            return str(self.coef) + '*x^' + str(self.power)

        if self.int_coef % 1 == 0:
            res = str(self.int_coef)
        else:
            res = str(self.coef) + '/' + str(self.int_power)
        if not self.log:
            if self.int_power == 0:
                return res
            if self.int_power == 1:
                return res + '*x'
            res += '*x^' + str(self.int_power)
        else:
            res += '*ln(|x|)'
        return res
