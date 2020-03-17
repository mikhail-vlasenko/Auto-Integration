import re
from term import Term

print('''input '1' to evaluate only 1 term''')
s = input()
if s == '1':
    s = input()
    print(Term(s).to_str())
else:
    terms = re.split('[+-]', s)
    signs = re.findall(r'[-+]', s)

    for i in range(len(terms)):
        t = Term(terms[i])
        print(t.to_str(), end=' ')
        if i != len(terms) - 1:
            print(signs[i], end=' ')
