# Concept Definitions

## Overview

This document defines the core concepts used by Emergence. These definitions are the official vocabulary of the project. All documentation, code, and communication should use these terms consistently.

---

## World

**Definition**: The fundamental entity in Emergence. A World is a two-dimensional grid of cells that persists indefinitely and evolves continuously.

**Details**: The World is created once and never reset. It carries the accumulated history of all modifications, interventions, and evolutionary changes. The World is not a container for simulations—it is a living entity that embodies the simulation.

**Properties**:
- Persistent: Never destroyed or reset
- Spatial: Two-dimensional grid structure
- Dynamic: Continuously evolving
- Historical: Carries full history in its state
- Observable: Can be queried and inspected

**Related Concepts**: Cell, Generation, State, Persistent World

---

## Persistent World

**Definition**: A World that maintains its state indefinitely, accumulating all changes over time.

**Details**: Persistence is the defining characteristic of Emergence's World. Unlike ephemeral simulations that can be reset, a Persistent World carries the full weight of its history. Every cell's current state reflects its entire lineage—every modification, every interaction, every evolutionary change.

**Why It Matters**: Persistence enables genuine evolutionary dynamics. It creates the historical depth necessary for complex emergent behavior. It mirrors biological reality, where organisms carry the legacy of their evolutionary history.

**Contrast With**: Ephemeral worlds that can be reset, simulations that start fresh for each experiment.

**Related Concepts**: World, Generation, History

---

## Generation

**Definition**: A single step in the World's evolution. One generation represents one complete cycle of observation, decision, and update.

**Details**: Each generation follows a strict two-phase protocol:
1. **Read Phase**: All components observe the current World state
2. **Write Phase**: All changes are applied atomically

The generation counter increments after each complete cycle. The World at generation N+1 is derived from the World at generation N through the application of rules, agent actions, and evolutionary changes.

**Properties**:
- Atomic: Changes are applied all at once
- Ordered: Generations are strictly sequential
- Counted: Each generation has a unique number
- Observable: The World state at any generation can be inspected

**Related Concepts**: World, Simulation, State

---

## Simulation

**Definition**: The continuous process of generating successive World states through the application of rules, agent actions, and evolutionary changes.

**Details**: The Simulation is the active process that drives the World's evolution. It is not the World itself, but the mechanism through which the World changes. The Simulation runs continuously, generating new generations without pause.

**Properties**:
- Continuous: Never stops once started
- Deterministic: Same inputs produce same outputs (given same random seed)
- Observable: Events are published for all significant changes
- Controllable: Can be paused, resumed, or queried

**Related Concepts**: World, Generation, Core Engine

---

## Target

**Definition**: A desired pattern that the World should embody. The Target provides direction for the World's evolution.

**Details**: Targets are specified by users and processed by the Pattern Generator into binary matrices. The World gradually reorganizes itself to match the Target, carrying forward its history through the transition.

**Types**:
- Text: String rendered to bitmap
- Image: Raster image binarized
- SVG: Vector path rasterized
- ASCII: Character-based pattern
- Binary: Direct matrix specification
- Procedural: Algorithmically generated

**Properties**:
- Generic: Represented as binary matrix
- Optional: The World can exist without a Target
- Temporary: Changes when a new Target is provided
- Aspirational: The World may not fully achieve it

**Related Concepts**: Target Pattern, Binary Pattern, Pattern Generator

---

## Target Pattern

**Definition**: The binary matrix representation of a Target after processing by the Pattern Generator.

**Details**: The Target Pattern is the universal intermediate representation that all Targets are converted to. It is a two-dimensional array of binary values (0 or 1) that specifies which cells should be active.

**Properties**:
- Binary: Only two states (on/off)
- Normalized: Same dimensions as World or scaled to fit
- Validated: Checked for consistency and feasibility
- Comparable: Can be compared with World state for similarity

**Related Concepts**: Target, Binary Pattern, Pattern Generator

---

## Binary Pattern

**Definition**: A two-dimensional array of binary values representing a spatial pattern.

