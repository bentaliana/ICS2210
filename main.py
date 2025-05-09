from dfa import DFA
from test_dfa import DFATest

def main(test_mode=None, seed=None):
    dfa = DFA(debug=False, seed=seed)

    if test_mode:
        if 'bfs' in test_mode:
            DFATest.bfs_tests()
        if 'hopcroft' in test_mode:
            DFATest.hopcroft_tests(dfa)

    # Question 2 output
    print(f"\n--- Question 2 Output ---")
    print(f"Number of states in A: {dfa.n}")
    print(f"Depth of A: {dfa.bfs_depth()}")

    # Question 3 continuation
    minimized_dfa = dfa.hopcroft_minimization()

    # Question 4 output
    print(f"\n--- Question 4 Output ---")
    print(f"Number of states in minimized DFA (M): {minimized_dfa.n}")
    print(f"Depth of minimized DFA (M): {minimized_dfa.bfs_depth()}")

    # Validation
    print("\n--- Validation ---")
    print(f"Reduction ratio: {minimized_dfa.n / dfa.n:.2f}")
    print(f"States reduced: {dfa.n - minimized_dfa.n}")

    

if __name__ == "__main__":
    # Run with desired test mode 
    main(test_mode=['bfs', 'hopcroft'], seed=None)
