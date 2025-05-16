import random
from collections import deque

class DFA:
    def __init__(self, min=16, max=64, debug=False, seed=None):
        self._rng = random.Random(seed)

        self.n = self._rng.randint(min, max)
        self.states = list(range(self.n))

        self.accepting = {state: self._rng.choice([True, False]) for state in self.states}

        self.transition = {
            state: {
                'a': self._rng.randint(0, self.n - 1),
                'b': self._rng.randint(0, self.n - 1)
            } for state in self.states
        }

        self.start_state = self._rng.choice(self.states)

        if debug:   
            self.print_summary()

    @classmethod
    def empty_dfa(cls):
        obj = cls(min=1, max=1)  # Dummy call to satisfy init
        obj.n = 0
        obj.states = []
        obj.accepting = {}
        obj.transition = {}
        obj.start_state = None
        return obj


    def bfs_depth(self):
        distances = {state: float('inf') for state in self.states}
        distances[self.start_state] = 0

        queue = deque([self.start_state])
        visited = {self.start_state}

        while queue:
            current = queue.popleft()

            for symbol in ['a', 'b']:
                next_state = self.transition[current][symbol]
                if next_state not in visited:
                    distances[next_state] = distances[current] + 1
                    visited.add(next_state)
                    queue.append(next_state)

        reachable_distances = [d for d in distances.values() if d != float('inf')]
        return max(reachable_distances) if reachable_distances else 0

    def get_reachable_states(self):
        visited = set()
        queue = deque([self.start_state])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for symbol in ['a', 'b']:
                    queue.append(self.transition[current][symbol])
        return visited

    def get_useful_states(self):
        reverse_graph = {s: [] for s in self.states}
        for state in self.states:
            for symbol in ['a', 'b']:
                next_state = self.transition[state][symbol]
                reverse_graph[next_state].append(state)

        useful = set()
        stack = [s for s in self.states if self.accepting[s]]

        while stack:
            s = stack.pop()
            if s not in useful:
                useful.add(s)
                stack.extend(reverse_graph[s])

        return useful

    def prune(self):
        reachable = self.get_reachable_states()
        useful = self.get_useful_states()
        valid = reachable & useful

        if not valid:
            # No valid states remain; reset to empty DFA
            self.states = []
            self.n = 0
            self.accepting = {}
            self.transition = {}
            self.start_state = None
            return

        # Create a trap state ID (after remapping valid states)
        state_mapping = {old: new for new, old in enumerate(sorted(valid))}
        trap_state_id = len(state_mapping)

        # Update state list and count (include trap if needed later)
        self.states = list(state_mapping.values())
        self.n = len(self.states)  # might be updated again if trap is added

        # Remap accepting states
        self.accepting = {
            state_mapping[s]: self.accepting[s]
            for s in valid
        }

        # Remap transitions, check for missing ones
        new_transitions = {}
        trap_needed = False

        for s in valid:
            new_s = state_mapping[s]
            new_transitions[new_s] = {}
            for symbol in ['a', 'b']:
                t = self.transition[s][symbol]
                if t in valid:
                    new_transitions[new_s][symbol] = state_mapping[t]
                else:
                    trap_needed = True
                    new_transitions[new_s][symbol] = trap_state_id

        # If needed, define the trap state
        if trap_needed:
            self.states.append(trap_state_id)
            self.n += 1
            self.accepting[trap_state_id] = False
            new_transitions[trap_state_id] = {'a': trap_state_id, 'b': trap_state_id}

        self.transition = new_transitions
        self.start_state = state_mapping[self.start_state]



    def hopcroft_minimization(self):
        alphabet = ['a', 'b']
        states = set(self.states)

        accepting_states = frozenset(state for state in states if self.accepting[state])
        non_accepting_states = frozenset(states - accepting_states)

        P = []
        if accepting_states:
            P.append(accepting_states)
        if non_accepting_states:
            P.append(non_accepting_states)

        W = set()
        if accepting_states and non_accepting_states:
            W.add(accepting_states if len(accepting_states) <= len(non_accepting_states) else non_accepting_states)
        elif accepting_states:
            W.add(accepting_states)
        elif non_accepting_states:
            W.add(non_accepting_states)

        while W:
            A = W.pop()
            for symbol in alphabet:
                X = frozenset(s for s in states if self.transition[s][symbol] in A)
                partition_changes = []
                for i, Y in enumerate(P):
                    intersection = Y & X
                    difference = Y - X
                    if intersection and difference:
                        partition_changes.append((i, Y, intersection, difference))
                for i, Y, intersection, difference in reversed(partition_changes):
                    P.pop(i)
                    P.append(intersection)
                    P.append(difference)
                    if Y in W:
                        W.discard(Y)
                        W.add(intersection)
                        W.add(difference)
                    else:
                        W.add(intersection if len(intersection) <= len(difference) else difference)

        state_to_new_state = {state: new_state for new_state, partition in enumerate(P) for state in partition}

        minimized_dfa = DFA.empty_dfa()
        minimized_dfa.n = len(P)
        minimized_dfa.states = list(range(len(P)))

        minimized_dfa.accepting = {
            new_state: any(self.accepting[state] for state in partition)
            for new_state, partition in enumerate(P)
        }

        minimized_dfa.transition = {
            new_state: {
                symbol: state_to_new_state[self.transition[next(iter(partition))][symbol]]
                for symbol in alphabet
            } for new_state, partition in enumerate(P)
        }

        minimized_dfa.start_state = state_to_new_state[self.start_state]
        return minimized_dfa

    def accepts(self, input_string):
        state = self.start_state
        for symbol in input_string:
            if symbol not in self.transition[state]:
                return False
            state = self.transition[state][symbol]
        return self.accepting.get(state, False)

    def print_summary(self):
        print(f"\n--- DFA Summary ---")
        print(f"Number of states: {self.n}")
        print(f"Start state: {self.start_state}")
        print("Accepting states:")
        for state in sorted(k for k, v in self.accepting.items() if v):
            print(f"  State {state}")
        print("Transitions:")
        for state in sorted(self.states):
            print(f"  State {state}: a → {self.transition[state]['a']}, b → {self.transition[state]['b']}")