**Details**: Binary Patterns are the fundamental representation of spatial information in Emergence. Both Target Patterns and World states can be represented as Binary Patterns (when considering only the on/off aspect of cell states).

**Properties**:
- Binary: Only two values (0 and 1)
- Spatial: Two-dimensional structure
- Comparable: Can be compared using various metrics
- Transformable: Can be scaled, rotated, filtered

**Related Concepts**: Target Pattern, World, State

---

## Agent

**Definition**: An entity that observes the World and takes actions to guide it toward Target Patterns.

**Details**: Agents are the mechanism through which external intelligence interacts with the living World. They perceive the World state, make decisions based on their policy, and apply actions to modify cells.

**Architecture**:
- Perception: Observes World state
- Decision: Selects action based on policy
- Action: Modifies World cells
- Learning: Improves policy through experience

**Types**:
- Reactive: Responds to immediate conditions
- Deliberative: Plans sequences of actions
- Learning: Improves through experience
- Social: Coordinates with other agents
- Meta: Controls other agents

**Related Concepts**: Action, Policy, Reward, Learning Cycle

---

## Evolution

**Definition**: The process of improving strategies, rules, or agents through variation, selection, and reproduction.

**Details**: Evolution applies biological principles to optimize components of the Emergence system. It maintains populations of candidate solutions, evaluates their fitness, selects winners, and creates offspring through variation operators.

**Components**:
- Population: Collection of candidate solutions
- Fitness: Measure of solution quality
- Selection: Choosing which solutions reproduce
- Variation: Creating modified copies of solutions
- Replacement: Updating the population

**What Is Evolved**:
- Rule set parameters
- Agent strategies
- Reward function components
- Neighborhood definitions
- Resource distribution patterns

**Related Concepts**: Population, Fitness, Mutation, Genome

---

## Intervention

**Definition**: A modification applied to the World by an Agent or external process.

**Details**: Interventions are the mechanism through which the World is guided toward Target Patterns. Unlike natural evolution, which is undirected, interventions are purposeful modifications that move the World toward a goal.

**Types**:
- Cell modification: Setting a specific cell's state
- Region modification: Setting a rectangular region
- Signal: Broadcasting information to other agents
- Wait: Observing without acting

**Properties**:
- Atomic: Applied without interference
- Logged: Recorded for analysis
- Reversible: Can be undone (in principle, through counter-interventions)
- Purposeful: Directed toward a goal

**Related Concepts**: Agent, Action, World

---

## Genome

**Definition**: The encoded representation of a strategy, rule set, or agent configuration that can be evolved.

**Details**: Genomes are the data structures that evolution operates on. They encode the parameters and structure of a solution in a format that supports variation operators (mutation, crossover).

**Properties**:
- Encodable: Can be represented as a data structure
- Variations: Supports mutation and crossover
- Evaluable: Can be tested for fitness
- Interpretable: Can be decoded into a working solution

**Related Concepts**: Evolution, Population, Mutation, Fitness

---

## Fitness

**Definition**: A measure of how well a candidate solution performs its task.

**Details**: Fitness is the metric that evolution uses to select which solutions reproduce. In Emergence, fitness typically measures how well a strategy, rule set, or agent configuration guides the World toward Target Patterns.

**Components**:
- Target similarity: Match to Target Pattern
- Transition speed: Generations to reach Target
- Stability: Persistence of achieved patterns
- Resource efficiency: Energy consumption
- Adaptability: Performance across multiple Targets

**Properties**:
- Quantitative: Expressed as a number
- Comparative: Used to rank solutions
- Multi-dimensional: May combine multiple factors
- Time-varying: May change as the World evolves

**Related Concepts**: Evolution, Population, Genome

---

## Emergence

**Definition**: The arising of complex, organized behavior from the interaction of simple components following local rules.

**Details**: Emergence is both the name of the project and the phenomenon it studies. In Emergence, complex global behavior should arise from the interaction of simple cells following local rules, guided by agents toward meaningful patterns.

**Properties**:
- Bottom-up: Arises from local interactions
- Unexpected: Not explicitly programmed
- Organized: Shows structure and pattern
- Robust: Persists despite perturbations

