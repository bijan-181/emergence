# Timing Model

## Overview

The timing model defines the execution timeline of one simulation cycle. It specifies the exact order of operations that occur during each generation, ensuring deterministic, reproducible behavior.

Understanding the timing model is essential for implementing correct simulations and for analyzing emergent behavior.

---

## Generation Cycle

One complete generation consists of the following phases, executed in strict order:

```
┌─────────────────────────────────────────────────┐
│                  GENERATION N                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Current World State                          │
│     └── Immutable snapshot of all cell states    │
│                                                  │
│  2. Agent Observation                            │
│     └── All agents read world state              │
│                                                  │
│  3. Decision Making                              │
│     └── All agents compute actions               │
│                                                  │
│  4. Allowed Intervention                         │
│     └── Agent actions are validated and queued   │
│                                                  │
│  5. Physics Update                               │
│     └── Game of Life rules are applied           │
│                                                  │
│  6. Generation Advance                           │
│     └── World state is committed                 │
│                                                  │
│  7. Rendering                                    │
│     └── World state is visualized                │
│                                                  │
│  8. Repeat                                       │
│     └── Next generation begins                   │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Detailed Phase Descriptions

### Phase 1: Current World State

**Description**: The generation begins with a complete snapshot of the world state.

**Properties**:
- **Immutable**: No cell state can change during this phase
- **Complete**: All cell states, metadata, and history are available
- **Consistent**: The state represents a single, coherent moment in time

**Purpose**: Establish a stable baseline for all subsequent operations. All agents observe the same world state. No agent has privileged access to a different state.

```
World State at Generation N:
┌───┬───┬───┬───┬───┐
│ 0 │ 1 │ 0 │ 0 │ 1 │
├───┼───┼───┼───┼───┤
│ 1 │ 0 │ 1 │ 0 │ 0 │
├───┼───┼───┼───┼───┤
│ 0 │ 1 │ 1 │ 1 │ 0 │
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 1 │ 0 │ 1 │
├───┼───┼───┼───┼───┤
│ 1 │ 0 │ 0 │ 1 │ 0 │
└───┴───┴───┴───┴───┘

All cells are fixed.
All agents see this exact state.
No modifications are possible.
```

### Phase 2: Agent Observation

**Description**: All agents read the current world state and extract relevant information.

**Operations**:
- **Local perception**: Each agent examines cells within its neighborhood
- **Global perception**: Agents may examine the entire world state
- **Target comparison**: Agents compare current state with target pattern
- **History analysis**: Agents may examine recent state transitions
- **Feature extraction**: Agents compute relevant features from raw state

**Constraints**:
- Observation is read-only (no modifications)
- All agents observe the same world state
- Observation does not affect world state
- Observation order does not matter (all see same state)

```
Agent 1 observes:           Agent 2 observes:
┌───┬───┬───┐               ┌───┬───┬───┐
│ 0 │ 1 │ 0 │               │ 1 │ 0 │ 1 │
├───┼───┼───┤               ├───┼───┼───┤
│ 1 │ 0 │ 1 │               │ 0 │ 1 │ 1 │
├───┼───┼───┤               ├───┼───┼───┤
│ 0 │ 1 │ 1 │               │ 1 │ 1 │ 0 │
└───┴───┴───┘               └───┴───┴───┘

Both see the same world.
Different agents may focus on different regions.
```

### Phase 3: Decision Making

**Description**: All agents compute their intended actions based on observations.

**Operations**:
- **Policy evaluation**: Each agent applies its policy to observations
- **Action selection**: Each agent selects an action from its action space
- **Confidence computation**: Each agent computes confidence in its decision
- **Communication**: Agents may communicate with other agents

**Constraints**:
- Decision making is local to each agent
- Agents cannot see other agents' decisions
- Decisions are made independently
- Decisions are based on current world state only

```
Agent 1 decides:            Agent 2 decides:
┌───────────────┐           ┌───────────────┐
│ Action:       │           │ Action:       │
│   Set (2,1)   │           │   Set (3,2)   │
│   to Alive    │           │   to Dead     │
│               │           │               │
│ Confidence:   │           │ Confidence:   │
│   0.85        │           │   0.72        │
└───────────────┘           └───────────────┘

