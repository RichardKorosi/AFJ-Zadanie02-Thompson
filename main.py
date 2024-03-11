import sys


# TODO: Treba sa pozriet na to ze po concate maju viacere States rovnake ID


class Transition:
    def __init__(self, from_state, to_state, symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol

    def __str__(self):
        return f'(form: {self.from_state.id()}, to: {self.to_state.id()}, symbol: {self.symbol})'


class State:
    def __init__(self, state_id, start, accept):
        self.state_id = state_id
        self.start = start
        self.accept = accept

    def __str__(self):
        return f'(ID: {self.state_id}, start: {self.start}, accept: {self.accept})'

    def id(self):
        return f'{self.state_id}'


class Automata:
    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions

    def __str__(self):
        state_str = ', '.join(str(state) for state in self.states)
        transition_str = ', '.join(str(transition) for transition in self.transitions)
        return f'Automata(States: [{state_str}], Transitions: [{transition_str}])'


# regex_f = open(sys.argv[1], "r")
# texts_f = open(sys.argv[2], "r")

regex_f = open("my_regex.txt", "r")
texts_f = open("my_retazce.txt", "r")

regex = [None] + [line.strip().split(',') for line in regex_f.readlines()]
texts = [line.split() for line in texts_f.readlines()]

automatas = [None]


def union(one, two):
    pass


def concat(id_ctr, automata_left, automata_right):
    new_automata_states = []
    new_automata_transitions = automata_left.transitions.copy() + automata_right.transitions.copy()
    accepts_left = []
    start_right = None

    for state in automata_left.states.copy():
        if state.accept:
            accepts_left.append(state)
            state.accept = False
        new_automata_states.append(state)

    for state in automata_right.states:
        new_automata_states.append(state)

    for state in automata_right.states:
        if state.start:
            start_right = state
            state.start = False

    for state in accepts_left:
        new_transition = Transition(state, start_right, "")
        new_automata_transitions.append(new_transition)

    new_automata = Automata(new_automata_states, new_automata_transitions)
    automatas.append(new_automata)


def iteration(id_ctr, automata):
    new_automata = Automata(automata.states.copy(), automata.transitions.copy())
    old_start = None
    new_start = State(id_ctr, True, True)
    accept = [new_start]
    for state in automata.states:
        if state.start:
            state.start = False
            old_start = state
        if state.accept:
            accept.append(state)

    new_automata.states.append(new_start)

    for state in accept:
        new_transition = Transition(state, old_start, "")
        new_automata.transitions.append(new_transition)

    automatas.append(new_automata)


def create_automata(id_ctr, row):
    if len(row[0]) == 0:
        new_start = State(id_ctr, True, True)
        new_automata = Automata([new_start], [])
        automatas.append(new_automata)
        id_ctr += 1
        return 1
    else:
        new_start = State(id_ctr, True, False)
        id_ctr += 1
        new_accept = State(id_ctr, False, True)
        id_ctr += 1
        new_transition = Transition(new_start, new_accept, row[0])
        new_automata = Automata([new_start, new_accept], [new_transition])
        automatas.append(new_automata)
        return 2


dictionaryOperations = {
    "I": iteration,
    "U": union,
    "C": concat,
}


def app(id_ctr):
    for i in range(1, len(regex)):
        row = regex[i]
        operation = row[0]
        arguments = row[1:]
        if operation in dictionaryOperations:
            if len(arguments) == 1:
                pass
                dictionaryOperations[operation](id_ctr, automatas[int(arguments[0])])
                id_ctr += 1
            elif len(arguments) == 2:
                dictionaryOperations[operation](id_ctr, automatas[int(arguments[0])], automatas[int(arguments[1])])
        else:
            id_ctr = id_ctr + 2 if create_automata(id_ctr, row) == 2 else id_ctr + 1

    for automata in automatas[1:]:
        print(automata)


app(0)
