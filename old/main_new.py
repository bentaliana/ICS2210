
import random 
from collections import deque # Double ended queue for BFS

class DFA: 
    # Question 1
    def __init__(self , min=16, max=64, debug=False, seed=None): 

        # Included random seed for test reproducibility
        if seed is not None:
            random.seed(seed)

        # Question 1a
        self.n = random.randint(min, max) 
        self.states = list(range(self.n))

        # Question 1b
        # True = accepting state, False = non-accepting state
        self.accepting = {state : random.choice([True, False]) for state in self.states} 

        # Question 1c
        self.transition = {
            state: {
                'a' : random.randint(0, self.n - 1), # Randomly generating transition for 'a'
                'b' : random.randint(0, self.n - 1)  # Randomly generating transition for 'b'
            }
            for state in self.states
        }

        # Question 1d
        self.start_state = random.choice(self.states) 

        # Question 1 summary/debug
        if debug:
            self.print_summary()


    # Question 2
    def depth(self):
        # Initialize distances to infinity (except start state)
        distances = {state: float('inf') for state in self.states}
        distances[self.start_state] = 0
        
        # Use BFS to find shortest paths
        queue = deque([self.start_state])
        visited = {self.start_state}
        
        while queue:
            current = queue.popleft()
            
            # For each symbol in our alphabet
            for symbol in ['a', 'b']:
                next_state = self.transition[current][symbol]
                
                if next_state not in visited:
                    distances[next_state] = distances[current] + 1
                    visited.add(next_state)
                    queue.append(next_state)
        
        # Filter out unreachable states (still infinity)
        reachable_distances = [d for state, d in distances.items() if d != float('inf')]
        
        # Return max depth (0 if only start state is reachable)
        return max(reachable_distances) if reachable_distances else 0
    
    # Print summary of the DFA for debugging purposes
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
            a_target = self.transition[state]['a']
            b_target = self.transition[state]['b']
            print(f"State {state}: 'a' -> {a_target}, 'b' -> {b_target}")


    # Question 3 : Hopcroft's Algorithm for DFA Minimization
    def minimize(self):
        alphabet = ['a', 'b']
        states = set(self.states)
        
        # Initial partition: accepting and non-accepting states
        accepting_states = frozenset(state for state in states if self.accepting[state])
        non_accepting_states = frozenset(state for state in states if not self.accepting[state])
        
        # Initial partition
        P = []
        if accepting_states:
            P.append(accepting_states)
        if non_accepting_states:
            P.append(non_accepting_states)
        
        # Waiting set (start with smaller partition for efficiency)
        W = set()
        if accepting_states and non_accepting_states:
            W.add(accepting_states if len(accepting_states) <= len(non_accepting_states) else non_accepting_states)
        elif accepting_states:
            W.add(accepting_states)
        elif non_accepting_states:
            W.add(non_accepting_states)
        
        # Refine partitions until no more refinements can be made
        while W:
            A = W.pop()
            
            # For each symbol in the alphabet
            for symbol in alphabet:
                # States that lead to A via symbol
                X = frozenset(s for s in states if self.transition[s][symbol] in A)
                
                # Partitions to split based on X
                partition_changes = []
                
                # Check each existing partition
                for i, Y in enumerate(P):
                    # States in Y that lead to A via symbol
                    intersection = Y & X
                    # States in Y that don't lead to A via symbol
                    difference = Y - X
                    
                    # If Y is split by X
                    if intersection and difference:
                        partition_changes.append((i, Y, intersection, difference))
                
                # Apply all changes to the partition
                for i, Y, intersection, difference in reversed(partition_changes):
                    # Remove the original partition
                    P.pop(i)
                    # Add the two new partitions
                    P.append(intersection)
                    P.append(difference)
                    
                    # Update the waiting set
                    if Y in W:
                        W.discard(Y)
                        W.add(intersection)
                        W.add(difference)
                    else:
                        # Always add the smaller partition for efficiency
                        W.add(intersection if len(intersection) <= len(difference) else difference)
        
        # Create a mapping from original states to new states
        state_to_new_state = {}
        for new_state, partition in enumerate(P):
            for state in partition:
                state_to_new_state[state] = new_state
        
        # Create the minimized DFA
        minimized_dfa = DFA(min=1, max=1)  # Create minimal DFA with dummy parameters
        minimized_dfa.n = len(P)
        minimized_dfa.states = list(range(len(P)))
        
        # Set accepting states
        minimized_dfa.accepting = {
            new_state: any(self.accepting[state] for state in partition)
            for new_state, partition in enumerate(P)
        }
        
        # Set transitions
        minimized_dfa.transition = {}
        for new_state, partition in enumerate(P):
            # Take any representative from the partition (all are equivalent)
            representative = next(iter(partition))
            minimized_dfa.transition[new_state] = {
                symbol: state_to_new_state[self.transition[representative][symbol]]
                for symbol in alphabet
            }
        
        # Set start state
        minimized_dfa.start_state = state_to_new_state[self.start_state]
        
        return minimized_dfa
    
    # TESTING FUNCTION 
    def accepts(self, input_string):
        state = self.start_state
        for symbol in input_string:
            if symbol not in ['a', 'b']:
                return False  # Invalid 
            state = self.transition[state][symbol]
        return self.accepting[state]