Decisions are independent.
No agent knows another's decision.
```

### Phase 4: Allowed Intervention

**Description**: Agent actions are collected, validated, and queued for application.

**Operations**:
- **Action collection**: Gather all agent actions
- **Validation**: Check actions against intervention constraints
- **Conflict resolution**: Resolve conflicts between agents
- **Prioritization**: Order actions by priority
- **Queuing**: Place valid actions in intervention queue

**Constraints**:
- Invalid actions are rejected (logged but not applied)
- Conflicts are resolved consistently
- Total interventions may be limited per generation
- Interventions are ordered deterministically

```
Collected Actions:
┌─────────────────────────────────────────┐
│ Agent 1: Set (2,1) to Alive    [Valid]  │
│ Agent 2: Set (3,2) to Dead     [Valid]  │
│ Agent 3: Set (2,1) to Dead     [Conflict]│
└─────────────────────────────────────────┘

Conflict Resolution:
  Agent 1 and Agent 3 both target (2,1)
  Resolution strategy: First-come-first-served
  Winner: Agent 1 (submitted first)

Queued Actions:
  1. Set (2,1) to Alive
  2. Set (3,2) to Dead
```

### Phase 5: Physics Update

**Description**: The Game of Life rules are applied to compute the next state of every cell.

**Operations**:
- **Neighbor counting**: For each cell, count alive neighbors
- **Rule application**: Apply birth, survival, underpopulation, overpopulation rules
- **Next state computation**: Compute next state for every cell
- **Physics result**: Complete next world state (without interventions)

**Constraints**:
- Physics rules are applied simultaneously to all cells
- Physics computation is deterministic
- Physics result is independent of agent interventions
- Physics result is computed before interventions are applied

```
Current State:              Physics Result:
┌───┬───┬───┬───┬───┐      ┌───┬───┬───┬───┬───┐
│ 0 │ 1 │ 0 │ 0 │ 1 │      │ 0 │ 0 │ 0 │ 0 │ 0 │
├───┼───┼───┼───┼───┤      ├───┼───┼───┼───┼───┤
│ 1 │ 0 │ 1 │ 0 │ 0 │  ──► │ 0 │ 0 │ 0 │ 0 │ 0 │
├───┼───┼───┼───┼───┤      ├───┼───┼───┼───┼───┤
│ 0 │ 1 │ 1 │ 1 │ 0 │      │ 0 │ 0 │ 1 │ 0 │ 0 │
├───┼───┼───┼───┼───┤      ├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 1 │ 0 │ 1 │      │ 0 │ 0 │ 0 │ 0 │ 0 │
├───┼───┼───┼───┼───┤      ├───┼───┼───┼───┼───┤
│ 1 │ 0 │ 0 │ 1 │ 0 │      │ 0 │ 0 │ 0 │ 0 │ 0 │
└───┴───┴───┴───┴───┘      └───┴───┴───┴───┴───┘

Physics rules applied simultaneously to all cells.
Result is independent of agent actions.
```

### Phase 6: Generation Advance

**Description**: Agent interventions are applied to the physics result, and the world state is committed.

**Operations**:
- **Intervention application**: Apply queued agent actions to physics result
- **State commit**: Commit the final state as the new world state
- **Generation increment**: Increment the generation counter
- **History update**: Update world history with new state
- **Event publication**: Publish generation-end events

**Constraints**:
- Interventions are applied atomically
- The final state is the physics result plus interventions
- The generation counter increments by exactly 1
- The world state is now immutable until the next generation

```
Physics Result:             Queued Interventions:
┌───┬───┬───┬───┬───┐       1. Set (2,1) to Alive
│ 0 │ 0 │ 0 │ 0 │ 0 │       2. Set (3,2) to Dead
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │       Final State:
├───┼───┼───┼───┼───┤       ┌───┬───┬───┬───┬───┐
│ 0 │ 0 │ 1 │ 0 │ 0 │   ──► │ 0 │ 0 │ 0 │ 0 │ 0 │
├───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │       │ 0 │ 1 │ 0 │ 0 │ 0 │
├───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │       │ 0 │ 0 │ 0 │ 0 │ 0 │
└───┴───┴───┴───┴───┘       ├───┼───┼───┼───┼───┤
                            │ 0 │ 0 │ 0 │ 0 │ 0 │
                            ├───┼───┼───┼───┼───┤
                            │ 0 │ 0 │ 0 │ 0 │ 0 │
                            └───┴───┴───┴───┴───┘