**Related Concepts**: World, Rules, Agents, Complex Adaptive Systems

---

## Experiment

**Definition**: A controlled run of the Emergence system with defined parameters, objectives, and measurement.

**Details**: Experiments are the scientific units of Emergence. Each experiment has defined parameters (World size, rules, agents, Targets), runs for a specified duration, and produces measurable results.

**Components**:
- Parameters: Configuration settings
- Lifecycle: Setup, run, monitor, complete
- Metrics: Performance measurements
- Results: Outcomes and analysis

**Properties**:
- Reproducible: Can be repeated with same results
- Documented: Parameters and outcomes recorded
- Analyzable: Results can be studied
- Comparable: Can be compared with other experiments

**Related Concepts**: Experiment Manager, Results, Metrics

---

## Controller

**Definition**: The component that manages the simulation loop and coordinates all subsystems.

**Details**: The Controller (also called Core Engine) is the central coordinator. It does not perform computation itself—it delegates to specialized subsystems and ensures lifecycle correctness.

**Responsibilities**:
- Initialize subsystems
- Run simulation loop
- Dispatch events
- Ensure state consistency
- Provide public API

**Properties**:
- Central: Coordinates all components
- Event-driven: Communicates through events
- Lifecycle-managed: Handles startup, running, shutdown
- Stateless: Does not store simulation state

**Related Concepts**: Core Engine, Simulation, Event System

---

## Renderer

**Definition**: A component that visualizes World state for human observation.

**Details**: The Renderer is completely decoupled from the simulation. It connects to the engine through the event system and visualizes the World state. Multiple renderers can be supported (windowed, terminal, web, headless).

**Types**:
- Windowed: Graphical display
- Terminal: Text-based display
- Web: Browser-based display
- Headless: File output

**Properties**:
- Optional: Simulation runs without renderer
- Decoupled: No direct dependency on engine
- Pluggable: Can be replaced without affecting engine
- Interactive: Supports user input

**Related Concepts**: Core Engine, Event System, Visualization

---

## Pattern Generator

**Definition**: The component that converts Target specifications into binary matrices.

**Details**: The Pattern Generator handles all input formats and processing steps needed to convert user-provided Targets into the binary matrix format that the rest of the system uses.

**Pipeline**:
1. Format detection
2. Parsing
3. Normalization
4. Scaling
5. Binarization
6. Validation

**Properties**:
- Generic: Handles multiple input formats
- Pluggable: New formats can be added
- Validated: Ensures output is valid
- Cached: Processes each Target once

**Related Concepts**: Target, Target Pattern, Binary Pattern

---

## Rule Engine

**Definition**: The component that defines and applies cell behavior rules.

**Details**: The Rule Engine determines how cells evolve. It contains multiple Rule Sets, each defining behavior for different aspects of cell life (growth, diffusion, interaction, etc.).

**Components**:
- Rule Set: Collection of related rules
- Neighborhood: Which cells are considered
- Compute: Next-state function
- Priority: Rule ordering

**Properties**:
- Pluggable: Rule Sets can be added/removed
- Composable: Multiple Rule Sets can be active
- Configurable: Parameters can be adjusted
- Evolvable: Rule Sets can be evolved

**Related Concepts**: Rules, World, Generation

---

## State

**Definition**: The complete configuration of the World at a specific moment in time.

**Details**: State includes every cell's current values, the generation counter, and all metadata. The World's State is the accumulated result of its entire history.

**Components**:
- Cell states: Values for every cell
- Generation: Current generation number
- Metadata: Timestamps, parameters, statistics
- History: Recent state changes

**Properties**:
- Complete: Includes all information
- Snapshotable: Can be saved and restored
- Comparable: Can be compared with other states
- Serializable: Can be stored and transmitted

**Related Concepts**: World, Generation, Snapshot

---

## Action

**Definition**: A decision made by an Agent that modifies the World.

**Details**: Actions are the outputs of Agent decision-making. They specify what modifications to apply to the World. Actions are applied during the Write Phase of each generation.

