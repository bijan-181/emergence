# Architecture Decision Records

## Overview

This document records architectural decisions for the Emergence project. Each decision is documented using a standard ADR format, providing context, rationale, and consequences.

ADRs are immutable once accepted. If a decision needs to be reversed or modified, a new ADR is created that supersedes the old one.

---

## ADR-001: The World Is Persistent

**Decision ID**: ADR-001

**Status**: Accepted

**Date**: 2024-01-15

### Context

Emergence is a research platform for exploring artificial life through cellular automata. The fundamental question is how to represent the world state.

Traditional approaches treat the world as ephemeral: create a world, run an experiment, discard the world, start fresh. This approach is simple and well-understood.

However, biological systems are fundamentally persistent. An organism's current state is the accumulated result of its entire history. Discarding state between experiments eliminates the mechanism through which biological complexity arises.

### Decision

The world is persistent. Once created, the world state is never discarded. All modifications accumulate. The world at any point in time reflects its entire history.

### Consequences

**Positive**:
- Enables genuine evolutionary dynamics
- Creates historical depth and memory
- Allows study of long-term emergent behavior
- Mirrors biological reality

**Negative**:
- Increased storage requirements
- More complex state management
- Potential for state degradation over time
- Requires careful snapshot management

**Risks**:
- World may accumulate unwanted patterns
- Storage may grow unbounded without management
- Long-running simulations may encounter bugs not present in short runs

### Alternatives Considered

1. **Ephemeral world with snapshots**: Create new worlds, save periodic snapshots. Rejected because it doesn't capture the continuous nature of biological persistence.

2. **Reset on demand**: Allow world reset for new experiments. Rejected because it violates the persistence principle and enables lazy experimentation.

3. **Multiple persistent worlds**: Allow creating new worlds while keeping old ones. Rejected for now to focus on single-world dynamics; may revisit in future.

### Reasoning

Persistence is the central idea of Emergence. Without it, Emergence becomes just another cellular automata simulator. The research questions that Emergence asks—about long-term dynamics, emergent intelligence, and guided self-organization—require persistence. The costs are manageable with proper engineering.

---

## ADR-002: The World Never Resets

**Decision ID**: ADR-002

**Status**: Accepted

**Date**: 2024-01-15

### Context

Building on ADR-001, the question arises: should the world ever be reset?

Resetting is tempting for several reasons:
- Clean slate for new experiments
- Easier to reproduce results
- Simpler state management
- Familiar paradigm from other simulators

However, resetting contradicts the biological metaphor. In nature, mass extinctions destroy much structure but never everything. Survivors carry forward the legacy of what came before.

### Decision

The world is never reset. When a new target pattern is requested, the existing world gradually reorganizes itself. The transition from one pattern to another is a living process, not a replacement.

### Consequences

**Positive**:
- Every experiment builds on previous ones
- The world develops genuine history
- Transitions between patterns create emergent dynamics
- No information is ever lost

**Negative**:
- Previous patterns influence subsequent ones
- World may carry "scars" from past experiments
- Requires careful transition management
- May be confusing for users expecting clean experiments

**Risks**:
- World may become pathological over time
- Previous patterns may interfere with new targets
- Users may need to understand world history to interpret results

### Alternatives Considered

1. **Soft reset**: Gradually clear the world before new target. Rejected because it still discards information.

2. **History-aware reset**: Reset but preserve key historical features. Rejected because it's complex and still loses information.

3. **World branching**: Create new world from old state. Rejected for now; may revisit for specific use cases.

### Reasoning

Never resetting is a stronger commitment to persistence than ADR-001 alone. It ensures that the world's history is always present and influential. This creates richer dynamics and more interesting research questions. The challenges of managing accumulated state are worth the benefits.

---

## ADR-003: Rendering Is Separated from Simulation

**Decision ID**: ADR-003

**Status**: Accepted

**Date**: 2024-01-15

### Context

The relationship between simulation and visualization needs to be defined.

Tight coupling (rendering integrated with simulation) is simpler to implement and understand. It's the default in many small projects.

However, coupling creates several problems:
- Simulation cannot run without rendering
- Rendering overhead slows simulation
- Headless operation (for experiments) is difficult
- Testing is harder (rendering is hard to unit test)
- Multiple visualization options are difficult to support