Agent interventions applied after physics.
Final state committed as Generation N+1.
```

### Phase 7: Rendering

**Description**: The world state is visualized for human observation.

**Operations**:
- **State reading**: Read the committed world state
- **Color mapping**: Map cell states to colors
- **Display update**: Update the display with new state
- **Overlay rendering**: Render agent positions, targets, etc.

**Constraints**:
- Rendering is passive (does not affect world state)
- Rendering may be delayed or skipped (engine runs without renderer)
- Rendering order does not affect world evolution
- Multiple renderers can operate simultaneously

```
Rendered Output:
┌─────────────────────────────────────────┐
│                                         │
│    ████        ████                     │
│    ████        ████                     │
│                                         │
│              ████                       │
│              ████                       │
│                                         │
│                                         │
│                                         │
└─────────────────────────────────────────┘

Rendering is passive observation.
World state is not affected by rendering.
```

### Phase 8: Repeat

**Description**: The generation cycle completes and the next generation begins.

**Operations**:
- **Cycle completion**: Mark generation N as complete
- **Next generation**: Begin generation N+1
- **State snapshot**: Capture world state for next generation
- **Agent reset**: Agents prepare for next observation cycle

**Constraints**:
- The cycle repeats indefinitely
- The world never resets
- Each generation is independent (except through world state)
- The timing model applies to every generation identically

```
Generation N Complete:
  World state committed
  Generation counter: N → N+1
  Agents ready for next observation
  Cycle restarts

Generation N+1 Begins:
  World state is immutable
  All agents observe same state
  Process repeats
```

---

## Sequence Diagram

The complete generation cycle can be represented as a sequence diagram:

```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│  World  │  │ Agent 1 │  │ Agent 2 │  │ Physics │  │Renderer │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │            │
     │◄───────────┤            │            │            │
     │  Observe   │            │            │            │
     │            │            │            │            │
     │◄───────────┼────────────┤            │            │
     │  Observe   │            │            │            │
     │            │            │            │            │
     │            │──┐         │            │            │
     │            │  │ Decide  │            │            │
     │            │◄─┘         │            │            │
     │            │            │            │            │
     │            │            │──┐         │            │
     │            │            │  │ Decide  │            │
     │            │            │◄─┘         │            │
     │            │            │            │            │
     │◄───────────┼────────────┤            │            │
     │  Intervene │            │            │            │
     │            │            │            │            │
     │            │            │──┐         │            │
     │            │            │  │ Validate│            │
     │            │            │◄─┘         │            │
     │            │            │            │            │
     │            │            │            │──┐         │
     │            │            │            │  │ Compute │
     │            │            │            │◄─┘         │
     │            │            │            │            │
     │            │            │            │            │
     │◄───────────┼────────────┼────────────┤            │
     │  Commit    │            │            │            │
     │            │            │            │            │
     │            │            │            │            │
     │────────────────────────────────────────────────►│
     │            │            │            │   Render   │
     │            │            │            │            │
     │            │            │            │            │
```

---

## Timing Diagram

A linear timing diagram showing the phases within one generation:

```
Time ──────────────────────────────────────────────────────►

┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│  Read   │  Read   │ Decide  │Validate │Compute  │ Write   │
│  (W)    │  (A1)   │ (A1)    │ (A2)    │ (Phy)   │ (All)   │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
│         │         │         │         │         │
▼         ▼         ▼         ▼         ▼         ▼
World    Agent1    Agent1    Agent2    Physics   World
State    Observe   Decide    Validate  Compute   Commit
```

---

## Determinism and Reproducibility

### Why Timing Matters

The timing model is critical for determinism:

1. **Same observations**: All agents see the same world state
2. **Same decisions**: Same observations produce same decisions (given same policy)
3. **Same conflicts**: Same actions produce same conflicts
4. **Same resolution**: Same conflicts produce same resolution
5. **Same result**: Same interventions produce same final state

### Reproducibility Guarantees

Given:
- Same initial world state
- Same agent policies
- Same random seeds
- Same configuration

The system will produce:
- Identical observations
- Identical decisions
- Identical interventions
- Identical world states
- Identical emergent behavior

### Sources of Non-determinism

The only allowed sources of non-determinism are:

1. **Random number generators**: Must be seeded for reproducibility
2. **Floating-point precision**: May vary across hardware (but is deterministic on same hardware)
3. **Timing**: Real-world timing is non-deterministic (but generation count is deterministic)

### Replay Capability

The timing model enables replay:

1. **Log all interventions**: Record every agent action
2. **Log random seeds**: Record all random number generator states
3. **Log configuration**: Record all system parameters
4. **Replay from any point**: Restart from any logged state
5. **Verify reproducibility**: Compare replayed results with original results

---

## Timing Modes

### Real-time Mode

**Description**: Generations advance at a fixed rate matching wall clock time.

**Use case**: Visualization, interactive exploration.

**Properties**:
- Fixed generation interval (e.g., 100ms per generation)
- Consistent visual experience
- May be slower than computation allows

### Accelerated Mode

**Description**: Generations advance as fast as computation allows.

**Use case**: Experiments, batch processing, research.

**Properties**:
- No delay between generations
- Maximum throughput
- No visual feedback during computation

### Burst Mode

**Description**: Process N generations, then pause for analysis.

**Use case**: Analysis, debugging, milestone checking.

**Properties**:
- Process N generations without interruption
- Pause for inspection
- Resume for next burst

### Event-driven Mode

**Description**: Advance only when external input arrives.

**Use case**: Interactive control, step-by-step debugging.

**Properties**:
- Wait for user input
- Advance one generation per input
- Full control over progression

---

## Edge Cases

### Empty World

When the world contains no alive cells:

- **Observation**: All agents see empty world
- **Decisions**: Agents may decide to intervene (birth cells)
- **Physics**: No births occur (no cells with 3 neighbors)
- **Result**: World remains empty (unless agents intervene)

### Full World

When all cells are alive:

- **Observation**: All agents see full world
- **Decisions**: Agents may decide to intervene (kill cells)
- **Physics**: All cells die (overpopulation)
- **Result**: World becomes empty (unless agents intervene)

### Oscillating World

When the world oscillates between states:

- **Observation**: Agents observe oscillating patterns
- **Decisions**: Agents may try to break or stabilize oscillations
- **Physics**: Oscillations continue (if no intervention)
- **Result**: Oscillations persist or are modified by agents

### Chaotic World

When the world exhibits chaotic behavior:

- **Observation**: Agents observe unpredictable patterns
- **Decisions**: Agents may attempt to stabilize chaos
- **Physics**: Chaos continues (if no intervention)
- **Result**: Chaos persists or is reduced by agents

---

## Implementation Considerations

### Read/Write Separation

Implementations must ensure strict read/write separation:

- **Read phase**: No modifications to world state
- **Write phase**: All modifications committed atomically
- **No mixed operations**: Reading and writing cannot interleave

### Parallelism

Parallelism is allowed within phases but not across phases:

- **Parallel observation**: All agents can observe simultaneously
- **Parallel decision-making**: All agents can decide simultaneously
- **Parallel physics computation**: All cells can be computed simultaneously
- **Sequential intervention application**: Conflicts may require sequential resolution

### Memory Management

Implementations must manage memory efficiently:

- **Double buffering**: Maintain two copies of world state (current and next)
- **Batch updates**: Apply all updates in a single pass
- **Lazy evaluation**: Compute only what is needed
- **Caching**: Cache frequently accessed data

---

## Summary

The timing model defines the execution timeline:

| Phase | Description | Key Property |
|-------|-------------|--------------|
| **1. Current State** | Immutable snapshot | Fixed baseline |
| **2. Observation** | Agents read state | Read-only |
| **3. Decision** | Agents compute actions | Independent |
| **4. Intervention** | Actions validated/queued | Ordered |
| **5. Physics** | Rules applied | Simultaneous |
| **6. Advance** | State committed | Atomic |
| **7. Rendering** | State visualized | Passive |
| **8. Repeat** | Cycle restarts | Continuous |

This timing model ensures:

- **Determinism**: Same inputs produce same outputs
- **Reproducibility**: Experiments can be repeated exactly
- **Consistency**: All agents observe the same state
- **Atomicity**: State transitions are complete and instant
- **Persistence**: The world never resets

The timing model is the heartbeat of the Emergence universe—the rhythm through which life emerges, evolves, and persists.

---

*"Time in Emergence is not a river flowing downstream. It is a sequence of moments, each complete, each eternal, each the foundation for what comes next."*