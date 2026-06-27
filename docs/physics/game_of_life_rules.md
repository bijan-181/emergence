# Game of Life Rules

## Overview

The Game of Life is a cellular automaton invented by mathematician John Horton Conway in 1970. Despite its simple rules, it produces extraordinarily complex emergent behavior. This document specifies the exact rules governing cell evolution in the Emergence universe.

---

## Fundamental Principle

The Game of Life is governed by a single principle: **the next state of a cell depends entirely on its current state and the states of its eight neighbors**.

No cell knows about the global state. No cell has memory of past states. No cell communicates with distant cells. Yet from these simple local interactions, complex global patterns emerge.

---

## Neighbor Counting

### Definition

The **neighbor count** is the number of cells in the Moore neighborhood that are currently in the **alive** state.

### Counting Rules

For a cell at position `(x, y)`:

1. Examine all 8 neighbors in the Moore neighborhood
2. Count how many are in the **alive** state
3. Ignore the cell itself
4. Ignore cells outside the world boundary (or apply toroidal wrapping)

### Example: Counting Neighbors

Consider a 5×5 world segment:

```
  0 1 0 0 0
  0 0 1 0 0
  1 1 1 1 0
  0 0 0 0 0
  0 0 0 0 0
```

For the cell at position `(2, 2)` (the center of the pattern):

```
  0 1 0     ← (1,1)=0, (2,1)=1, (3,1)=0
  1 1 1     ← (1,2)=1, (2,2)=1, (3,2)=1
  0 0 0     ← (1,3)=0, (2,3)=0, (3,3)=0
```

Neighbor states (excluding the cell itself):
- `(1,1)`: 0
- `(2,1)`: 1
- `(3,1)`: 0
- `(1,2)`: 1
- `(3,2)`: 1
- `(1,3)`: 0
- `(2,3)`: 0
- `(3,3)`: 0

**Neighbor count = 3**

---

## The Four Rules

The Game of Life is defined by exactly four rules. These rules determine whether a cell is born, survives, or dies in the next generation.

### Rule 1: Birth

**Condition**: A dead cell with exactly **3 alive neighbors** becomes alive.

**Rationale**: Three alive neighbors provide sufficient "stimulation" to birth a new cell. This simulates biological reproduction where multiple parents contribute to creating offspring.

**Example**:

```
Current State:          Next State:
  0 1 0                 0 1 0
  1 0 1      ───►       1 1 1
  0 1 0                 0 1 0

Dead cell (1,1) has 3 neighbors → Becomes alive
```

### Rule 2: Survival

**Condition**: An alive cell with **2 or 3 alive neighbors** survives.

**Rationale**: Two or three neighbors provide adequate support for survival. Too few neighbors means isolation; too many means overcrowding.

**Example**:

```
Current State:          Next State:
  1 1 1                 1 1 1
  1 1 1      ───►       1 0 1
  1 1 1                 1 1 1

Center cell (1,1) has 8 neighbors → Dies (overcrowding)
Corner cell (0,0) has 3 neighbors → Survives
Edge cell (1,0) has 5 neighbors → Dies (overcrowding)
```

### Rule 3: Underpopulation

**Condition**: An alive cell with **fewer than 2 alive neighbors** dies.

**Rationale**: A cell without sufficient neighbors cannot sustain itself. This simulates the biological reality that isolated organisms perish.

**Example**:

```
Current State:          Next State:
  0 0 0                 0 0 0
  0 1 0      ───►       0 0 0
  0 0 0

Alone cell (1,1) has 0 neighbors → Dies (underpopulation)
```

### Rule 4: Overpopulation

**Condition**: An alive cell with **more than 3 alive neighbors** dies.

**Rationale**: Too many neighbors create unsustainable competition for resources. This simulates the biological reality that overcrowded populations collapse.

**Example**:

```
Current State:          Next State:
  1 1 1                 0 0 0
  1 1 1      ───►       0 1 0
  1 1 1                 0 0 0

Center cell (1,1) has 8 neighbors → Dies (overpopulation)
```

---

## Rule Summary Table

