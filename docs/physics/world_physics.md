# World Physics

## Overview

The Emergence universe is governed by a set of physical laws that define its fundamental properties. These laws are immutable—they cannot be changed, bypassed, or reinterpreted by any mechanism within the system.

This document specifies the physical properties of the world: its structure, state representation, spatial organization, and temporal behavior.

---

## Persistent World

### Definition

The world is a **persistent entity** that exists indefinitely once created. It is never destroyed, reset, or recreated.

### Properties

- **Creation**: The world is created once at the beginning of the simulation
- **Continuity**: The world exists continuously without interruption
- **Non-resetability**: No mechanism exists to return the world to a previous state
- **Accumulation**: Every change is permanent and irreversible
- **Memory**: The world's current state encodes its entire history

### Implications

- There is no "initial state" after creation—the world always has a state
- There is no "game over" or "restart"—the simulation runs indefinitely
- Every intervention is a permanent modification to the world's fabric
- The world carries forward the legacy of every interaction

### Why Persistence Matters

Persistence is the fundamental mechanism through which complexity emerges. Biological systems achieve depth through accumulated history. Emergence mirrors this principle: a persistent world develops structure, memory, and richness that transient systems cannot achieve.

---

## Coordinate System

### Grid Structure

The world is organized as a **two-dimensional rectangular grid** of cells.

### Coordinate Origin

The coordinate system uses the standard Cartesian convention:

```
(0,0) ────────────────────────── (width-1,0)
  │                                    │
  │                                    │
  │           World Grid               │
  │                                    │
  │                                    │
(0,height-1) ──────────────── (width-1,height-1)
```

- **X-axis**: Horizontal, increases to the right
- **Y-axis**: Vertical, increases downward
- **Origin**: Top-left corner at `(0, 0)`

### Coordinate Properties

- **Integer coordinates**: All cell positions are integer pairs `(x, y)`
- **Bounded coordinates**: Valid coordinates are within the world dimensions
- **Unique positions**: Each coordinate pair identifies exactly one cell

---

## Grid Representation

### Structure

The world grid is a **two-dimensional array** of cells organized in rows and columns.

### Dimensions

- **Width**: Number of columns (x-dimension)
- **Height**: Number of rows (y-dimension)
- **Total cells**: `width × height`

### Memory Layout

```
Row 0: [Cell(0,0), Cell(1,0), Cell(2,0), ..., Cell(width-1,0)]
Row 1: [Cell(0,1), Cell(1,1), Cell(2,1), ..., Cell(width-1,1)]
Row 2: [Cell(0,2), Cell(1,2), Cell(2,2), ..., Cell(width-1,2)]
...
Row height-1: [Cell(0,h-1), Cell(1,h-1), ..., Cell(width-1,h-1)]
```

### Properties

- **Homogeneous**: All cells occupy equal area
- **Regular**: Spacing between cells is uniform
- **Planar**: The grid forms a flat surface (no curvature)
- **Static topology**: The grid structure does not change

---

## Cell State Representation

### State Types

Each cell in the world has a **state** that determines its behavior and appearance.

#### Binary State (Standard)

In the standard configuration, each cell has a binary state:

- **Dead** (0): The cell is inactive
- **Alive** (1): The cell is active

#### Multi-state (Extended)

Extended configurations may support multiple states:

- **State 0**: Dead/inactive
- **State 1 through N-1**: Different active states with distinct behaviors

### State Properties

- **Atomic**: A cell's state is a single, indivisible value
- **Discrete**: States are distinct, not continuous
- **Local**: A cell's state is independent of other cells' states
- **Observable**: The state of any cell can be read at any time

### State Transitions

Cell states change only during the **write phase** of a generation. During the read phase, all cell states are immutable.

```
Generation N (Read Phase)
    │
    │  All cell states are fixed
    │  Agents observe current states
    │  Decisions are made
    │
    ▼
Generation N (Write Phase)
    │
    │  All cell states are updated simultaneously
    │  New states are committed
    │
    ▼
Generation N+1 (Read Phase)
    │
    │  New cell states are now fixed
    │  Cycle repeats
```

---

## Moore Neighborhood

### Definition

The **Moore neighborhood** defines which cells influence a given cell's next state. It consists of the eight cells immediately surrounding a cell.

