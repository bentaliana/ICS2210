from dfa import DFA
import random

class DFATest:

    @staticmethod
    def generate_random_strings(count=10, max_length=10):
        strings = []
        for _ in range(count):
            length = random.randint(1, max_length)
            s = ''.join(random.choice(['a', 'b']) for _ in range(length))
            strings.append(s)
        return strings

    @staticmethod
    def validate_equivalence(dfa, minimized_dfa, num_tests=20, max_len=10):
        print("\n--- Testing if A and M are functionally equivalent ---")
        test_strings = DFATest.generate_random_strings(num_tests, max_len)
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

    @staticmethod
    def bfs_tests():
        print("\n--- Testing BFS Functionality ---")

        # Known depth test
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
        computed_depth = dfa.bfs_depth()
        print(f"Expected depth: 3")
        print(f"Computed depth: {computed_depth}")
        print(f"Test passed: {computed_depth == 3}")

        DFATest.bfs_edge_cases()

    @staticmethod
    def bfs_edge_cases():
        print("\n--- Testing BFS Edge Cases ---")

        # Unreachable state
        dfa = DFA()
        dfa.n = 3
        dfa.states = [0, 1, 2]
        dfa.accepting = {0: False, 1: True, 2: True}
        dfa.transition = {
            0: {'a': 1, 'b': 1},
            1: {'a': 0, 'b': 0},
            2: {'a': 2, 'b': 2}
        }
        dfa.start_state = 0
        print(f"DFA with Unreachable State -> Depth: {dfa.bfs_depth()}")

        # Cyclic DFA
        dfa = DFA()
        dfa.n = 3
        dfa.states = [0, 1, 2]
        dfa.accepting = {0: False, 1: False, 2: True}
        dfa.transition = {
            0: {'a': 1, 'b': 2},
            1: {'a': 0, 'b': 2},
            2: {'a': 2, 'b': 1}
        }
        dfa.start_state = 0
        print(f"Cyclic DFA -> Depth: {dfa.bfs_depth()}")

    @staticmethod
    def hopcroft_tests(dfa):
        print("\n--- Comparing DFA Before and After Minimization ---")

        original_num_states = dfa.n
        original_depth = dfa.bfs_depth()

        minimized_dfa = dfa.hopcroft_minimization()
        minimized_num_states = minimized_dfa.n
        minimized_depth = minimized_dfa.bfs_depth()

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

        DFATest.validate_equivalence(dfa, minimized_dfa)
        DFATest.hopcroft_edge_cases()

    @staticmethod
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
        minimized = dfa.hopcroft_minimization()
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
        minimized = dfa.hopcroft_minimization()
        print(f"Minimal DFA -> Original: {dfa.n} states, Minimized: {minimized.n} states")

        # One-State DFA
        dfa = DFA()
        dfa.n = 1
        dfa.states = [0]
        dfa.accepting = {0: True}
        dfa.transition = {
            0: {'a': 0, 'b': 0}
        }
        dfa.start_state = 0
        minimized = dfa.hopcroft_minimization()
        print(f"One-State DFA -> Original: {dfa.n} states, Minimized: {minimized.n} states, Depth: {dfa.bfs_depth()}")
