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
        return self.state_id

    def copy(self):
        return State(self.state_id, self.start, self.accept)


class NFAutomata:
    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions

    def __str__(self):
        state_str = ', '.join(str(state) for state in self.states)
        transition_str = ', '.join(str(transition) for transition in self.transitions)
        return f'NFAutomata(States: [{state_str}], Transitions: [{transition_str}])'

    def copy(self):
        copied_states = [state.copy() for state in self.states]
        copied_transitions = [transition.copy() for transition in self.transitions]
        return NFAutomata(copied_states, copied_transitions)


class DFAutomata:
    def __init__(self, nfa_states, nfa_transitions):
        self.nfa_states = nfa_states
        self.nfa_transitions = nfa_transitions
        self.nfa_accept_states = [state for state in nfa_states if state.accept]
        self.nfa_start_state = [state for state in nfa_states if state.start][0]
        self.states = []
        self.transitions = []

    def __str__(self):
        state_str = ', '.join(str(state) for state in self.states)
        transition_str = ', '.join(str(transition) for transition in self.transitions)
        return f'DFAutomata(States: [{state_str}], Transitions: [{transition_str}])'


# regex_f = open(sys.argv[1], "r")
# texts_f = open(sys.argv[2], "r")

regex_f = open("regex4.txt", "r")
texts_f = open("my_retazce.txt", "r")

regex = [None] + [line.strip().split(',') for line in regex_f.readlines()]
texts = [line.split() for line in texts_f.readlines()]
nf_automatas = [NFAutomata([], [])]
df_automatas = []


def union(a_l, a_r):
    automata_left = a_l.copy()
    automata_right = a_r.copy()
    new_automata_states = []
    new_automata_transitions = automata_left.transitions + automata_right.transitions
    highest_left_id = max([state.state_id for state in automata_left.states])
    index = 1

    left_start = None
    right_start = None

    for state in automata_left.states:
        if state.start:
            left_start = state
            state.start = False
        new_automata_states.append(state)

    map_new_id_to_states = {}
    for state in automata_right.states:
        old_id = state.state_id
        state.state_id = highest_left_id + index
        map_new_id_to_states[old_id] = state
        index += 1
        if state.start:
            right_start = state
            state.start = False
        new_automata_states.append(state)

    # Update transitions in right automata, in new automata
    for transition in automata_right.transitions:
        transition.from_state = map_new_id_to_states[transition.from_state.state_id]
        transition.to_state = map_new_id_to_states[transition.to_state.state_id]

    new_start_id = highest_left_id + index
    new_start = State(new_start_id, True, False)
    transitions = [Transition(new_start, left_start, ""), Transition(new_start, right_start, "")]
    new_automata_states.append(new_start)
    new_automata_transitions += transitions
    new_automata = NFAutomata(new_automata_states, new_automata_transitions)
    nf_automatas.append(new_automata)
    return 1


def concat(a_l, a_r):
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

    new_automata = NFAutomata(new_automata_states, new_automata_transitions)
    nf_automatas.append(new_automata)
    return 0


def iteration(a):
    automata = a.copy()
    new_automata_states = []
    new_automata_transitions = automata.transitions
    highest_id = max([state.state_id for state in automata.states])
    index = 1
    new_start = State(highest_id + index, True, True)
    old_start = None
    accept_states = [new_start]

    for state in automata.states:
        if state.start:
            old_start = state
            state.start = False
        if state.accept:
            accept_states.append(state)
        new_automata_states.append(state)

    new_automata_states.append(new_start)

    for accept_state in accept_states:
        new_automata_transitions.append(Transition(accept_state, old_start, ""))

    new_automata = NFAutomata(new_automata_states, new_automata_transitions)
    nf_automatas.append(new_automata)
    return 0


dictionaryOperations = {
    "I": iteration,
    "U": union,
    "C": concat,
}


def create_nfautomata(row):
    id_ctr = 0
    if len(row[0]) == 0:
        new_start = State(id_ctr, True, True)
        new_automata = NFAutomata([new_start], [])
        nf_automatas.append(new_automata)
        id_ctr += 1
        return 1
    else:
        new_start = State(id_ctr, True, False)
        id_ctr += 1
        new_accept = State(id_ctr, False, True)
        id_ctr += 1
        new_transition = Transition(new_start, new_accept, row[0])
        new_automata = NFAutomata([new_start, new_accept], [new_transition])
        nf_automatas.append(new_automata)
        return 2


def create_dfautomata():
    nfa = nf_automatas[-1]
    nfa_states = nfa.states.copy()
    nfa_transitions = nfa.transitions.copy()
    dfa_automata = DFAutomata(nfa_states, nfa_transitions)

    print(dfa_automata)

    while True:
        closure = []
        if len(dfa_automata.states) == 0:
            closure.append((dfa_automata.nfa_start_state.id(), False))
        while any(not tup[1] for tup in closure):
            for tup in closure:
                if not tup[1]:
                    state_id = tup[0]
                    for transition in dfa_automata.nfa_transitions:
                        if transition.from_state.state_id == state_id and transition.symbol == "":
                            if not any(tup[0] == transition.to_state.id() for tup in closure):
                                closure.append((transition.to_state.id(), False))
                    closure[closure.index(tup)] = (state_id, True)


def app():
    for i in range(1, len(regex)):
        row = regex[i]
        operation = row[0]
        arguments = row[1:]
        if operation in dictionaryOperations:
            if len(arguments) == 1:
                pass
                dictionaryOperations[operation](nf_automatas[int(arguments[0])])
            elif len(arguments) == 2:
                dictionaryOperations[operation](nf_automatas[int(arguments[0])], nf_automatas[int(arguments[1])])
        else:
            create_nfautomata(row)

    for automata in nf_automatas[1:]:
        print(automata)

    create_dfautomata()


app()
