
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
        visited = {state: False for state in self.states} 
        distance = {state: -1 for state in self.states} 

        queue = deque([self.start_state]) 
        visited[self.start_state] = True
        distance[self.start_state] = 0

        while queue: 
            current = queue.popleft() 
            for symbol in ['a', 'b']: 
                next_state = self.transition[current][symbol] 
                if not visited[next_state]: 
                    visited[next_state] = True
                    distance[next_state] = distance[current] + 1 
                    queue.append(next_state) 
        


        reachable = [d for d in distance.values() if d != -1] # Getting all reachable distances
        return max(reachable) if reachable else 0 # Returning the maximum distance or 0 if no states are reachable  
    
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
        
        # Initial partition: accepting vs non-accepting states
        accepting = frozenset(state for state in states if self.accepting[state])
        non_accepting = frozenset(states - accepting)
        
        # Initialize partition and waiting set
        P = []
        if accepting:
            P.append(accepting)
        if non_accepting:
            P.append(non_accepting)
        
        # Initialize waiting set with smaller partition for efficiency
        W = deque()
        if accepting and non_accepting:
            if len(accepting) <= len(non_accepting):
                W.append(accepting)
            else:
                W.append(non_accepting)
        elif accepting:
            W.append(accepting)
        elif non_accepting:
            W.append(non_accepting)
        
        # Main refinement loop
        while W:
            A = W.popleft()
            
            for symbol in alphabet:
                # X = set of states that lead to A on symbol
                X = frozenset(state for state in states if self.transition[state][symbol] in A)
                
                # Store partitions that need to be split
                to_split = []
                
                # Find partitions that need splitting
                for i, Y in enumerate(P):
                    intersection = Y & X
                    difference = Y - X
                    
                    if intersection and difference:
                        to_split.append((i, Y, intersection, difference))
                
                # Process splits (backwards to avoid index issues)
                for i, Y, intersection, difference in reversed(to_split):
                    # Remove the original partition
                    P.pop(i)
                    
                    # Add the new partitions
                    P.append(intersection)
                    P.append(difference)
                    
                    # Update waiting set
                    if Y in W:
                        W.remove(Y)
                        W.append(intersection)
                        W.append(difference)
                    else:
                        if len(intersection) <= len(difference):
                            W.append(intersection)
                        else:
                            W.append(difference)
        
        # Map states to their partition indices
        partition_map = {}
        for idx, group in enumerate(P):
            for state in group:
                partition_map[state] = idx
        
        # Create minimized DFA
        new_states = list(range(len(P)))
        new_accepting = {i: any(self.accepting[state] for state in group) for i, group in enumerate(P)}
        
        # Build transition function
        new_transition = {}
        for i, group in enumerate(P):
            # Pick any representative from the group (all behave the same)
            representative = next(iter(group))
            new_transition[i] = {}
            
            for symbol in alphabet:
                target_state = self.transition[representative][symbol]
                new_transition[i][symbol] = partition_map[target_state]
        
        # Create minimized DFA
        minimized_dfa = DFA()
        minimized_dfa.n = len(P)
        minimized_dfa.states = new_states
        minimized_dfa.accepting = new_accepting
        minimized_dfa.transition = new_transition
        minimized_dfa.start_state = partition_map[self.start_state]
        
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
    
    # Question 4
    minimized_dfa = dfa.minimize()
    print(f"\n--- Question 4 Output ---")
    print(f"Number of states in minimized DFA (M): {minimized_dfa.n}")
    print(f"Depth of minimized DFA (M): {minimized_dfa.depth()}")

    if test_hopcroft:
        hopcroft_test(dfa)

if __name__ == "__main__":
    main()
