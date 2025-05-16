from dfa import DFA
from test_dfa import DFATest

def main(test_mode, seed):
    dfa = DFA(debug=False, seed=seed)

    if test_mode:
        DFATest.bfs_tests()
        DFATest.hopcroft_tests(dfa)
            

    # Question 2 output
    print(f"\n--- Question 2 Output ---")
    print(f"Number of states in A: {dfa.n}")
    print(f"Depth of A: {dfa.bfs_depth()}")

    original_state_count = dfa.n

    # Prune unreachable and useless states
    dfa.prune()

    # Question 3 and 4
    minimized_dfa = dfa.hopcroft_minimization()

    print(f"\n--- Question 4 Output ---")
    print(f"Number of states in minimized DFA (M): {minimized_dfa.n}")
    print(f"Depth of minimized DFA (M): {minimized_dfa.bfs_depth()}")

    # Validation
    print("\n--- Validation ---")
    print(f"Original DFA states (before pruning): {original_state_count}")
    print(f"States after pruning: {dfa.n}")
    print(f"States after minimization: {minimized_dfa.n}")
    print(f"Reduction from original: {original_state_count - minimized_dfa.n}")
    print(f"Total reduction ratio: {minimized_dfa.n / original_state_count:.2f}")

if __name__ == "__main__":
    main(test_mode=True, seed=None)