| Current State | Neighbor Count | Next State | Rule |
|---------------|----------------|------------|------|
| Dead (0) | 0 | Dead (0) | No birth |
| Dead (0) | 1 | Dead (0) | No birth |
| Dead (0) | 2 | Dead (0) | No birth |
| Dead (0) | 3 | Alive (1) | **Birth** |
| Dead (0) | 4 | Dead (0) | No birth |
| Dead (0) | 5 | Dead (0) | No birth |
| Dead (0) | 6 | Dead (0) | No birth |
| Dead (0) | 7 | Dead (0) | No birth |
| Dead (0) | 8 | Dead (0) | No birth |
| Alive (1) | 0 | Dead (0) | **Underpopulation** |
| Alive (1) | 1 | Dead (0) | **Underpopulation** |
| Alive (1) | 2 | Alive (1) | **Survival** |
| Alive (1) | 3 | Alive (1) | **Survival** |
| Alive (1) | 4 | Dead (0) | **Overpopulation** |
| Alive (1) | 5 | Dead (0) | **Overpopulation** |
| Alive (1) | 6 | Dead (0) | **Overpopulation** |
| Alive (1) | 7 | Dead (0) | **Overpopulation** |
| Alive (1) | 8 | Dead (0) | **Overpopulation** |

---

## Compact Rule Notation

The Game of Life rules are often expressed in **Life-like cellular automaton notation**:

**B3/S23**

Where:
- **B3**: Birth occurs when neighbor count is 3
- **S23**: Survival occurs when neighbor count is 2 or 3

This compact notation fully specifies the transition rules.

---

## Simultaneous State Updates

### Critical Property

All cells in the world update their state **simultaneously**. No cell's update affects any other cell's update in the same generation.

### Why Simultaneous Updates Matter

If cells updated sequentially (e.g., left-to-right, top-to-bottom):

- Earlier updates would affect later updates
- The result would depend on update order
- The system would lose determinism
- The behavior would be fundamentally different from the Game of Life

### Implementation Constraint

Every implementation must ensure that:

1. **Read phase**: All cell states are read before any are written
2. **Compute phase**: Next states are computed for all cells
3. **Write phase**: All cells are updated simultaneously

```
Generation N:
┌─────────────────────────────────────────────┐
│  Read Phase                                  │
│  ┌───┬───┬───┬───┐                         │
│  │ 0 │ 1 │ 1 │ 0 │  ← Read all states     │
│  ├───┼───┼───┼───┤                         │
│  │ 1 │ 0 │ 0 │ 1 │                         │
│  ├───┼───┼───┼───┤                         │
│  │ 0 │ 1 │ 1 │ 0 │                         │
│  └───┴───┴───┴───┘                         │
│                                             │
│  Compute Phase                              │
│  ┌───┬───┬───┬───┐                         │
│  │ ? │ ? │ ? │ ? │  ← Compute next state   │
│  ├───┼───┼───┼───┤     for each cell        │
│  │ ? │ ? │ ? │ ? │                         │
│  ├───┼───┼───┼───┤                         │
│  │ ? │ ? │ ? │ ? │                         │
│  └───┴───┴───┴───┘                         │
│                                             │
│  Write Phase                                │
│  ┌───┬───┬───┬───┐                         │
│  │ 0 │ 0 │ 0 │ 0 │  ← Write all states    │
│  ├───┼───┼───┼───┤     simultaneously      │
│  │ 0 │ 0 │ 0 │ 0 │                         │
│  ├───┼───┼───┼───┤                         │
│  │ 0 │ 0 │ 0 │ 0 │                         │
│  └───┴───┴───┴───┘                         │
└─────────────────────────────────────────────┘
```

---

## Generation Transitions

### Transition Function

The transition from generation N to generation N+1 is a pure function:

```
World(N+1) = Transition(World(N))
```

Where:
- `World(N)` is the complete state at generation N
- `Transition` applies the rules to every cell simultaneously
- `World(N+1)` is the complete state at generation N+1

### Mathematical Formalization

For a cell at position `(x, y)`:

```
NextState(x, y) = f(CurrentState(x, y), NeighborCount(x, y))
```

Where:

```
f(dead, 3) = alive      // Birth
f(alive, 2) = alive     // Survival
f(alive, 3) = alive     // Survival
f(alive, n) = dead      // Underpopulation (n < 2) or Overpopulation (n > 3)
f(dead, n) = dead       // No birth for n ≠ 3
```

