import test_automata
from automata import Automata

# Construction d'un premier automate
Sigma = {'a', 'b'}
states = {0, 1, 2}
trans = {
    0: {'a': {1}},
    1: {'b': {1, 2}, 'a': {1}}
}
ini = {0}
final = {2}
# A l'aide du constructeur de la classe
A = Automata(Sigma, states, trans, ini, final)
print(A)

# Construction du même automate
# à l'aide des méthodes de la classe
Abis = Automata(Sigma, set(), {}, set(), set())
print(Abis)
Abis.add_state(0)
Abis.add_state(1)
Abis.add_state(2)
Abis.set_initial(0)
Abis.set_final(2)
Abis.add_transition(0, 'a', 1)
Abis.add_transition(1, 'a', 1)
Abis.add_transition(1, 'b', 1)
Abis.add_transition(1, 'b', 2)
print(Abis)

# 1. Construction de l'automate de la figure 2
B = Automata(Sigma, set(), {}, set(), set())
B.add_state(0)
B.add_state(1)
B.add_state(2)
B.add_state(3)
B.set_initial(0)
B.set_final(3)
B.add_transition(0, "a", 0)
B.add_transition(0, "b", 0)
B.add_transition(0, "b", 1)
B.add_transition(1,"a", 2)
B.add_transition(2, "b", 3)
B.add_transition(3, "a", 3)
B.add_transition(3, "b", 3)
print(B)


# 2.
print("A est déterministe : ")
print(A.is_deterministic(True))
# Rendons A déterministe:

Adeter = Automata(Sigma, set(), {}, set(), set())

Adeter.add_state(0)
Adeter.add_state(1)
Adeter.add_state("1,2")
Adeter.add_state(3) # Etat cimetière, pour le rendre complet en plus.

Adeter.set_final("1,2")
Adeter.set_initial(0)


Adeter.add_transition(3, "b", 3)
Adeter.add_transition(3, "a", 3)

Adeter.add_transition(0, "b", 3)
Adeter.add_transition(0, "a", 1)

Adeter.add_transition(1, "a", 1)
Adeter.add_transition(1, "b", "1,2")

Adeter.add_transition("1,2", "b", "1,2")
Adeter.add_transition("1,2", "a", 1)

Adeter.union(B)
