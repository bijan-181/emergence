# Terminology Guide

## Overview

This document establishes the official terminology for the Emergence project. Consistent terminology is essential for clear communication across documentation, code, and research papers.

Every term in this guide includes:
- **Preferred term**: The term to use
- **Avoided alternatives**: Terms to avoid and why
- **Definition**: Precise meaning in Emergence context
- **Reasoning**: Why this term was chosen
- **Examples**: Usage in context

---

## World Terms

### World

**Preferred term**: World

**Avoided alternatives**:
- Board: Suggests a game; Emergence is not a game
- Grid: Too generic; refers to the data structure, not the entity
- Canvas: Suggests visual art; Emergence is a research platform
- Simulation: The World is an entity, not a process
- Environment: Too generic; used in RL but not specific enough

**Definition**: The fundamental entity in Emergence—a persistent, two-dimensional grid of cells that evolves continuously.

**Reasoning**: "World" conveys the scale and permanence of the entity. It's a place where things happen, not just a structure or process.

**Examples**:
- "The World evolves continuously."
- "Agents observe the World state."
- "The World never resets."

---

### Persistent World

**Preferred term**: Persistent World

**Avoided alternatives**:
- Permanent World: "Permanent" suggests unchanging; the World changes continuously
- Living World: Too metaphorical for technical documentation
- Eternal World: Suggests timelessness; the World has a beginning
- Indestructible World: Focuses on destruction; persistence is about continuity

**Definition**: A World that maintains its state indefinitely, accumulating all changes over time.

**Reasoning**: "Persistent" precisely describes the key property—continuity over time. It's a technical term used in computing for state that survives across sessions.

**Examples**:
- "Emergence uses a Persistent World model."
- "The Persistent World carries its full history."

---

### Generation

**Preferred term**: Generation

**Avoided alternatives**:
- Step: Too generic; suggests a single operation
- Tick: Suggests a clock; generations are more complex
- Cycle: Suggests repetition; generations are evolutionary
- Frame: Suggests visualization; generations are conceptual
- Iteration: Suggests loops; generations are evolutionary steps

**Definition**: A single step in the World's evolution, consisting of a read phase and a write phase.

**Reasoning**: "Generation" captures the evolutionary nature of each step. It connects to biological evolution, where each generation is a complete cycle of reproduction and variation.

**Examples**:
- "The World advances one generation."
- "After 1000 generations, the pattern emerged."
- "Each generation follows a two-phase protocol."

---

### State

**Preferred term**: State

**Avoided alternatives**:
- Configuration: Too generic; suggests settings
- Snapshot: Implies a single captured moment; State is the complete configuration
- Layout: Suggests visual arrangement; State includes all properties
- Pattern: Specific to spatial arrangement; State includes metadata

**Definition**: The complete configuration of the World at a specific moment in time, including all cell values, metadata, and historical information.

**Reasoning**: "State" is the standard term in computer science for the complete condition of a system at a point in time. It's precise and well-understood.

**Examples**:
- "The World state includes all cell values."
- "State transitions are atomic."
- "Save the current state to disk."

---

### Cell

**Preferred term**: Cell

**Avoided alternatives**:
- Pixel: Suggests display; Cells are computational entities
- Node: Too generic; suggests graph structures
- Tile: Suggests visual arrangement; Cells are active entities
- Agent: Confusing with the Agent system
- Unit: Too generic; suggests measurement

**Definition**: A single unit in the World grid, containing state, age, lineage, and energy information.

**Reasoning**: "Cell" connects to biological cells, which are the fundamental units of life. It also connects to cellular automata, the computational substrate of Emergence.

**Examples**:
- "Each cell has a state value."
- "Cells evolve according to rules."
- "Agent actions modify specific cells."

---

## Pattern Terms

### Target

**Preferred term**: Target

**Avoided alternatives**:
- Goal: Suggests a single objective; Targets can be multiple
- Objective: Too formal; suggests optimization
- Pattern: Too generic; Target specifies a desired pattern
- Image: Suggests visual only; Targets can be text, symbols, etc.
- Template: Suggests a model to copy; Targets are aspirations

