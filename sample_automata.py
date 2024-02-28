""" Some input automata useful to check functions
    from the class Automata """

from automata import *
from random import *

# B1: (a+b)^*
Sigma = {'a', 'b'}
states_1 = {0}
ini_1 = {0}
final_1 = {0}
trans_1 = {
    0: {'a': {0}, 'b': {0}},
}
B1 = Automata(Sigma, states_1, trans_1, ini_1, final_1)

# B2: |w|_a = 0 modulo 2
Sigma = {'a', 'b'}
states_2 = {0, 1}
ini_2 = {0}
final_2 = {0}
trans_2 = {
    0: {'a': {1}, 'b': {0}},
    1: {'a': {0}, 'b': {1}}
}
B2 = Automata(Sigma, states_2, trans_2, ini_2, final_2)

# B3: (a+b)^*.b
Sigma = {'a', 'b'}
states_3 = {0, 1}
ini_3 = {0}
final_3 = {1}
trans_3 = {
    0: {'a': {0}, 'b': {1}},
    1: {'a': {0}, 'b': {1}}
}
B3 = Automata(Sigma, states_3, trans_3, ini_3, final_3)

# B4: (a+b)^*.b  (non-deterministic)
Sigma = {'a', 'b'}
states_4 = {0, 1}
ini_4 = {0}
final_4 = {1}
trans_4 = {
    0: {'a': {0}, 'b': {0, 1}},
    1: {}
}
B4 = Automata(Sigma, states_4, trans_4, ini_4, final_4)

for B in [B1, B2, B3, B4]:
    print("***   New Automaton  ***")
    print(B)
    print("is deterministic:", B.is_deterministic(True))
    print("is complete:", B.is_complete(True))
    print("is empty:", B.is_empty())
    print("reachable states:", B.reachable_states())
    print("Test acceptance")
    for i in range(10):
        list_symbols = list(B.alphabet)
        word = "".join([choice(list_symbols) for i in range(randrange(10))])
        print("Test", i, " : accept", word, B.accept(word))