### Determinism

Given the same `World(N)`, the function always produces the same `World(N+1)`. This determinism is fundamental to the Game of Life and to Emergence.

---

## Pattern Categories

The Game of Life produces several categories of patterns. These patterns are not explicitly programmed—they emerge naturally from the four simple rules.

### Still Life

**Definition**: A pattern that remains unchanged from one generation to the next.

**Properties**:
- No cells are born or die
- The pattern is stable
- The pattern is self-sustaining

**Examples**:

**Block** (2×2 square):
```
Generation N:      Generation N+1:
  1 1                1 1
  1 1                1 1
```

**Beehive** (6 cells):
```
Generation N:      Generation N+1:
  0 1 0              0 1 0
  1 0 1              1 0 1
  1 0 1              1 0 1
  0 1 0              0 1 0
```

**Loaf** (7 cells):
```
Generation N:      Generation N+1:
  0 1 1              0 1 1
  1 0 1              1 0 1
  1 0 1              1 0 1
  0 1 0              0 1 0
```

**Boat** (5 cells):
```
Generation N:      Generation N+1:
  1 1 0              1 1 0
  1 0 1              1 0 1
  0 1 0              0 1 0
```

### Oscillator

**Definition**: A pattern that returns to its initial state after a fixed number of generations (the **period**).

**Properties**:
- Cycles through a finite set of states
- Period is the number of generations per cycle
- The pattern is self-sustaining
- The pattern does not move

**Examples**:

**Blinker** (period 2):
```
Generation N:      Generation N+1:
  0 1 0              0 0 0
  0 1 0    ───►      1 1 1
  0 1 0              0 0 0
```

**Toad** (period 2):
```
Generation N:      Generation N+1:
  0 0 0 0            0 1 0 0
  0 1 1 1            1 0 1 1
  1 1 1 0    ───►    0 1 1 0
  0 0 0 0            0 0 0 0
```

**Beacon** (period 2):
```
Generation N:      Generation N+1:
  1 1 0 0            1 1 0 0
  1 1 0 0            1 0 0 0
  0 0 1 1    ───►    0 0 0 1
  0 0 1 1            0 0 1 1
```

**Pentadecathlon** (period 15):
A more complex oscillator that cycles through 15 distinct states.

### Spaceship

**Definition**: A pattern that translates across the grid while maintaining its shape (or a periodic variation of it).

**Properties**:
- Moves across the grid
- Returns to its original shape (possibly after multiple generations)
- Has a fixed velocity (cells per generation)
- Does not interact with its past or future positions

**Examples**:

**Glider** (period 4, moves diagonally):
```
Generation 0:    Gen 1:    Gen 2:    Gen 3:    Gen 4:
  0 1 0            0 0 1      0 0 0      0 0 0      0 1 0
  0 0 1            0 1 1      0 0 1      0 1 0      0 0 1
  1 1 1            0 1 0      0 1 1      0 0 1      1 1 1
```

After 4 generations, the glider has moved 1 cell right and 1 cell down.

**Lightweight Spaceship (LWSS)** (period 4, moves horizontally):
```
Generation 0:              Generation 4:
  0 1 0 0 1                  0 1 0 0 1
  1 0 0 0 1                  1 0 0 0 1
  1 0 0 0 1                  1 0 0 0 1
  1 1 1 1 1                  1 1 1 1 1
```

After 4 generations, the LWSS has moved 2 cells right.

**Middleweight Spaceship (MWSS)** and **Heavyweight Spaceship (HWSS)**: Larger variants with similar behavior.

### Gun

**Definition**: A pattern that periodically emits spaceships (or other patterns).

**Properties**:
- Produces a stream of spaceships
- The gun itself remains stationary (or oscillates)
- The emitted spaceships travel away from the gun
- The gun is self-sustaining

**Examples**:

**Gosper Glider Gun** (first known gun):
```
Produces one glider every 30 generations
The gun itself oscillates with period 30
Gligers are emitted in a fixed direction
```

**Simkin Glider Gun**: A more compact gun design.

**Breeders**: Patterns that produce glider guns, creating a cascade of production.

