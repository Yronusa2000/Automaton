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
    # assert(A.is_complete() == False)
    # assert(D.is_complete() == True)
    return


def test_compute_next():
    X = {1,2}
    letter = 'a'
    Y = {1}
    assert(A.compute_next(X,letter) == Y)
    letter = 'b'
    assert(A.compute_next(X,letter) == X)
    return


def test_accept():
    # à compléter
    return