# TESTING FUNCTIONS 
def bfs_edge_cases():
    print("\n--- Testing BFS Edge Cases ---")

    # DFA with Unreachable State
    dfa = DFA()
    dfa.n = 3
    dfa.states = [0, 1, 2]
    dfa.accepting = {0: False, 1: True, 2: True}
    dfa.transition = {
        0: {'a': 1, 'b': 1},
        1: {'a': 0, 'b': 0},
        2: {'a': 2, 'b': 2}  # Unreachable
    }
    dfa.start_state = 0
    depth = dfa.depth()
    print(f"DFA with Unreachable State -> Depth (should ignore state 2): {depth}")

    # Cyclic DFA
    dfa = DFA()
    dfa.n = 3
    dfa.states = [0, 1, 2]
    dfa.accepting = {0: False, 1: False, 2: True}
    dfa.transition = {
        0: {'a': 1, 'b': 2},
        1: {'a': 0, 'b': 2},
        2: {'a': 2, 'b': 1}  # Cycles
    }
    dfa.start_state = 0
    print(f"Cyclic DFA -> Depth: {dfa.depth()}")

def bfs_test():
    print("\n--- Testing BFS Functionality ---")

    dfa = DFA()
    dfa.n = 4
    dfa.states = [0, 1, 2, 3]
    dfa.accepting = {0: False, 1: False, 2: False, 3: True}
    dfa.transition = {
        0: {'a': 1, 'b': 0},
        1: {'a': 2, 'b': 0},
        2: {'a': 3, 'b': 0},
        3: {'a': 3, 'b': 3}
    }
    dfa.start_state = 0

    dfa.print_summary()
    computed_depth = dfa.depth()
    print(f"Expected depth: 3")
    print(f"Computed depth: {computed_depth}")
    print(f"Test passed: {computed_depth == 3}")

    # Testing BFS edge cases
    bfs_edge_cases()

def generate_random_strings(count=10, max_length=10):
    import random
    strings = []
    for _ in range(count):
        length = random.randint(1, max_length)
        s = ''.join(random.choice(['a', 'b']) for _ in range(length))
        strings.append(s)
    return strings

def validate_equivalence(dfa, minimized_dfa, num_tests=20, max_len=10):
    print("\n--- Testing if A and M are functionally equivalent ---")
    test_strings = generate_random_strings(num_tests, max_len)
    all_match = True

    for s in test_strings:
        result_a = dfa.accepts(s)
        result_m = minimized_dfa.accepts(s)
        print(f"Input: '{s}' -> A: {result_a}, M: {result_m}")
        if result_a != result_m:
            print("Mismatch found!")
            all_match = False

    if all_match:
        print("L(A) = L(M), all strings were accepted or rejected identically.")
    else:
        print("A functional mismatch was found between A and M.")