### Puffer

**Definition**: A pattern that moves and leaves debris (still lifes or oscillators) in its wake.

**Properties**:
- Moves across the grid
- Leaves a trail of stable patterns
- The trail grows indefinitely
- The pattern does not repeat exactly (due to accumulated debris)

**Examples**:

**Puffer 1**: The first discovered puffer.
**Puffer 2**: A faster pumper.
**Puffer 3**: A more complex puffer.

### Breeder

**Definition**: A pattern that produces glider guns, which in turn produce gliders. The rate of glider production grows quadratically with time.

**Properties**:
- Produces glider guns
- Glider guns produce gliders
- The growth rate is quadratic (O(n²))
- The pattern is self-sustaining and self-replicating

**Examples**:

**Methuselah**: A pattern that takes many generations to stabilize. The most famous is the **R-pentomino**.

**R-pentomino**:
```
  0 1 1
  1 1 0
  0 1 0
```

This tiny pattern evolves for 1103 generations before stabilizing into a collection of still lifes, oscillators, and gliders.

---

## Why Moving Patterns Emerge

### The Paradox

No cell in the Game of Life moves. Each cell simply evaluates its local neighborhood and updates its state accordingly. Yet gliders, spaceships, and puffers move across the grid.

### The Explanation

Moving patterns emerge because:

1. **Local rules create local structure**: The birth and survival rules create clusters of alive cells
2. **Structure propagates**: The rules cause the cluster to "shift" as cells at the leading edge are born and cells at the trailing edge die
3. **Shape is preserved**: The specific arrangement of cells causes the pattern to maintain its shape while shifting position
4. **Emergence**: The movement is not programmed—it arises from the interaction of simple local rules

### Analogy

Consider a wave in water. No water molecule moves from one end of the ocean to the other. The wave is a pattern of energy that propagates through the medium. Similarly, gliders are patterns of cellular activity that propagate through the grid.

---

## Mathematical Properties

### Computational Universality

The Game of Life is **Turing complete**. This means:

- Any computation that can be performed by a Turing machine can be performed in the Game of Life
- Logical gates (AND, OR, NOT) can be constructed
- Memory can be implemented
- Programs can be encoded as patterns

### Implications

- The Game of Life can simulate any computer
- Complex behavior can arise from simple rules
- The system has infinite computational potential
- Emergence is not just metaphorical—it is mathematically rigorous

### Undecidability

The **halting problem** applies to the Game of Life:

- Given an arbitrary initial pattern, it is impossible to determine in general whether it will eventually stabilize, oscillate, or grow indefinitely
- This means the Game of Life is fundamentally unpredictable in the general case
- Each specific pattern can be analyzed, but no universal algorithm can predict all patterns

---

## Relationship to Emergence

### Why Game of Life

The Game of Life was chosen for Emergence because:

1. **Simplicity**: Only four rules
2. **Complexity**: Produces extraordinary emergent behavior
3. **Well-studied**: Decades of research and known patterns
4. **Turing complete**: Infinite computational potential
5. **Philosophical alignment**: Emergence from simple rules is the project's core principle

### Custom Rule Sets

While the Game of Life is the default, Emergence supports alternative rule sets:

- **Life-like rules**: B/S notation for birth/survival thresholds
- **Generations**: Multiple cell states with aging
- **Higher-order rules**: Larger neighborhoods, more complex transitions
- **Probabilistic rules**: Stochastic state transitions

All rule sets must respect the fundamental physics: deterministic (or reproducible) evolution, simultaneous updates, local computation.

---

## Summary

The Game of Life rules are:

| Rule | Condition | Outcome |
|------|-----------|---------|
| **Birth** | Dead cell + 3 neighbors | Becomes alive |
| **Survival** | Alive cell + 2 or 3 neighbors | Stays alive |
| **Underpopulation** | Alive cell + < 2 neighbors | Dies |
| **Overpopulation** | Alive cell + > 3 neighbors | Dies |

These four rules, applied simultaneously to all cells, produce the rich tapestry of emergent behavior that defines the Game of Life and the Emergence universe.

---

*"The Game of Life proves that complexity does not require complexity. Simple rules, applied locally, can produce behavior that rivals the richness of the natural world."*