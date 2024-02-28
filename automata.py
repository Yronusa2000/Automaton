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

import main


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
        while (Y != Y):
            Y.update(X)
            for letter in self.alphabet:
                print("before")
                print(X)
                X.update(X + self.compute_next(X, letter))
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
        Computes an automaton whose language is the union of
        two automata defined over the same alphabet.
        :param other: an instance of the class Automata
        :return: a new instance of the class Automata
        """
        return

    def intersection(self, other):
        """
        Computes an automaton whose language is the intersection of
        two automata defined over the same alphabet. It computes
        the product of the two automata
        :param other: an instance of the class Automata
        :return: a new instance of the class Automata, obtained as the product
        of the automaton with automaton other
        """
        return main.A

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
