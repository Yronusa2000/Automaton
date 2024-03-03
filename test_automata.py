import sample_automata
from automata import Automata

Sigma = {'a', 'b'}
states = {0, 1, 2}
trans = {
    0: {'a': {1}},
    1: {'b': {1, 2}, 'a': {1}}
}
ini = {0}
final = {2}
A = Automata(Sigma, states, trans, ini, final)

ini = {0, 1}
B = Automata(Sigma, states, trans, ini, final)

trans = {
    0: {'a': {1}},
    1: {'b': {2}, 'a': {1}}
}
ini = {0}

C = Automata(Sigma, states, trans, ini, final)

trans = {
    0: {'a': {1}, 'b': {2}},
    1: {'b': {2}, 'a': {1}},
    2: {'a': {1, 2}, 'b': {0}}
}

D = Automata(Sigma, states, trans, ini, final)


def test_isdeterministic():
    # A a deux transitions à partir de 1 sur b
    assert (A.is_deterministic() == False)
    # B a deux états initiaux
    assert (B.is_deterministic() == False)
    # C est déterministe
    assert (C.is_deterministic() == True)


def test_iscomplete():
    assert (A.is_complete(True) == False)
    assert (D.is_complete(True) == True)
    return


def test_compute_next():
    X = {1, 2}
    letter = 'a'
    Y = {1}
    assert (A.compute_next(X, letter) == Y)
    letter = 'b'
    assert (A.compute_next(X, letter) == X)
    return


def test_accept():
    assert (A.accept("aaaaaaaab") == True)
    assert (A.accept("aaaab") == True)
    assert (A.accept("") == False)
    return


def test_reachable_states():
    print(A.reachable_states())
    # assert ((A.reachable_states() == {0, 1, 2}) == True)
    A.add_state(4)
    assert ((4 in A.reachable_states()) == False)
    return


def test_is_empty():
    print(A.reachable_states())
    A.set_final(1)
    print(A.final)
    assert ((A.is_empty()) == False)
    # Automate sans état final:
    E = Automata(Sigma, states, trans, ini, set())
    assert ((E.is_empty()) == True)


def test_union():
    # Au vu de la fonction union, le nouvel automate créé a une structure d'états différente de l'automate de base.
    # On peut difficilement faire des tests sur les états accessibles etc mais on peut toujours tester sur leur nombre.
    for B in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
        for C in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
            assert (len(B.union(C).reachable_states()) <= len(B.reachable_states()) + len(C.reachable_states()))
            assert (len(B.union(C).ini) <= len(B.ini) + len(C.ini))


def test_intersection():
    for B in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
        for C in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
            assert (len(B.intersection(C).final) <= len(B.final))
            assert (len(B.intersection(C).final) <= len(C.final))


def test_trim():
    for B in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
        for C in [sample_automata.B1, sample_automata.B2, sample_automata.B3, sample_automata.B4]:
            assert (len(B.union(C).reachable_states()) >= len(B.reachable_states()) + len(C.reachable_states()))
            assert (len(B.union(C).ini) >= len(B.ini) + len(C.ini))
            assert (len(B.union(C).final) >= len(B.final) + len(C.final))


test_reachable_states()
test_is_empty()
test_union()
test_intersection()

print("A automata")
print(A)

print("A mirror automata")
print(A.mirror())