**Definition**: A desired pattern that the World should embody, specified by the user.

**Reasoning**: "Target" conveys direction and aspiration without implying exact achievement. The World may not fully achieve the Target, but it moves toward it.

**Examples**:
- "The user provides a new Target."
- "The World evolves toward the Target."
- "Multiple Targets can be queued."

---

### Target Pattern

**Preferred term**: Target Pattern

**Avoided alternatives**:
- Desired pattern: Too verbose
- Goal pattern: Suggests a game
- Output pattern: Suggests generation, not embodiment
- Reference pattern: Too formal
- Expected pattern: Suggests prediction

**Definition**: The binary matrix representation of a Target after processing by the Pattern Generator.

**Reasoning**: "Target Pattern" clearly indicates that this is the processed form of a Target, ready for comparison with the World state.

**Examples**:
- "The Target Pattern is a binary matrix."
- "Compare World state with Target Pattern."
- "Target Patterns are normalized to World dimensions."

---

### Binary Pattern

**Preferred term**: Binary Pattern

**Avoided alternatives**:
- Binary matrix: Describes the data structure, not the concept
- Bitmap: Suggests image processing
- Boolean array: Too technical
- On/off pattern: Too verbose
- Two-state pattern: Too verbose

**Definition**: A two-dimensional array of binary values representing a spatial pattern.

**Reasoning**: "Binary Pattern" emphasizes the conceptual nature (a pattern) while specifying the representation (binary). It's both precise and descriptive.

**Examples**:
- "Binary Patterns are the universal representation."
- "Both Target and World states can be expressed as Binary Patterns."
- "Binary Patterns support various similarity metrics."

---

### Pattern Generator

**Preferred term**: Pattern Generator

**Avoided alternatives**:
- Pattern processor: Too generic
- Image converter: Suggests only images
- Input handler: Too generic
- Target parser: Too specific to parsing
- Pattern factory: Suggests creation, not transformation

**Definition**: The component that converts Target specifications into binary matrices.

**Reasoning**: "Pattern Generator" accurately describes the component's role: it generates (produces) patterns from various inputs. The "Generator" suffix is standard for components that produce output.

**Examples**:
- "The Pattern Generator handles multiple input formats."
- "Pattern Generator outputs are validated."
- "New formats can be added to the Pattern Generator."

---

## Agent Terms

### Agent

**Preferred term**: Agent

**Avoided alternatives**:
- Controller: Suggests external control; Agents are part of the system
- Robot: Suggests physical embodiment
- Bot: Too informal
- Player: Suggests a game
- Entity: Too generic

**Definition**: An entity that observes the World and takes actions to guide it toward Target Patterns.

**Reasoning**: "Agent" is the standard term in AI and RL for an entity that perceives and acts. It's well-understood and precise.

**Examples**:
- "Agents observe the World state."
- "Agents make decisions based on their policy."
- "Multiple Agents can coordinate."

---

### Action

**Preferred term**: Action

**Avoided alternatives**:
- Move: Suggests spatial movement; Actions modify state
- Operation: Too generic
- Command: Suggests imperative control
- Step: Too generic
- Intervention: Better, but "Action" is more standard in RL

**Definition**: A decision made by an Agent that modifies the World.

**Reasoning**: "Action" is the standard term in RL for an agent's output. It's precise and well-understood in the context of agent-environment interaction.

**Examples**:
- "Agents select Actions based on their policy."
- "Actions are applied during the Write Phase."
- "Each Action is associated with a Reward."

---

### Policy

**Preferred term**: Policy

**Avoided alternatives**:
- Strategy: Suggests high-level planning; Policy is the mapping
- Algorithm: Suggests the implementation, not the concept
- Brain: Too metaphorical
- Controller: Suggests external control
- Decision function: Too verbose

**Definition**: The mapping from agent perception to action selection.

**Reasoning**: "Policy" is the standard term in RL for the agent's decision-making function. It's precise and well-understood.