### Decision

Rendering is completely separated from simulation. The simulation engine runs independently of any renderer. The renderer connects to the engine through a well-defined interface and subscribes to events.

### Consequences

**Positive**:
- Simulation runs without rendering
- Headless experiments are straightforward
- Multiple renderers can be supported
- Testing is easier
- Performance is not affected by rendering

**Negative**:
- More complex architecture
- Requires event system for communication
- Renderer may lag behind simulation
- Debugging requires separate tools

**Risks**:
- Interface may be too rigid for some use cases
- Event system may add overhead
- Renderer may not have access to all needed information

### Alternatives Considered

1. **Integrated rendering**: Rendering built into simulation. Rejected because it violates separation of concerns and prevents headless operation.

2. **Optional rendering**: Rendering can be toggled on/off. Rejected because it still couples the components, just with a flag.

3. **Rendering as plugin**: Rendering loaded dynamically. Rejected for now; may revisit for advanced plugin systems.

### Reasoning

Separation of rendering from simulation is a well-established best practice for simulation systems. It enables the core research use case (running experiments without visualization) while supporting the user-facing use case (interactive visualization). The additional complexity is manageable and worth the flexibility.

---

## ADR-004: Target Patterns Are Generic Binary Matrices

**Decision ID**: ADR-004

**Status**: Accepted

**Date**: 2024-01-15

### Context

The world needs to know what pattern to embody. How should target patterns be represented?

Options include:
- Specific formats (text, images, vectors)
- Abstract representations (feature vectors, embeddings)
- Binary matrices (cell on/off)

Specific formats limit what targets can be specified. Abstract representations are complex and may not map cleanly to cellular automata.

### Decision

Target patterns are generic binary matrices. Any target input (text, image, SVG, etc.) is processed into a binary matrix that the world can embody. The binary matrix is the universal intermediate representation.

### Consequences

**Positive**:
- Simple, universal representation
- Direct mapping to cell states
- Easy to compare with world state
- Supports any visual pattern

**Negative**:
- Limited to binary (on/off) patterns
- No color or gradient information
- Requires format conversion for diverse inputs
- May lose information during binarization

**Risks**:
- Binary limitation may be too restrictive
- Binarization threshold may be difficult to choose
- Some patterns may not binarize well

### Alternatives Considered

1. **Multi-state patterns**: Allow patterns with multiple cell states. Rejected for now to keep the problem tractable; may revisit if binary is too limiting.

2. **Feature-based patterns**: Specify patterns by features (density, symmetry) rather than exact layout. Rejected because it's harder to define and evaluate.

3. **Direct input formats**: Handle each input format separately. Rejected because it's complex and doesn't provide a unified representation.

### Reasoning

Binary matrices are the natural representation for cellular automata. They're simple, universal, and directly mappable to the world state. The binarization step handles diverse inputs. Multi-state patterns can be added later if needed, but binary provides a strong foundation.

---

## ADR-005: AI Manipulates Current World, Not Generates New Worlds

**Decision ID**: ADR-005

**Status**: Accepted

**Date**: 2024-01-15

### Context

The role of artificial intelligence in Emergence needs to be defined.

Options include:
- AI generates world states from scratch
- AI manipulates existing world toward targets
- AI does both depending on context

Generating from scratch is simpler but ignores the persistence principle. If AI can just generate the target pattern, the existing world state is irrelevant.

### Decision

AI manipulates the current world toward target patterns. It observes the current state and takes actions to guide the world toward the target. It never generates a new world state from scratch.

### Consequences

**Positive**:
- Respects persistence principle
- AI must work with existing structure
- Creates interesting optimization problems
- Preserves world history

**Negative**:
- AI may not be able to achieve target from current state
- Transition may be slow or impossible
- AI must understand current state deeply
- More complex than generation from scratch

**Risks**:
- Some targets may be unreachable from current state
- AI may get stuck in local optima
- Transition may destroy valuable structure

### Alternatives Considered

1. **Generate from scratch**: AI creates target pattern directly. Rejected because it ignores persistence and the existing world.

2. **Hybrid approach**: Generate when far from target, manipulate when close. Rejected because it's complex and violates the persistence principle.