### Structure

For a cell at position `(x, y)`, the Moore neighborhood includes:

```
(x-1, y-1)  (x, y-1)  (x+1, y-1)
(x-1, y  )  (x, y  )  (x+1, y  )
(x-1, y+1)  (x, y+1)  (x+1, y+1)
```

### Visual Representation

```
 ┌───┬───┬───┐
 │ NW│ N │ NE│
 ├───┼───┼───┤
 │ W │Cell│ E │
 ├───┼───┼───┤
 │ SW│ S │ SE│
 └───┴───┴───┘
```

Where:
- **N**: North (above)
- **NE**: Northeast (above-right)
- **E**: East (right)
- **SE**: Southeast (below-right)
- **S**: South (below)
- **SW**: Southwest (below-left)
- **W**: West (left)
- **NW**: Northwest (above-left)

### Neighborhood Size

- **Standard Moore neighborhood**: 8 neighbors
- **Extended neighborhoods**: Can include larger radii (Moore radius > 1)
- **Cell itself**: Not included in its own neighborhood

### Why Moore Neighborhood

The Moore neighborhood is chosen because:

1. **Standard in Game of Life**: Matches the original Conway specification
2. **8-connectivity**: Allows diagonal interactions
3. **Simple implementation**: Easy to compute and vectorize
4. **Rich dynamics**: Produces complex emergent behavior

---

## Finite vs Infinite World

### Finite World (Standard)

In the standard configuration, the world is **finite**:

- **Bounded dimensions**: Width and height are fixed positive integers
- **Fixed cell count**: Total cells = width × height
- **No expansion**: The world cannot grow or shrink

### Infinite World (Theoretical)

An infinite world would extend indefinitely in all directions:

- **Unbounded**: No limits on coordinates
- **Infinite cells**: Unlimited cell count
- **Theoretical only**: Not implemented in standard Emergence

### Why Finite Worlds

Finite worlds are preferred because:

1. **Computational feasibility**: Infinite worlds cannot be stored in memory
2. **Clear boundaries**: Enable well-defined edge behavior
3. **Physical realism**: Even virtual worlds must have finite resources
4. **Reproducibility**: Finite systems can be fully specified and reproduced

---

## World Boundaries

### Boundary Behavior

The world's boundaries define how cells at the edges interact with the world.

#### Toroidal (Wrap-around)

In the standard configuration, the world has **toroidal topology**:

- **Left edge** connects to **right edge**
- **Top edge** connects to **bottom edge**

```
World Grid (Toroidal)

    ┌───────────────────────┐
    │                       │
    │   ┌───┬───┬───┐      │
    │   │   │   │   │      │
    │   ├───┼───┼───┤      │
    │   │   │   │   │      │
    │   └───┴───┘ ←────── Right edge wraps to left
    │       ↑               │
    │       │               │
    │   Bottom edge         │
    │   wraps to top        │
    └───────────────────────┘
```

#### Example: Neighbor Lookup on Torus

For a cell at `(0, 0)` in a 10×10 world:

- **West neighbor**: `(9, 0)` (wraps to right edge)
- **North neighbor**: `(0, 9)` (wraps to bottom edge)
- **Northwest neighbor**: `(9, 9)` (wraps to both edges)

### Why Toroidal Topology

Toroidal boundaries are chosen because:

1. **No edge effects**: All cells have identical neighborhoods
2. **Infinite appearance**: The world appears unbounded
3. **Simple computation**: Easy to implement with modular arithmetic
4. **Game of Life standard**: Matches the canonical implementation

### Alternative Boundaries

While toroidal is standard, other boundaries are possible:

- **Fixed**: Cells outside the boundary are always dead
- **Reflective**: Cells outside mirror the nearest interior cells
- **Open**: No boundary—neighbors outside the world are considered dead

These alternatives can be configured but the default is toroidal.

---

## Time Model

### Discrete Generations

Time in Emergence is **discrete**, divided into distinct units called **generations**.

### Generation Structure

Each generation represents one complete cycle of the world's evolution:

```
Generation 0 ──► Generation 1 ──► Generation 2 ──► ...
```

### Generation Counter