**Examples**:
- "The Agent's policy maps perception to action."
- "Policies are learned through experience."
- "Different policies can be compared."

---

### Perception

**Preferred term**: Perception

**Avoided alternatives**:
- Observation: Suggests passive watching; Perception includes feature extraction
- Input: Too generic
- State: Confusing with World state
- View: Suggests visual; Perception includes non-visual information
- Sense: Suggests physical senses

**Definition**: The process by which an Agent observes and interprets World state.

**Reasoning**: "Perception" captures the active nature of observation—it's not just seeing, but interpreting and extracting features. It's standard in robotics and AI.

**Examples**:
- "Perception extracts features from World state."
- "Local Perception sees nearby cells."
- "Global Perception sees the entire World."

---

## Evolution Terms

### Evolution

**Preferred term**: Evolution

**Avoided alternatives**:
- Optimization: Suggests mathematical optimization; Evolution is biological
- Genetic algorithm: Too specific to one implementation
- Learning: Confusing with RL learning
- Adaptation: Suggests individual change; Evolution is population-based
- Search: Suggests exploration; Evolution includes selection

**Definition**: The process of improving strategies, rules, or agents through variation, selection, and reproduction.

**Reasoning**: "Evolution" captures the biological metaphor and the population-based nature of the process. It's the standard term in the field.

**Examples**:
- "Evolution optimizes agent strategies."
- "The Evolution Module manages populations."
- "Evolution uses selection and variation operators."

---

### Population

**Preferred term**: Population

**Avoided alternatives**:
- Pool: Suggests random collection; Population is structured
- Set: Suggests mathematical set; Population has dynamics
- Collection: Too generic
- Group: Too informal
- Ensemble: Suggests combining; Population includes selection

**Definition**: A collection of candidate solutions that evolve together.

**Reasoning**: "Population" is the standard term in evolutionary computation for a group of individuals that evolve. It's precise and well-understood.

**Examples**:
- "The Population contains multiple Genomes."
- "Population size is configurable."
- "Population diversity is monitored."

---

### Genome

**Preferred term**: Genome

**Avoided alternatives**:
- Chromosome: Too biological; Genome is more general
- Vector: Suggests mathematical vector; Genome has structure
- Encoding: Too generic
- Solution: Suggests a single solution; Genome is a representation
- Individual: Confusing with the person; Individual is the member of Population

**Definition**: The encoded representation of a strategy, rule set, or agent configuration that can be evolved.

**Reasoning**: "Genome" connects to biological genetics and is the standard term in evolutionary computation for the data structure that evolution operates on.

**Examples**:
- "Genomes encode strategy parameters."
- "Genomes are modified by mutation and crossover."
- "Genomes are decoded into working solutions."

---

### Fitness

**Preferred term**: Fitness

**Avoided alternatives**:
- Score: Suggests a game; Fitness is a biological measure
- Quality: Too generic
- Performance: Suggests speed; Fitness includes multiple factors
- Value: Confusing with mathematical value
- Merit: Too subjective

**Definition**: A measure of how well a candidate solution performs its task.

**Reasoning**: "Fitness" is the standard term in evolutionary computation for the measure of solution quality. It connects to biological fitness, which measures reproductive success.

**Examples**:
- "Fitness measures target similarity."
- "Selection is based on Fitness."
- "Fitness functions can be composite."

---

### Mutation

**Preferred term**: Mutation

**Avoided alternatives**:
- Variation: Too generic; Variation includes crossover
- Change: Too generic
- Perturbation: Suggests noise; Mutation is directed
- Modification: Too generic
- Alteration: Too generic

**Definition**: A random modification applied to a Genome during evolution.

**Reasoning**: "Mutation" is the standard term in evolutionary computation for random changes to genomes. It connects to biological mutation, which introduces genetic variation.

**Examples**:
- "Mutation rate is configurable."
- "Mutations introduce genetic diversity."
- "Point mutations change single genes."

---

## Learning Terms

### Reinforcement Learning

**Preferred term**: Reinforcement Learning (RL)