def hopcroft_edge_cases():
    print("\n--- Hopcroft Edge Cases ---")

    # All-accepting DFA
    dfa = DFA()
    dfa.n = 3
    dfa.states = [0, 1, 2]
    dfa.accepting = {0: True, 1: True, 2: True}
    dfa.transition = {
        0: {'a': 1, 'b': 2},
        1: {'a': 0, 'b': 2},
        2: {'a': 2, 'b': 1}
    }
    dfa.start_state = 0
    minimized = dfa.minimize()
    print(f"All-accepting DFA -> Original: {dfa.n} states, Minimized: {minimized.n} states")

    # Already minimal DFA
    dfa = DFA()
    dfa.n = 2
    dfa.states = [0, 1]
    dfa.accepting = {0: False, 1: True}
    dfa.transition = {
        0: {'a': 1, 'b': 0},
        1: {'a': 1, 'b': 1}
    }
    dfa.start_state = 0
    minimized = dfa.minimize()
    print(f"Minimal DFA -> Original: {dfa.n} states, Minimized: {minimized.n} states")

        # One-State DFA
    dfa = DFA()
    dfa.n = 1
    dfa.states = [0]
    dfa.accepting = {0: True}  # or False
    dfa.transition = {
        0: {'a': 0, 'b': 0}  # Self-loop
    }
    dfa.start_state = 0
    minimized = dfa.minimize()
    print(f"One-State DFA -> Original: {dfa.n} states, Minimized: {minimized.n} states, Depth: {dfa.depth()}")


def hopcroft_test(dfa):
    print("\n--- Comparing DFA Before and After Minimization ---")

    original_num_states = dfa.n
    original_depth = dfa.depth()

    minimized_dfa = dfa.minimize()
    minimized_num_states = minimized_dfa.n
    minimized_depth = minimized_dfa.depth()

    print(f"Original DFA: {original_num_states} states")
    print(f"Minimized DFA: {minimized_num_states} states")
    print(f"Depth of original DFA (A): {original_depth}")
    print(f"Depth of minimized DFA (M): {minimized_depth}")

    if minimized_num_states < original_num_states:
        print("Minimization successful: DFA was reduced.")
    elif minimized_num_states == original_num_states:
        print("DFA was already minimal or structurally unminifiable")
    else:
        print("Warning: Minimized DFA has more states than original (should not happen!)")

    # Run equivalence test
    validate_equivalence(dfa, minimized_dfa)

    # Run edge case tests
    hopcroft_edge_cases()



# Set test_bfs to True to test the BFS functionality
def main(test_bfs= False , test_hopcroft= False , seed=None):

    # Set debug to True to see the summary of or debug the DFA
    dfa = DFA(debug= False, seed=seed) 

    depth = dfa.depth()

    # Question 2 continuation
    print(f"\n--- Question 2 Output ---")
    print(f"Number of states in A: {dfa.n}")
    print(f"Depth of A: {depth}")

    if test_bfs:
        bfs_test()
    
    # Question 3 continuation
    minimized_dfa = dfa.minimize()

    # Question 4 Output
    print(f"\n--- Question 4 Output ---")
    print(f"Number of states in minimized DFA (M): {minimized_dfa.n}")
    print(f"Depth of minimized DFA (M): {minimized_dfa.depth()}")

    # Validation: Check if minimization preserved language
    print("\n--- Validation ---")
    print(f"Reduction ratio: {minimized_dfa.n / dfa.n:.2f}")
    print(f"States reduced: {dfa.n - minimized_dfa.n}")
    

    if test_hopcroft:
        hopcroft_test(dfa)

if __name__ == "__main__":
    main()
