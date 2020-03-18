import re


class Term:
    def __init__(self, string=''):
        self.coef = 0
        self.power = 0
        self.int_power = 0
        self.int_coef = 0
        self.diff_coef = 0
        self.diff_power = 0
        self.log = False
        self.trigon = 0  # 0 - nothing, 1 - sin, 2 - cos
        self.int_trigon = 0  # 0 - nothing, 1 - sin, 2 - cos
        self.diff_trigon = 0
        self.integrated = False
        self.e_power = None
        if string:
            self.from_str(string)

    def set_value(self, coef=0, power=0, log=False, trigon=0, e_power=0):
        self.coef = int(coef)
        self.power = int(power)
        self.log = log
        self.trigon = trigon
        self.e_power = e_power

    def from_str(self, s):
        self.coef = float(re.search(r'[.\-0-9]*', s)[0])
        coef_end = re.search(r'[.\-0-9]*', s).end()
        assert s[coef_end] == '*'
        if s[coef_end+1] == 'x':
            if coef_end+2 < len(s) and s[coef_end+2] == '^':
                self.power = float(re.search(r'[.\-0-9]*', s[coef_end+3:])[0])
            else:
                self.power = 1
        elif s[coef_end+1: coef_end+7] == 'sin(x)':
            self.trigon = 1
        elif s[coef_end+1: coef_end+7] == 'cos(x)':
            self.trigon = 2
        elif s[coef_end+1] == 'e':
            if s[coef_end+2] == '^':
                self.e_power = Term(re.search(r'\(.*\)', s[coef_end+2:])[0][1:-1])
                assert self.e_power.power <= 1, 'Not implemented'
            else:
                self.coef = self.coef * 2.71828182846

    def integrate(self):
        if self.trigon == 1:
            self.int_coef = -self.coef
            self.int_trigon = 2
        elif self.trigon == 2:
            self.int_coef = self.coef
            self.int_trigon = 1
        elif self.power == -1:
            self.log = True
            self.int_coef = self.coef
        elif self.e_power:
            self.int_coef = self.coef / self.e_power.coef * self.e_power.power
        else:
            self.int_power = self.power + 1
            self.int_coef = self.coef / self.int_power

        self.integrated = True

    def differentiate(self):
        if not self.log:
            if self.trigon == 1:
                self.diff_coef = self.coef
                self.diff_trigon = 2
            elif self.trigon == 2:
                self.diff_coef = -self.coef
                self.diff_trigon = 1
            else:
                self.diff_coef = self.coef * self.power
                self.diff_power = self.power - 1
            return self.diff_coef, self.diff_power, False, self.diff_trigon
        else:
            raise NotImplementedError

    def to_str(self, integrate=True):
        if not self.integrated and integrate:
            self.integrate()

        if not integrate:  # just print
            self.int_power = self.power
            self.int_coef = self.coef
            self.int_trigon = self.trigon

        if self.int_coef % 1 == 0 or self.int_power == 0:
            res = str(self.int_coef)
        else:
            res = str(self.coef) + '/' + str(self.int_power)
        if self.log:
            res += '*ln(|x|)'
        elif self.int_trigon == 1:
            res += '*sin(x)'
        elif self.int_trigon == 2:
            res += '*cos(x)'
        elif self.e_power:
            res += '*e^(' + self.e_power.to_str(integrate=False) + ')'
        else:
            if self.int_power == 0:
                return res
            if self.int_power == 1:
                return res + '*x'
            res += '*x^' + str(self.int_power)
        return res