**Avoided alternatives**:
- Machine learning: Too broad
- Deep learning: Too specific to neural networks
- Supervised learning: Different paradigm
- Unsupervised learning: Different paradigm
- Trial and error: Too informal

**Definition**: A learning paradigm where agents learn to make decisions by receiving rewards for their actions.

**Reasoning**: "Reinforcement Learning" is the standard term in AI for this learning paradigm. It's precise and well-understood.

**Examples**:
- "Agents learn through Reinforcement Learning."
- "RL algorithms optimize agent policies."
- "RL requires reward signals."

---

### Reward

**Preferred term**: Reward

**Avoided alternatives**:
- Signal: Too generic
- Feedback: Too generic
- Score: Suggests a game
- Utility: Too formal
- Value: Confusing with value functions

**Definition**: A numerical signal indicating how good an Agent's Action was.

**Reasoning**: "Reward" is the standard term in RL for the feedback signal. It's intuitive and well-understood.

**Examples**:
- "Rewards guide agent learning."
- "Reward components include pattern match and efficiency."
- "Delayed rewards require credit assignment."

---

### Episode

**Preferred term**: Episode

**Avoided alternatives**:
- Trial: Suggests experimentation
- Run: Too generic
- Session: Suggests user interaction
- Game: Suggests a game
- Episode: Standard term, but note the redefinition below

**Definition**: A complete sequence of interactions between an Agent and the World, from initial state to terminal state. In Emergence, Episodes may be defined by time periods between Target changes.

**Reasoning**: "Episode" is the standard term in RL for a sequence of interactions. The definition is adapted to Emergence's persistent World.

**Examples**:
- "Each Episode covers one Target transition."
- "Episodes are measured in generations."
- "Episode rewards are summed for learning."

---

## System Terms

### Core Engine

**Preferred term**: Core Engine

**Avoided alternatives**:
- Simulator: Suggests simulation; the Engine coordinates, not simulates
- Runtime: Too generic
- Controller: Suggests external control
- Orchestrator: Too verbose
- Main loop: Too specific to implementation

**Definition**: The central coordinator that manages the simulation loop and ensures lifecycle correctness.

**Reasoning**: "Core Engine" emphasizes the central, essential nature of the component. "Engine" is a standard term for the driving force of a system.

**Examples**:
- "The Core Engine manages the simulation loop."
- "All components connect through the Core Engine."
- "The Core Engine publishes lifecycle events."

---

### Event System

**Preferred term**: Event System

**Avoided alternatives**:
- Message bus: Suggests message passing; Events are published
- Observer pattern: Too specific to design pattern
- Pub/sub: Too informal
- Communication layer: Too generic
- Signal system: Confusing with RL signals

**Definition**: The publish/subscribe message bus through which components communicate.

**Reasoning**: "Event System" accurately describes the component's role: it manages events. It's a standard term in software architecture.

**Examples**:
- "Components communicate through the Event System."
- "Events are published for all significant changes."
- "The Event System decouples components."

---

### Rule Engine

**Preferred term**: Rule Engine

**Avoided alternatives**:
- Rule system: Too generic
- Transition function: Too mathematical
- Behavior system: Too vague
- Cell logic: Too specific to implementation
- Update mechanism: Too generic

**Definition**: The component that defines and applies cell behavior rules.

**Reasoning**: "Rule Engine" is a standard term in software for a component that evaluates and applies rules. It's precise and well-understood.

**Examples**:
- "The Rule Engine defines cell behavior."
- "Multiple Rule Sets can be active."
- "Rule Sets are pluggable and configurable."

---

### Snapshot

**Preferred term**: Snapshot

**Avoided alternatives**:
- Save: Too generic
- Backup: Suggests redundancy; Snapshots are for analysis
- Checkpoint: Suggests resumption; Snapshots are for analysis
- Dump: Too informal
- Export: Suggests external format

**Definition**: A saved state of the World at a specific generation, used for analysis and recovery.

**Reasoning**: "Snapshot" accurately describes a captured moment in time. It's a standard term in computing for saved state.

