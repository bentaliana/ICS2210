import random
from collections import deque

class DFA:
    # Question 1
    def __init__(self, min=16, max=64, debug=False, seed=None):
        # Included random seed for reproducbility
        if seed is not None:
            random.seed(seed)

        # Question 1a
        self.n = random.randint(min, max)
        self.states = list(range(self.n))

        # Question 1b
        # True = accepting state, False = non accepting state
        self.accepting = {state: random.choice([True, False]) for state in self.states}
        
        # Question 1c
        self.transition = {
            state: {
                'a': random.randint(0, self.n - 1),
                'b': random.randint(0, self.n - 1)
            } for state in self.states
        }
        
        # Question 1d
        self.start_state = random.choice(self.states)

        # Question 1 summary/debugging info 
        if debug:
            self.print_summary()


    # Question 2 
    def bfs_depth(self):
        # Setting unexplored states to infinity
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

        # Checking for reachable states
        reachable_distances = [d for d in distances.values() if d != float('inf')]

        return max(reachable_distances) if reachable_distances else 0
    
    # Print a summary of the DFA for debugging purposes
    def print_summary(self):
        print(f"\n--- DFA Summary ---")
        print(f"Number of states (1a): {self.n}")
        print(f"Start state (1d): {self.start_state}")
        print("Accepting states (1b):")
        for state, is_accepting in self.accepting.items():
            if is_accepting:
                print(f"State {state}")
        print("Transitions (1c):")
        for state in self.states:
            print(f"State {state}: 'a' -> {self.transition[state]['a']}, 'b' -> {self.transition[state]['b']}")

    # Question 3 : Hopcroft's algorithm for DFA minimization
    def hopcroft_minimization(self):
        alphabet = ['a', 'b']
        states = set(self.states)

        # Initializing accepting , non accepting states
        accepting_states = frozenset(state for state in states if self.accepting[state])
        non_accepting_states = frozenset(states - accepting_states)

        # Parition list
        P = []

        if accepting_states:
            P.append(accepting_states)
        if non_accepting_states:
            P.append(non_accepting_states)


        # Working set 
        W = set()

        if accepting_states and non_accepting_states:
            W.add(accepting_states if len(accepting_states) <= len(non_accepting_states) else non_accepting_states)
        elif accepting_states:
            W.add(accepting_states)
        elif non_accepting_states:
            W.add(non_accepting_states)


        # While W is not empty
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
                        # Always add the smaller parition for efficiency
                        W.add(intersection if len(intersection) <= len(difference) else difference)

        state_to_new_state = {state: new_state for new_state, partition in enumerate(P) for state in partition}

        minimized_dfa = DFA(min=1, max=1)
        minimized_dfa.n = len(P)
        minimized_dfa.states = list(range(len(P)))

        # Accepting states
        minimized_dfa.accepting = {
            new_state: any(self.accepting[state] for state in partition)
            for new_state, partition in enumerate(P)
        }

        # Transitions
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
            if symbol not in ['a', 'b']:
                return False
            state = self.transition[state][symbol]
        return self.accepting[state]
