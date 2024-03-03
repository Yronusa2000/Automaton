"""

A class to deal with finite-state automata
P.-A. Reynier, Feb. 2023
Algorithms implemented by Marin Feb. 2024 :
    - is_deterministic()
    - is_complete()
    - compute_next()
    - accept()
    - compute_next

"""
import copy


class Automata:
    def __init__(self, alphabet, states, trans, ini, final):
        """
        :param alphabet: set of symbols
        :param states: set of states
        :param trans: dictionary giving transitions
        :param ini: set of initial states
        :param final: set of final states
        """
        self.alphabet = alphabet
        self.states = states
        self.trans = trans
        self.ini = ini
        self.final = final

    def add_state(self, state):
        """
        :param state: state to be added
        :return: 1 if state successfuly added, 0 otw
        """
        if state in self.states:
            print("Error while adding state: already present")
            return 0
        try:
            self.states.add(state)
        except:
            print("Error while adding state: set error")
            return 0
        return 1

    def add_transition(self, source, label, target):
        """
        :param source: source state
        :param label: label of the transition
        :param target: target state
        :return: 1 if transition successfuly added, 0 otw
        """
        if source not in self.states:
            print("Error while adding transition: source state not in states")
            return 0
        if target not in self.states:
            print("Error while adding transition: target state not in states")
            return 0
        if label not in self.alphabet:
            print("Error while adding transition: label not in alphabet")
            return 0
        # source is not a key of self.trans
        if source not in self.trans:
            self.trans[source] = {}
            self.trans[source][label] = {target}
        # source is a key of self.trans
        else:
            # label is not a key of self.trans[source]
            if label not in self.trans[source]:
                self.trans[source][label] = {target}
            # label is a key of self.trans[source]
            else:
                self.trans[source][label].add(target)
        return 1

    def set_initial(self, state):
        """
        :param state: a state
        :return: 1 if modification suceeded, 0 otw
        """
        if state in self.states:
            self.ini.add(state)
            return 1
        else:
            return 0

    def set_final(self, state):
        """
        :param state: a state
        :return: 1 if modification suceeded, 0 otw
        """
        if state in self.states:
            self.final.add(state)
            return 1
        else:
            return 0

    def __str__(self):
        """ Overrides print function """
        res = "Display Automaton\n"
        res += "Alphabet: " + str(self.alphabet) + "\n"
        res += "Set of states: " + str(self.states) + "\n"
        res += "Initial states " + str(self.ini) + "\n"
        res += "Final states " + str(self.final) + "\n"
        res += "Transitions:" + "\n"
        for source in self.trans:
            for label in self.trans[source]:
                for target in self.trans[source][label]:
                    res += "Transition from " + str(source) + " to " + str(target) + " labelled by " + str(label) + "\n"
        return res

    def is_deterministic(self, verbose):
        """
        :param verbose: a boolean to return or not the reason why the automaton is non-deterministic.
        :return: True if the automaton is deterministic, False otherwise

        """

        # Checks the number of initial states
        if len(self.ini) != 1:
            if (verbose): print("Too many initial states")
            return False
        # Loop over source states
        for source in self.trans:
            # Loop over labels
            for label in self.trans[source]:
                # Check whether there are two transitions with same
                # source state and label
                if len(self.trans[source][label]) > 1:
                    if (verbose): print("too many outgoing transitions from 0 labelled by " + label)
                    return False
        return True

    def is_complete(self, verbose):
        """
        :param verbose: a boolean to return or not the reason why the automaton is non-complete.
        :return: True if the automaton is complete, False otherwise

        """

        # Loop over source states
        for source in self.trans:
            # Loop over alphabet
            for symbol in self.alphabet:
                # Check whether there isn't a transition from source to another state, using symbol.
                # Each symbol of the alphabet should appear at least one time.
                if symbol not in self.trans.get(source, {}):
                    if (verbose): print("Missing transition {} at {}".format(symbol, source))
                    return False
        return True

    def compute_next(self, X, sigma):
        """
        :param X: set of states
        :param sigma: symbol of the alphabet
        :return: a set of states corresponding to one-step successors of X by reading sigma
        """
        res = set()
        # Iterate over given states (in X)
        for source in X:
            # Test if there's a transition from X, with sigma
            if source in self.trans:
                if sigma in self.trans[source]:
                    for s in self.trans[source][sigma]:
                        res.add(s)
                        # Add the state reached through sigma

        return res

    def accept(self, word):
        """
        :param word: string on the alphabet
        :return: True if word is accepted, False otw.
        """

        F = self.final  # Define the set of final states
        X = self.ini  # Start with the initial state

        # For epsilon, we simply check that there's at least one final states is an initial one.
        if word == "":
            if X.isdisjoint(F):
                return True
            else:
                return False
        # For other words, we iterate through letters:
        for letter in word:
            X.update(self.compute_next(X, letter))
        if X.intersection(F):
            return True  # The word is accepted
        else:
            return False  # The word is not accepted

    def reachable_states(self):
        """
        Computes the of states reachable from the initial ones
        :return: the set of reachable states
        """
        X = self.ini
        Y = set()
        while (X != Y):
            Y.update(X)
            for letter in self.alphabet:
                print("before")
                print(X)
                X.update(X.union(self.compute_next(X, letter)))
                print("after")
                print(X)
        return X

    def is_empty(self):
        """
        Checks whether   the automaton accepts no word. Proceeds by checking
        whether there exists a final state reachable from an initial one.
        :return: True if the language of the automaton is empty, False otherwise
        """
        if self.final & self.reachable_states():
            print()
            return False
        else:
            return True

    def copy(self):
        """
        :return: A new automaton which is a deep copy of the automaton
        """
        new_alphabet = self.alphabet.copy()
        new_states = self.states.copy()
        new_trans = copy.deepcopy(self.trans)
        new_ini = self.ini.copy()
        new_final = self.final.copy()
        return Automata(new_alphabet, new_states, new_trans, new_ini, new_final)

    def union(self, other):
        """
        :param other: an automaton
        :return: a new automaton whose language is the union
        """

        #
        new_states = {(s, 0) for s in self.states} | {(s, 1) for s in other.states}
        new_trans = {}
        for state in new_states:
            if not state[1] and state[0] in self.trans:
                new_trans[state] = {label: {s for s in new_states if s[1] == 0 and s[0] in self.trans[state[0]][label]}
                                    for
                                    label in self.trans[state[0]]}
            elif state[1] and state[0] in other.trans:
                new_trans[state] = {label: {s for s in new_states if s[1] == 1 and s[0] in other.trans[state[0]][label]}
                                    for
                                    label in other.trans[state[0]]}
                # Note: cette optimisation du code provient de Paul, ma version était beaucoup plus longue (3 ou 4x).

        new_ini = set()
        new_final = set()

        for state in new_states:
            if state[0] in self.ini or state[0] in other.ini:
                new_ini.add(state)
        for state in new_states:
            if state[0] in self.final or state[0] in other.final:
                new_final.add(state)

        return Automata(self.alphabet, new_states, new_trans, new_ini, new_final)

    def intersection(self, other):
        """
        Compute the intersection of two automatas.

        :param other: Automata to intersect with
        :return: New Automata representing the intersection
        """

        new_alphabet = self.alphabet
        new_states = {(s1, s2) for s1 in self.states for s2 in other.states}
        new_trans = {}

        for state_pair in new_states:
            new_trans[state_pair] = {}
            for symbol in new_alphabet:
                transitions_self = self.trans.get(state_pair[0], {}).get(symbol, set())
                transitions_other = other.trans.get(state_pair[1], {}).get(symbol, set())
                new_trans[state_pair][symbol] = {(s1, s2) for s1 in transitions_self for s2 in transitions_other}

        new_ini = {(self_ini, other_ini) for self_ini in self.ini for other_ini in other.ini}
        new_final = {(self_final, other_final) for self_final in self.final for other_final in other.final}

        return Automata(new_alphabet, new_states, new_trans, new_ini, new_final)

    def complement_DFA(self):
        """
        Assumes the input automaton is deterministic and complete
        :return: modifies the automaton to accept the complement language
        """
        temp = self.final
        self.final = self.ini
        self.ini = temp
        return

    def check_inclusion_DFA(self, other):
        """
        checks whether the language of the automaton is included
        in that of the other automaton (assumed deterministic and complete)
        :param other: an automaton which is deterministic and complete
        :return: True if inclusion holds, False otherwise
        """
        complement_other = other.complement_DFA().copy
        product = self.intersection(complement_other)
        return product.is_empty()

    def check_equivalence_DFA(self, other):
        """
        checks whether the language of the automaton is equal
        to that of the other automaton.
        Assumes both automata are deterministic and complete.
        :param other: an automaton which is deterministic and complete
        :return: True if equality holds, False otherwise
        """

        return self.check_inclusion_DFA(other) and other.check_inclusion_DA(self)

    def mirror(self):
        """
        Modifies the automaton so that it accepts the mirror
        image of the language (swaps direction of transitions)
        :return: None
        """

        # Invert the transitions
        mirror_trans = {state: {symbol: set() for symbol in self.alphabet} for state in self.states}
        for state, transitions in self.trans.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    mirror_trans[next_state][symbol].add(state)

        return Automata(self.alphabet, self.states, mirror_trans, self.final, self.ini)

    def co_reachable_states(self):
        """
        :return: set of states that are co-reachable from some final state
        """
        copy = self.copy()
        copy.mirror()
        return copy.reachable_states()

    def useful_states(self):
        """
        :return: set of states that are useful
        """
        return self.co_reachable_states().intersection(self.reachable_states())

    def trim(self):
        useful = self.useful_states()

        # Les nouveaux états sont l'intersection entre les états, et les états utiles.
        new_states = useful.intersection(self.states)
        # De même les transitions sont les transitions entre les états utiles de l'automate.
        new_trans = {
            state: {symbol: next_states.intersection(new_states) for symbol, next_states in transitions.items()} for
            state, transitions in self.trans.items() if state in useful}
        new_ini = self.ini.intersection(new_states)
        new_final = self.final.intersection(new_states)

        return Automata(self.alphabet, new_states, new_trans, new_ini, new_final)