**Examples**:
- "Snapshots are taken at regular intervals."
- "Snapshots can be loaded for analysis."
- "Incremental Snapshots reduce storage."

---

## Process Terms

### Simulation

**Preferred term**: Simulation

**Avoided alternatives**:
- Run: Too generic
- Execution: Too formal
- Process: Too generic
- Operation: Too generic
- Experiment: Specific to controlled runs; Simulation is continuous

**Definition**: The continuous process of generating successive World states through the application of rules, agent actions, and evolutionary changes.

**Reasoning**: "Simulation" is the standard term for computational modeling of a system. It's precise and well-understood.

**Examples**:
- "The Simulation runs continuously."
- "Simulation parameters are configurable."
- "The Simulation publishes events."

---

### Intervention

**Preferred term**: Intervention

**Avoided alternatives**:
- Modification: Too generic
- Action: Confusing with Agent Action
- Edit: Suggests text editing
- Change: Too generic
- Manipulation: Suggests external control

**Definition**: A modification applied to the World by an Agent or external process.

**Reasoning**: "Intervention" captures the purposeful nature of modifications. It's used in biology and medicine for deliberate changes to a system.

**Examples**:
- "Agents apply Interventions to guide the World."
- "Interventions are logged for analysis."
- "Interventions are atomic and ordered."

---

### Experiment

**Preferred term**: Experiment

**Avoided alternatives**:
- Trial: Suggests experimentation
- Test: Suggests verification
- Run: Too generic
- Study: Too formal
- Investigation: Too formal

**Definition**: A controlled run of the Emergence system with defined parameters, objectives, and measurement.

**Reasoning**: "Experiment" is the standard term in science for a controlled investigation. It captures the scientific nature of Emergence research.

**Examples**:
- "Experiments are defined by parameters."
- "Experiment results are recorded."
- "Experiments are reproducible."

---

## Usage Guidelines

### Consistency Rules

1. **Use preferred terms**: Always use the preferred term from this guide
2. **Avoid avoided alternatives**: Never use avoided alternatives in documentation
3. **Define new terms**: If a new term is needed, add it to this guide
4. **Check existing terms**: Before inventing a new term, check if one already exists

### Documentation Standards

1. **First mention**: Use the full term (e.g., "Persistent World")
2. **Subsequent mentions**: Can use abbreviated form (e.g., "the World")
3. **Definitions**: Always reference this guide for definitions
4. **Code**: Use the same terms in code comments and docstrings

### Code Standards

1. **Class names**: Use preferred terms (e.g., `World`, `Agent`, `Evolution`)
2. **Method names**: Use verb forms (e.g., `observe()`, `act()`, `learn()`)
3. **Variable names**: Use preferred terms (e.g., `world`, `agent`, `fitness`)
4. **Comments**: Use preferred terms in all comments

### Research Paper Standards

1. **Abstract**: Use preferred terms throughout
2. **Introduction**: Define terms on first use
3. **Methods**: Use preferred terms consistently
4. **Results**: Use preferred terms in descriptions
5. **Discussion**: Use preferred terms in conclusions

---

## Examples of Correct Usage

### Correct

- "The World evolves continuously across generations."
- "Agents observe the World state and select actions."
- "Evolution optimizes strategies through selection and variation."
- "The Pattern Generator converts Targets to binary matrices."
- "Reinforcement Learning guides agent policy improvement."

### Incorrect

- "The board evolves continuously across steps." (Wrong terms)
- "Controllers observe the grid and select moves." (Wrong terms)
- "Optimization improves strategies through selection and mutation." (Wrong terms)
- "The image converter processes goals to bitmaps." (Wrong terms)
- "Machine learning guides agent strategy improvement." (Wrong terms)

---

## Summary

This terminology guide ensures consistent communication across the Emergence project. By using these terms consistently in documentation, code, and research papers, we create a clear, precise vocabulary that enables effective communication and reduces confusion.

The terms connect to their biological and computational origins while being precise for the Emergence context. They should be used consistently to maintain clarity and professionalism.
