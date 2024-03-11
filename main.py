import sys


class Transition:
    def __init__(self, from_state, to_state, symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol

    def __str__(self):
        return f'(form: {self.from_state.id()}, to: {self.to_state.id()}, symbol: {self.symbol})'

    def copy(self):
        return Transition(self.from_state, self.to_state, self.symbol)


class State:
    def __init__(self, state_id, start, accept):
        self.state_id = state_id
        self.start = start
        self.accept = accept

    def __str__(self):
        return f'(ID: {self.state_id}, start: {self.start}, accept: {self.accept})'

    def id(self):
        return f'{self.state_id}'

    def copy(self):
        return State(self.state_id, self.start, self.accept)


class Automata:
    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions

    def __str__(self):
        state_str = ', '.join(str(state) for state in self.states)
        transition_str = ', '.join(str(transition) for transition in self.transitions)
        return f'Automata(States: [{state_str}], Transitions: [{transition_str}])'

    def copy(self):
        copied_states = [state.copy() for state in self.states]
        copied_transitions = [transition.copy() for transition in self.transitions]
        return Automata(copied_states, copied_transitions)


# regex_f = open(sys.argv[1], "r")
# texts_f = open(sys.argv[2], "r")

regex_f = open("regex1.txt", "r")
texts_f = open("my_retazce.txt", "r")

regex = [None] + [line.strip().split(',') for line in regex_f.readlines()]
texts = [line.split() for line in texts_f.readlines()]

automatas = [None]


def union(id_ctr, a_l, a_r):
    automata_left = a_l.copy()
    automata_right = a_r.copy()
    new_automata = Automata(automata_left.states + automata_right.states,
                            automata_left.transitions + automata_right.transitions)
    left_start = None
    right_start = None
    for state in automata_left.states:
        if state.start:
            left_start = state
            state.start = False

    for state in automata_right.states:
        if state.start:
            right_start = state
            state.start = False

    new_start = State(id_ctr, True, False)
    id_ctr += 1
    transitions = [Transition(new_start, left_start, ""), Transition(new_start, right_start, "")]
    new_automata.states.append(new_start)
    new_automata.transitions += transitions
    automatas.append(new_automata)
    return 1


def concat(id_ctr, a_l, a_r):
    automata_left = a_l.copy()
    automata_right = a_r.copy()
    new_automata_states = []
    new_automata_transitions = automata_left.transitions + automata_right.transitions
    accept_states_left = []
    start_right = None
    highest_left_id = max([state.state_id for state in automata_left.states])
    index = 1

    # Remove accept from left automata, in new automata
    for state in automata_left.states:
        if state.accept:
            state.accept = False
            accept_states_left.append(state)
        new_automata_states.append(state)

    # Change IDs in right automata, in new automata
    # Also remove start from right automata, in new automata
    map_new_id_to_states = {}
    for state in automata_right.states:
        old_id = state.state_id
        state.state_id = highest_left_id + index
        map_new_id_to_states[old_id] = state
        index += 1
        if state.start:
            start_right = state
            state.start = False
        new_automata_states.append(state)

    # Update transitions in right automata, in new automata
    for transition in automata_right.transitions:
        transition.from_state = map_new_id_to_states[transition.from_state.state_id]
        transition.to_state = map_new_id_to_states[transition.to_state.state_id]

    for accepts_state in accept_states_left:
        new_automata_transitions.append(Transition(accepts_state, start_right, ""))

    new_automata = Automata(new_automata_states, new_automata_transitions)
    automatas.append(new_automata)
    return 0


def iteration(id_ctr, automata):
    new_automata = automata.copy()
    old_start = None
    new_start = State(id_ctr, True, True)
    accept_states = [new_start]

    for state in new_automata.states:
        if state.start:
            state.start = False
            old_start = state
        if state.accept:
            accept_states.append(state)

    new_automata.states.append(new_start)

    for accept_state in accept_states:
        new_automata.transitions.append(Transition(accept_state, old_start, ""))

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
                result = dictionaryOperations[operation](id_ctr, automatas[int(arguments[0])],
                                                         automatas[int(arguments[1])])
                if result == 1:
                    id_ctr += 1
        else:
            id_ctr = id_ctr + 2 if create_automata(id_ctr, row) == 2 else id_ctr + 1

    for automata in automatas[1:]:
        print(automata)


app(0)