- **Type**: Unsigned 64-bit integer
- **Range**: 0 to 2^64 - 1
- **Monotonic**: The counter never decreases
- **Unique**: Each generation has a distinct number

### Why Discrete Time

Discrete time is chosen because:

1. **Computational efficiency**: Integer arithmetic is fast
2. **Determinism**: Discrete steps produce reproducible results
3. **Event alignment**: All changes happen at generation boundaries
4. **Measurement**: Time can be precisely measured and compared

---

## Deterministic Evolution

### Definition

The world evolves **deterministically** given the same initial state and the same sequence of interventions.

### Properties

- **Same input → same output**: Identical conditions produce identical results
- **Reproducible**: Experiments can be repeated exactly
- **Predictable**: Future states can be computed from current state
- **Traceable**: State transitions can be logged and replayed

### Sources of Non-determinism

The only sources of non-determinism are:

1. **Random number generators**: Used for stochastic processes (mutation, exploration)
2. **Floating-point precision**: May vary across hardware (but is deterministic on same hardware)
3. **Timing**: Real-world timing is non-deterministic, but generation count is not

### Reproducibility

To ensure reproducibility:

- **Random seeds**: All random number generators must be seeded
- **Deterministic algorithms**: All computations must produce identical results on same hardware
- **Event ordering**: Events must be processed in a consistent order

---

## Immutable Physical Laws

### Definition

The laws of physics in the Emergence universe are **immutable**. They cannot be changed by any mechanism within the system.

### What Cannot Change

The following properties are fixed:

- **Grid structure**: Two-dimensional rectangular grid
- **Cell representation**: State, age, lineage, energy
- **Neighborhood**: Moore neighborhood (default)
- **Transition rules**: Game of Life rules (default)
- **Boundary behavior**: Toroidal topology (default)
- **Time model**: Discrete generations
- **Update mechanism**: Simultaneous state updates

### What Can Change

The following properties are configurable:

- **World dimensions**: Width and height
- **Cell states**: Number and meaning of states
- **Neighborhood radius**: Size of Moore neighborhood
- **Rule parameters**: Birth/survival thresholds (for extended rules)
- **Agent configurations**: Number, type, and behavior of agents
- **Evolution parameters**: Population size, mutation rates
- **Timing modes**: Real-time, accelerated, burst

### Why Immutable Laws

Immutable laws are essential because:

1. **Scientific rigor**: Experiments compare results under same laws
2. **Implementation clarity**: Developers know exactly what to implement
3. **Emergence authenticity**: Complex behavior arises from fixed simple rules
4. **Philosophical consistency**: The world has unchangeable physics, like the real universe

---

## Future Extensibility

### Design Principles

The physics module is designed for extensibility:

1. **Layered extensions**: New rules can be added on top of base rules
2. **Pluggable neighborhoods**: Alternative neighborhood definitions can be configured
3. **Multiple state types**: Different cell state representations can be supported
4. **Configurable boundaries**: Alternative boundary conditions can be implemented
5. **Timing modes**: Different execution modes can be added

### Extension Constraints

All extensions must respect:

1. **Persistence**: The world must never be reset
2. **Determinism**: Results must be reproducible given same inputs
3. **Simultaneity**: State updates must be atomic
4. **Local computation**: Cell updates depend only on local information

### Future Directions

Potential extensions include:

- **Higher dimensions**: 3D or 4D worlds
- **Hexagonal grids**: Alternative grid topologies
- **Continuous states**: Real-valued cell states
- **Continuous time**: Non-discrete evolution
- **Stochastic rules**: Probabilistic state transitions
- **Chemical models**: Diffusion and reaction systems

---

## Summary

The physical properties of the Emergence universe are:

| Property | Value |
|----------|-------|
| **Dimensionality** | 2D |
| **Grid type** | Rectangular |
| **Cell state** | Binary (default) |
| **Neighborhood** | Moore (8-connected) |
| **World boundary** | Toroidal (wrap-around) |
| **Time model** | Discrete generations |
| **Evolution** | Deterministic |
| **Persistence** | Infinite (never reset) |
| **Physics** | Immutable |

These properties define the immutable substrate upon which all emergent behavior arises. They are the foundation of the Emergence universe—the constraints within which complexity emerges.

---

*"Physics defines the possible. Emergence discovers the actual."*