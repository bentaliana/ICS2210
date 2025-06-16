# DFA Construction, Minimization, and Analysis

**Course**: Data Structures and Algorithms 2 - ICS2210  
**Institution**: University of Malta  
**Year**: 2025

## Project Overview

This project implements a comprehensive suite of algorithms for Deterministic Finite Automata (DFA) operations, including:
- Random DFA construction
- Depth computation using BFS
- DFA minimization using Hopcroft's algorithm
- Strongly Connected Components (SCC) detection using Tarjan's algorithm

## Features

### 1. Random DFA Generation
- Creates DFAs with 16-64 states
- Random accepting/rejecting state assignment
- Random transition generation for alphabet {a, b}
- Configurable seed for reproducibility

### 2. DFA Depth Computation
- BFS-based shortest path calculation
- Efficient O(V + E) implementation
- Handles unreachable states

### 3. DFA Minimization
- **Hopcroft's Algorithm** implementation with O(n log n) complexity
- Pre-computed reverse transitions for optimization
- Automatic pruning of unreachable and useless states
- Language preservation guarantee (L(A) = L(M))

### 4. SCC Detection
- **Tarjan's Algorithm** with O(V + E) complexity
- Complete SCC identification and analysis
- Visualization support for SCC highlighting

## Project Structure

```
DFA.ipynb          # Main Jupyter notebook with all implementations
├── Question 1     # DFA construction
├── Question 2     # Depth computation (BFS)
├── Question 3     # Minimization (Hopcroft's)
├── Question 4     # Minimized DFA depth
├── Question 5     # SCC detection (Tarjan's)
└── Testing        # Empirical validation
```

## Technical Details

### Data Structure Choice
- **Adjacency List** representation using nested Python dictionaries
- O(1) transition lookups
- O(n|Σ|) space complexity (optimal for sparse DFAs)

### Algorithm Implementations

#### Hopcroft's Algorithm
- Worklist-based partition refinement
- Pre-computed reverse transitions
- Efficient splitting mechanism

#### Tarjan's Algorithm
- Linear-time SCC detection
- Stack-based DFS approach
- Complete node coverage guarantee

## Example Output

For seed = 2025:
```
DFA A: 51 states, depth = 11
DFA M: 38 states, depth = 11 (after minimization)
SCCs in A: 1 (size 39)
SCCs in M: 1 (size 38)
```

## Testing & Validation

### Minimization Testing
- Language equivalence verification (L(A) = L(M))
- Edge cases: all-accepting DFAs, single-state DFAs
- Comparison with credible sources (RELIC, GeeksforGeeks)
- Visual verification using Graphviz

### SCC Testing
- Property validation (all nodes in SCCs, strong connectivity)
- Multiple test cases from academic sources
- Visual highlighting of SCC groups

## Requirements

- Python 3.x
- Jupyter Notebook
- Dependencies:
  - `random` (standard library)
  - `collections.deque` (standard library)
  - `graphviz` (for visualization)

## Performance

- **DFA Construction**: O(n) where n ∈ [16, 64]
- **BFS Depth**: O(V + E)
- **Hopcroft's Minimization**: O(n log n)
- **Tarjan's SCC**: O(V + E)

## References

Key algorithms implemented from:
- Hopcroft, Motwani & Ullman - *Introduction to Automata Theory*
- Tarjan, R. E. - *Depth-First Search and Linear Graph Algorithms*
- University of Malta RELIC Portal

## Key Design Decisions

1. **Hopcroft's over Moore's Algorithm**: Better asymptotic complexity (O(n log n) vs O(n²))
2. **Adjacency List over Matrix**: Optimal for sparse DFA structure
3. **Monkey Patching**: Clean modular code organization in Jupyter
4. **Comprehensive Testing**: Both programmatic and visual validation

## Notes

- All implementations include extensive inline documentation
- Visualizations support both standard DFA and SCC-highlighted views
- Seed parameter ensures reproducible results for testing

---

**Author**: Ben Taliana  
**Course Code**: ICS2210 : Data Structures and Algorithms 2
**Submission Date**: 21/05/2025
