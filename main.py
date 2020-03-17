import re
from term_class import Term


def docs_print():
    print('''no spaces allowed
input '1' to evaluate only 1 complicated integral term
(for integration by parts put brackets around product terms)
Don't forget to put +C at the end of an indefinite integral''')


def get_mult_sep(s):
    brackets = 0
    was_x = False
    sep = -1
    for i in range(len(s)):
        if s[i] == '(':
            brackets += 1
        elif s[i] == ')':
            brackets -= 1
        elif s[i] == 'x':
            was_x = True
        elif brackets == 0 and was_x and s[i] == '*':
            assert sep == -1
            sep = i
    return sep


def by_parts(s, sep):
    f = Term(s[1:sep-1])
    g_der = Term(s[sep + 2:-1])
    res = s[:sep + 1] + g_der.to_str() + ' - _int_ ' + Term(*f.differentiate()).to_str(False) \
           + ' * ' + g_der.to_str() + ' dx'
    print(res)


docs_print()

s = input()
if s == '1':
    s = input()
    sep = get_mult_sep(s)
    print('Integration by parts #1: ', end='')
    by_parts(s, sep)
    rev_s = s[sep+1:] + '*' + s[:sep]
    print('Integration by parts #2: ', end='')
    by_parts(rev_s, get_mult_sep(rev_s))
    # print(Term(s).to_str())
else:
    terms = re.split('[+-]', s)
    signs = re.findall(r'[-+]', s)

    for i in range(len(terms)):
        t = Term(terms[i])
        print(t.to_str(), end=' ')
        if i != len(terms) - 1:
            print(signs[i], end=' ')
