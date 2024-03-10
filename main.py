import sys


class Transition:
    def __init__(self, state, next_state, symbol):
        self.state = state
        self.next_state = next_state
        self.symbol = symbol

    def __str__(self):
        return f'Transition(state: {self.state}, next_state: {self.next_state}, symbol: {self.symbol})'


class State:
    def __init__(self, state_id, start, valid):
        self.state_id = state_id
        self.start = start
        self.valid = valid

    def __str__(self):
        return f'State(state_id: {self.state_id}, start: {self.start}, valid: {self.valid})'


class Automata:
    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions

    def __str__(self):
        state_str = ', '.join(str(state) for state in self.states)
        transition_str = ', '.join(str(transition) for transition in self.transitions)
        return f'Automata(states: [{state_str}], transitions: [{transition_str}])'


# regex_f = open(sys.argv[1], "r")
# texts_f = open(sys.argv[2], "r")

regex_f = open("my_regex.txt", "r")
texts_f = open("my_retazce.txt", "r")

regex = [None] + [line.strip().split(',') for line in regex_f.readlines()]
texts = [line.split() for line in texts_f.readlines()]

automatas = [None]


def union(one, two):
    pass


def concat(one, two):
    pass


def iteration(id_ctr, automata):
    new_automata = Automata(automata.states.copy(), automata.transitions.copy())
    old_start = None
    new_start = State(id_ctr, 1, True)
    valid = [new_start]
    for state in automata.states:
        if state.start == 1:
            state.start = 0
            old_start = state
        if state.valid:
            valid.append(state)

    new_automata.states.append(new_start)

    for state in valid:
        new_transition = Transition(state, old_start, "")
        new_automata.transitions.append(new_transition)

    automatas.append(new_automata)


def create_automata(id_ctr, row):
    new_start = State(id_ctr, 1, False)
    id_ctr += 1
    new_valid = State(id_ctr, 0, True)
    id_ctr += 1
    new_transition = Transition(new_start, new_valid, row[0])
    new_automata = Automata([new_start, new_valid], [new_transition])
    automatas.append(new_automata)


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
                dictionaryOperations[operation](arguments[0], arguments[1])
        else:
            create_automata(id_ctr, row)
            id_ctr += 2

    for automata in automatas[1:]:
        print(automata)


app(0)