**Types**:
- Modify cell: Set specific cell state
- Modify region: Set rectangular area
- Signal: Broadcast information
- Wait: Observe without acting

**Properties**:
- Discrete: Chosen from a defined action space
- Applied: Executed during Write Phase
- Logged: Recorded for analysis
- Rewardable: Associated with reward signal

**Related Concepts**: Agent, Policy, Reward

---

## Reward

**Definition**: A numerical signal indicating how good an Agent's Action was.

**Details**: Rewards are computed after Actions are applied and the World has transitioned. They guide Agent learning by indicating which Actions lead to desirable outcomes.

**Components**:
- Pattern match: Improvement toward Target
- Progress: Change from previous state
- Efficiency: Resource cost of Action
- Stability: Persistence of achieved state
- Diversity: Contribution to complexity

**Properties**:
- Numerical: Single scalar value
- Delayed: May be computed after multiple Actions
- Composite: May combine multiple factors
- Shaped: Can be designed to guide learning

**Related Concepts**: Agent, Action, Learning Cycle, Reinforcement Learning

---

## Episode

**Definition**: A complete sequence of interactions between an Agent and the World, from initial state to terminal state.

**Details**: In Emergence, Episodes may be less clearly defined than in traditional RL because the World never resets. An Episode can be defined as:
- A fixed number of generations
- The time between Target changes
- A defined experimental period
- Or the entire lifetime of the World

**Properties**:
- Bounded: Has a clear start and end
- Measurable: Can be evaluated for total reward
- Comparable: Can be compared with other Episodes
- Learning unit: Used for policy updates

**Related Concepts**: Agent, Reward, Learning Cycle

---

## Mutation

**Definition**: A random modification applied to a Genome during evolution.

**Details**: Mutations introduce variation into the population, enabling exploration of the solution space. They are applied with configurable probability and magnitude.

**Types**:
- Point mutation: Change a single gene
- Insertion: Add new genetic material
- Deletion: Remove genetic material
- Duplication: Copy existing material
- Inversion: Reverse a sequence

**Properties**:
- Random: Introduces stochastic variation
- Bounded: Limited by mutation rate and magnitude
- Evaluated: fitness is measured after mutation
- Reversible: Can be undone by counter-mutation

**Related Concepts**: Evolution, Genome, Population, Variation

---

## Population

**Definition**: A collection of candidate solutions that evolve together.

**Details**: The Population is the unit of evolution. It contains multiple Genomes, each representing a candidate solution. The Population evolves through selection, variation, and replacement.

**Properties**:
- Diverse: Contains multiple different solutions
- Sized: Has a fixed or dynamic size
- Evaluated: All members have measured fitness
- Evolving: Changes over evolutionary time

**Related Concepts**: Evolution, Genome, Fitness, Selection

---

## Learning Cycle

**Definition**: The complete process of observing, acting, receiving reward, and updating policy.

**Details**: The Learning Cycle is the fundamental unit of agent learning. It encompasses:
1. Observe World state
2. Select Action based on policy
3. Apply Action to World
4. Compute Reward
5. Update policy based on experience

**Properties**:
- Repeated: Many cycles per Episode
- Measurable: Can track learning progress
- Incremental: Policy improves gradually
- Experience-generating: Produces data for learning

**Related Concepts**: Agent, Action, Reward, Policy, Reinforcement Learning

---

## Summary

These concepts form the vocabulary of Emergence. They should be used consistently in all documentation, code, and communication. When new concepts are introduced, they should be defined here first.

The concepts are interconnected:

```
World ← Generation ← Simulation
  ↑
  ├── State
  │     ├── Cell states
  │     ├── Metadata
  │     └── History
  │
  ├── Agent → Action → Reward → Learning Cycle
  │     │
  │     └── Policy
  │
  └── Target → Target Pattern → Binary Pattern
        │
        └── Pattern Generator

Evolution → Population → Genome → Fitness → Mutation

Experiment → Experiment Manager → Results → Metrics

Core Engine → Simulation Loop → Event System → Renderer
```

This vocabulary enables precise communication about Emergence's concepts and mechanisms.