3. **AI chooses strategy**: AI decides whether to generate or manipulate. Rejected because it gives AI too much control over fundamental architecture.

### Reasoning

Manipulating the current world is the only approach that respects persistence. It creates a rich optimization problem: how to transform one pattern into another while preserving as much structure as possible. This is more interesting and more biologically relevant than generation from scratch.

---

## ADR-006: Every Subsystem Is Replaceable

**Decision ID**: ADR-006

**Status**: Accepted

**Date**: 2024-01-15

### Context

Emergence is a research platform. Research involves experimentation, which requires flexibility. If subsystems are not replaceable, the platform cannot adapt to new research questions.

### Decision

Every subsystem (Rule Engine, RL Algorithm, Evolution Strategy, Renderer, Storage Backend) is replaceable. Each subsystem is defined by an interface. Implementations can be swapped without affecting other components.

### Consequences

**Positive**:
- Research can explore different approaches
- No lock-in to specific algorithms
- Components can be improved independently
- Community can contribute alternatives

**Negative**:
- Interface design is critical and difficult
- May add abstraction overhead
- Testing becomes more complex
- Documentation must cover multiple implementations

**Risks**:
- Interfaces may be too rigid or too flexible
- Replacements may not be compatible
- Performance may vary across implementations

### Alternatives Considered

1. **Fixed subsystems**: Choose one implementation for each. Rejected because it limits research flexibility.

2. **Plugin system**: Dynamic loading of implementations. Rejected for now as over-engineering; may revisit later.

3. **Configuration-based**: Choose implementations through configuration. This is the chosen approach, but with well-defined interfaces.

### Reasoning

Replaceability is essential for a research platform. It enables exploration, comparison, and improvement. The cost of well-defined interfaces is worth the flexibility they provide.

---

## ADR-007: The Engine Remains Independent from Visualization

**Decision ID**: ADR-007

**Status**: Accepted

**Date**: 2024-01-15

### Context

This is a refinement of ADR-003, specifically addressing the core engine's relationship to visualization.

The core engine is the heart of the simulation. If it depends on visualization, it cannot run headless, testing is difficult, and performance suffers.

### Decision

The core engine has no dependency on visualization code. It communicates with renderers exclusively through the event system. The engine can be imported and used without any visualization library.

### Consequences

**Positive**:
- Engine is self-contained
- Headless operation is guaranteed
- Testing is straightforward
- Performance is not affected by visualization

**Negative**:
- Engine cannot directly update visualization
- Must use events for all communication
- Renderer may lag behind engine state
- Debugging requires separate tools

**Risks**:
- Event system may add latency
- Renderer may miss events
- Engine state may be stale when renderer reads it

### Alternatives Considered

1. **Engine provides state access**: Engine has methods for renderer to query state. Rejected because it couples engine to renderer needs.

2. **Engine updates renderer directly**: Engine calls renderer methods. Rejected because it creates hard dependency.

3. **Shared state**: Engine and renderer share state object. Rejected because it creates race conditions and coupling.

### Reasoning

Engine independence from visualization is critical for the research use case. Experiments must run without visualization. The event system provides a clean, decoupled interface. Any latency or staleness is acceptable for the benefits.

---

## ADR-008: Documentation Is the Project's Source of Truth

**Decision ID**: ADR-008

**Status**: Accepted

**Date**: 2024-01-15

### Context

In many projects, documentation lags behind code. Code becomes the source of truth, and documentation is outdated or incomplete.

This creates problems:
- New contributors cannot understand the project
- Decisions are not recorded
- Architecture is not documented
- Research context is lost

### Decision

Documentation is the project's source of truth. Before any code is written, the architecture, decisions, and concepts are documented. Code must follow documentation, not the other way around.

### Consequences

**Positive**:
- Clear vision before implementation
- Decisions are recorded and justified
- New contributors can understand the project
- Research context is preserved

**Negative**:
- Documentation must be maintained
- May slow initial development
- Documentation may diverge from code
- Requires discipline to keep in sync

**Risks**:
- Documentation may be too rigid
- Code may need to deviate from documentation
- Documentation may become outdated

### Alternatives Considered

1. **Code-first**: Write code, document later. Rejected because it leads to unclear vision and lost context.

2. **Documentation as code**: Use code comments as documentation. Rejected because it doesn't provide high-level architecture.

3. **README only**: Minimal documentation. Rejected because it doesn't provide sufficient detail for a research platform.

### Reasoning

For a research platform, documentation is essential. It records not just what the code does, but why it does it. It provides the context that makes the code meaningful. Treating documentation as source of truth ensures this context is preserved.

---

## ADR-009: Use TOML for Configuration

**Decision ID**: ADR-009

**Status**: Accepted

**Date**: 2024-01-15

### Context

Configuration files need a format. Options include:
- YAML: Popular, human-readable, but complex syntax
- JSON: Universal, but verbose and no comments
- TOML: Simple, explicit, supports comments
- INI: Simple, but limited nesting
- Python: Flexible, but security concerns

### Decision

Use TOML for configuration files. TOML provides a good balance of simplicity, expressiveness, and human-readability.

### Consequences

**Positive**:
- Simple, readable syntax
- Supports comments
- Good type system
- Growing ecosystem support

**Negative**:
- Less common than YAML
- Limited nesting compared to YAML
- Smaller tooling ecosystem
- May require custom parsing for complex cases

**Risks**:
- Contributors may not know TOML
- Complex configurations may be awkward
- Tooling support may be limited

### Alternatives Considered

1. **YAML**: More popular, but complex syntax and gotchas (indentation, type inference). Rejected for simplicity.

2. **JSON**: Universal, but verbose and no comments. Rejected for readability.

3. **INI**: Simple, but limited nesting. Rejected for expressiveness.

4. **Python files**: Flexible, but security concerns. Rejected for safety.

### Reasoning

TOML is the right choice for a project that values clarity and simplicity. It's easy to read, easy to write, and supports comments. The trade-off of less popularity is worth the benefits.

---

## ADR-010: Use Python as Primary Language

**Decision ID**: ADR-010

**Status**: Accepted

**Date**: 2024-01-15

### Context

The primary implementation language needs to be chosen. Options include:
- Python: Easy to learn, rich ecosystem, slow execution
- C++: Fast execution, complex development
- Rust: Fast execution, memory safety, learning curve
- JavaScript: Web-friendly, limited scientific computing
- Julia: Fast execution, scientific focus, smaller ecosystem

### Decision

Use Python as the primary language. Performance-critical components can use NumPy, Numba, or C extensions.

### Consequences

**Positive**:
- Easy to learn and contribute
- Rich scientific computing ecosystem
- Excellent for research and prototyping
- Large community and resources

**Negative**:
- Slower than compiled languages
- GIL limits true parallelism
- Memory usage is higher
- Packaging can be complex

**Risks**:
- Performance may be insufficient for large-scale experiments
- GIL may limit scalability
- Dependencies may conflict

### Alternatives Considered

1. **C++**: Maximum performance, but high development cost. Rejected for development speed.

2. **Rust**: Performance and safety, but learning curve. Rejected for community size.

3. **Julia**: Performance and scientific focus, but smaller ecosystem. Rejected for ecosystem size.

4. **Mixed languages**: Python for orchestration, C++ for hot paths. This is the chosen approach for performance-critical components.

### Reasoning

Python is the right choice for a research platform. It enables rapid development, easy contribution, and integration with scientific tools. Performance-critical components can use compiled extensions. The trade-off of raw performance is worth the benefits in development speed and accessibility.

---

## Summary

These ADRs establish the fundamental architectural principles of Emergence:

1. **Persistence**: The world is persistent (ADR-001)
2. **No Reset**: The world never resets (ADR-002)
3. **Separation**: Rendering is separated from simulation (ADR-003, ADR-007)
4. **Universality**: Target patterns are binary matrices (ADR-004)
5. **Manipulation**: AI manipulates, not generates (ADR-005)
6. **Replaceability**: Every subsystem is replaceable (ADR-006)
7. **Documentation**: Documentation is source of truth (ADR-008)
8. **Simplicity**: TOML for configuration (ADR-009)
9. **Accessibility**: Python as primary language (ADR-010)

These decisions will guide the project's development and ensure consistency as it grows.

**Note**: The physical laws governing the Emergence universe are documented in `docs/physics/`. These decisions operate within those physical constraints.
