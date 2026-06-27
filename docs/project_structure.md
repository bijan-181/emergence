# Project Structure

## Directory Hierarchy

```
emergence/
├── core/                    # Simulation engine and core abstractions
├── renderer/                # Visualization and display
├── world/                   # Persistent world state management
├── agents/                  # Intelligent agent system
├── patterns/                # Target pattern processing
├── rl/                      # Reinforcement learning algorithms
├── evolution/               # Evolutionary algorithms
├── experiments/             # Experiment management
├── storage/                 # Persistence and serialization
├── events/                  # Event system
├── configs/                 # Configuration files
├── tests/                   # Test suite
├── docs/                    # Project documentation
├── tools/                   # Development and analysis tools
├── examples/                # Example experiments and configurations
├── data/                    # Runtime data (generated)
├── scripts/                 # Utility scripts
└── benchmarks/              # Performance benchmarks
```

---

## Directory Descriptions

### `core/`

**Purpose**: The simulation engine and core abstractions that everything else depends on.

```
core/
├── __init__.py
├── engine.py               # Main simulation loop and lifecycle
├── loop.py                 # Generation cycle implementation
├── state.py                # State machine for engine phases
├── clock.py                # Simulation timing and control
├── lifecycle.py            # Component lifecycle management
└── api.py                  # Public API surface
```

**What belongs here**:
- The Core Engine class
- Simulation loop logic
- Engine state transitions (running, paused, stopped)
- Timing and synchronization
- Public API that external code uses

**What does NOT belong here**:
- World state (that's in `world/`)
- Specific algorithms (that's in their respective modules)
- Configuration parsing (that's in `configs/`)
- Visualization (that's in `renderer/`)

**Dependencies**: None. This is the foundation layer.

---

### `renderer/`

**Purpose**: Visualization and user interaction. Completely optional—the engine runs without it.

```
renderer/
├── __init__.py
├── base.py                 # Abstract renderer interface
├── window.py               # Windowed display implementation
├── headless.py             # Headless rendering to file
├── terminal.py             # Terminal-based visualization
├── web.py                  # Web-based viewer (future)
├── cell_renderer.py        # Cell state to color mapping
├── overlay.py              # Overlay rendering (targets, agents)
├── interaction.py          # Mouse/keyboard input handling
├── camera.py               # Viewport and navigation
└── palette.py              # Color schemes and themes
```

**What belongs here**:
- All visualization logic
- Display window management
- User input handling
- Color mapping and rendering
- Camera/viewport control
- Any code that produces visual output

**What does NOT belong here**:
- World state computation (that's in `world/`)
- Agent decision-making (that's in `agents/`)
- Simulation control (that's in `core/`)
- Data persistence (that's in `storage/`)

**Dependencies**: `core/` (for engine status), `world/` (for state to render), `events/` (for updates)

---

### `world/`

**Purpose**: The persistent cellular world. This is the heart of Emergence.

```
world/
├── __init__.py
├── grid.py                 # 2D grid implementation
├── cell.py                 # Cell state and properties
├── world.py                # World container and management
├── neighbors.py            # Neighborhood computation
├── region.py               # Spatial region queries
├── boundary.py             # Edge/wrapping behavior
├── snapshot.py             # State capture and restore
├── diff.py                 # State difference computation
├── history.py              # State history ring buffer
└── spatial.py              # Spatial indexing and queries
```

**What belongs here**:
- Grid data structure
- Cell representation
- Spatial queries (neighbors, regions)
- State snapshotting
- History management
- Boundary conditions (wrapping, walls)

**What does NOT belong here**:
- Rule computation (that's in `core/` via Rule Engine)
- Agent observation (that's in `agents/`)
- Pattern matching (that's in `patterns/`)
- Serialization (that's in `storage/`)

**Dependencies**: None. This is a core data structure.

---

### `agents/`

**Purpose**: Intelligent agents that observe and control the world.

```
agents/
├── __init__.py
├── base.py                 # Abstract agent interface
├── reactive.py             # Simple reactive agents
├── deliberative.py         # Planning-based agents
├── learning.py             # Learning-enabled agents
├── social.py               # Multi-agent coordination
├── meta.py                 # Agent management agents
├── perception.py           # World observation and feature extraction
├── action.py               # Action definitions and application
├── policy.py               # Policy interface and base classes
├── experience.py           # Experience buffer and replay
└── metrics.py              # Agent performance tracking
```

**What belongs here**:
- Agent class hierarchy
- Perception and observation
- Action definitions
- Policy interfaces
- Experience storage
- Agent lifecycle

**What does NOT belong here**:
- Specific RL algorithms (that's in `rl/`)
- Evolutionary optimization (that's in `evolution/`)
- World state management (that's in `world/`)
- Visualization of agents (that's in `renderer/`)

**Dependencies**: `world/` (for observation), `events/` (for communication), `rl/` (for learning)

---

### `patterns/`

**Purpose**: Target pattern processing and management.

```
patterns/
├── __init__.py
├── generator.py            # Main pattern generator
├── input/                  # Input format handlers
│   ├── text.py             # Text string rendering
│   ├── image.py            # Image file processing
│   ├── svg.py              # SVG path processing
│   ├── ascii.py            # ASCII art processing
│   ├── binary.py           # Binary matrix input
│   └── procedural.py       # Procedural generation
├── processing/             # Pattern processing pipeline
│   ├── normalize.py        # Normalization
│   ├── scale.py            # Scaling and resizing
│   ├── binarize.py         # Thresholding and binarization
│   └── validate.py         # Validation and error handling
├── schedule.py             # Target scheduling and sequencing
├── matcher.py              # Pattern matching and detection
└── metrics.py              # Pattern similarity metrics
```

**What belongs here**:
- Target input parsing
- Format detection
- Pattern processing pipeline
- Target scheduling
- Pattern matching

**What does NOT belong here**:
- World state modification (that's in `core/` via Rule Engine)
- Agent decision-making (that's in `agents/`)
- Visualization of targets (that's in `renderer/`)
- Storage of targets (that's in `storage/`)

**Dependencies**: None (pure processing)

---

### `rl/`

**Purpose**: Reinforcement learning algorithms.

```
rl/
├── __init__.py
├── base.py                 # Abstract RL interface
├── qlearning/              # Q-Learning family
│   ├── __init__.py
│   ├── q_table.py          # Tabular Q-learning
│   ├── dqn.py              # Deep Q-Network
│   └── dueling.py          # Dueling DQN
├── policy/                 # Policy gradient family
│   ├── __init__.py
│   ├── reinforce.py        # REINFORCE algorithm
│   ├── a2c.py              # Advantage Actor-Critic
│   └── ppo.py              # Proximal Policy Optimization
├── multi_agent/            # Multi-agent RL
│   ├── __init__.py
│   ├── independent.py      # Independent learners
│   ├── central.py          # Centralized training
│   └── communication.py    # Learned communication
├── state/                  # State representation
│   ├── __init__.py
│   ├── raw.py              # Raw cell states
│   ├── features.py         # Feature extraction
│   └── encoding.py         # State encoding
├── reward/                 # Reward computation
│   ├── __init__.py
│   ├── components.py       # Individual reward components
│   ├── composite.py        # Composite reward functions
│   └── shaping.py          # Reward shaping
└── buffers/                # Experience storage
    ├── __init__.py
    ├── replay.py           # Experience replay buffer
    └── priority.py         # Prioritized replay
```

**What belongs here**:
- Specific RL algorithm implementations
- Neural network architectures for RL
- State and action space definitions
- Reward computation
- Experience replay

**What does NOT belong here**:
- Agent logic (that's in `agents/`)
- World state (that's in `world/`)
- Training loop (that's in `core/`)
- Configuration (that's in `configs/`)

**Dependencies**: `agents/` (for agent interface), `world/` (for state access)

---

### `evolution/`

**Purpose**: Evolutionary algorithms for strategy optimization.

```
evolution/
├── __init__.py
├── base.py                 # Abstract evolution interface
├── population.py           # Population management
├── selection.py            # Selection operators
├── variation.py            # Variation operators
├── fitness.py              # Fitness evaluation
├── genome.py               # Genome representation
├── species.py              # Speciation and niching
├── operators/              # Specific operators
│   ├── mutation.py         # Mutation operators
│   ├── crossover.py        # Crossover operators
│   └── recombination.py    # Recombination operators
├── strategies/             # Evolution strategies
│   ├── genetic.py          # Standard genetic algorithm
│   ├── evolutionary.py     # Evolution strategies (ES)
│   ├── differential.py     # Differential evolution
│   └── cooperative.py      # Cooperative coevolution
└── metrics.py              # Population statistics
```

**What belongs here**:
- Population representation
- Selection mechanisms
- Variation operators
- Fitness evaluation framework
- Evolutionary strategy implementations

**What does NOT belong here**:
- Specific fitness functions for Emergence (that's in `experiments/`)
- Agent learning (that's in `rl/`)
- World simulation (that's in `core/`)
- Visualization of evolution (that's in `renderer/`)

**Dependencies**: `core/` (for fitness evaluation runs), `configs/` (for parameters)

---

### `experiments/`

**Purpose**: Experiment definition, management, and results.

```
experiments/
├── __init__.py
├── manager.py              # Experiment lifecycle management
├── definition.py           # Experiment definition schema
├── runner.py               # Experiment execution
├── monitor.py              # Runtime monitoring
├── results.py              # Results collection and analysis
├── reproducibility.py      # Reproducibility guarantees
├── templates/              # Experiment templates
│   ├── basic.py            # Basic pattern matching
│   ├── evolution.py        # Evolutionary experiments
│   ├── multi_target.py     # Multiple target experiments
│   └── long_running.py     # Extended duration experiments
└── examples/               # Example experiment configurations
    └── ...
```

**What belongs here**:
- Experiment lifecycle management
- Parameter validation
- Results collection
- Monitoring and logging
- Experiment templates

**What does NOT belong here**:
- Core simulation (that's in `core/`)
- Algorithm implementations (that's in their modules)
- Storage mechanics (that's in `storage/`)
- Visualization (that's in `renderer/`)

**Dependencies**: `core/`, `world/`, `agents/`, `rl/`, `evolution/`, `patterns/`, `storage/`

---

### `storage/`

**Purpose**: Persistence, serialization, and data management.

```
storage/
├── __init__.py
├── base.py                 # Abstract storage interface
├── world_store.py          # World state persistence
├── snapshot.py             # Snapshot management
├── config_store.py         # Configuration persistence
├── results_store.py        # Experiment results storage
├── formats/                # Serialization formats
│   ├── binary.py           # Binary format
│   ├── json.py             # JSON format
│   ├── hdf5.py             # HDF5 format (optional)
│   └── sqlite.py           # SQLite format (optional)
├── compression.py          # Compression strategies
├── indexing.py             # Data indexing and retrieval
├── backup.py               # Backup and recovery
└── cache.py                # Caching layer
```

**What belongs here**:
- Serialization and deserialization
- File I/O operations
- Data indexing
- Caching
- Backup and recovery

**What does NOT belong here**:
- World state logic (that's in `world/`)
- Experiment logic (that's in `experiments/`)
- Configuration parsing (that's in `configs/`)
- Algorithm state management (that's in their modules)

**Dependencies**: `world/` (for what to store), `configs/` (for storage settings)

---

### `events/`

**Purpose**: Event system for component communication.

```
events/
├── __init__.py
├── bus.py                  # Event bus implementation
├── publisher.py            # Event publishing interface
├── subscriber.py           # Event subscription interface
├── handler.py              # Event handler base class
├── types.py                # Event type definitions
├── queue.py                # Event queue and ordering
├── logger.py               # Event logging
└── replay.py               # Event replay
```

**What belongs here**:
- Event bus (publish/subscribe)
- Event type definitions
- Event queue management
- Event logging
- Event replay capability

**What does NOT belong here**:
- Specific event handling logic (that's in consuming components)
- World state modification (that's in `world/`)
- Agent actions (that's in `agents/`)
- Persistence (that's in `storage/`)

**Dependencies**: None (communication infrastructure)

---

### `configs/`

**Purpose**: Configuration management and defaults.

```
configs/
├── __init__.py
├── loader.py               # Configuration loading
├── validator.py            # Configuration validation
├── defaults.py             # Default values
├── schema.py               # Configuration schema
├── overrides.py            # Override handling
├── environment.py          # Environment variable handling
└── files/                  # Default configuration files
    ├── default.toml        # System defaults
    ├── experiments/        # Experiment-specific configs
    └── agents/             # Agent-specific configs
```

**What belongs here**:
- Configuration file parsing
- Parameter validation
- Default value management
- Override handling
- Schema definitions

**What does NOT belong here**:
- Runtime parameter access (use the loaded config objects)
- Algorithm-specific configuration (that's in their modules)
- File I/O mechanics (that's in `storage/`)

**Dependencies**: None (configuration infrastructure)

---

### `tests/`

**Purpose**: Test suite for all components.

```
tests/
├── __init__.py
├── conftest.py             # Pytest fixtures
├── unit/                   # Unit tests
│   ├── test_engine.py
│   ├── test_world.py
│   ├── test_agents.py
│   ├── test_patterns.py
│   ├── test_rl.py
│   ├── test_evolution.py
│   ├── test_storage.py
│   └── test_events.py
├── integration/            # Integration tests
│   ├── test_agent_world.py
│   ├── test_rl_agent.py
│   ├── test_experiment.py
│   └── test_persistence.py
├── system/                 # System tests
│   ├── test_full_run.py
│   ├── test_long_running.py
│   └── test_recovery.py
└── benchmarks/             # Performance benchmarks
    ├── bench_world.py
    ├── bench_rules.py
    └── bench_render.py
```

**What belongs here**:
- Unit tests for individual components
- Integration tests for component interactions
- System tests for full experiments
- Performance benchmarks
- Test fixtures and helpers

**What does NOT belong here**:
- Production code
- Configuration files
- Documentation
- Example experiments

**Dependencies**: All other modules (for testing)

---

### `docs/`

**Purpose**: Project documentation.

```
docs/
├── vision.md               # Project vision and philosophy
├── architecture.md         # System architecture
├── project_structure.md    # This file
├── roadmap.md              # Development roadmap
├── decisions.md            # Architecture decision records
├── concepts.md             # Concept definitions
├── terminology.md          # Terminology guide
├── physics/                # Physics module documentation
│   ├── README.md           # Physics module overview
│   ├── world_physics.md    # Physical properties of the universe
│   ├── game_of_life_rules.md # Cellular automata rules
│   ├── intervention_rules.md # Agent interaction rules
│   └── timing_model.md     # Execution timeline
├── api/                    # API documentation (future)
├── guides/                 # User guides (future)
└── research/               # Research notes (future)
```

**What belongs here**:
- Project documentation
- Architecture decisions
- Concept definitions
- Research notes
- User guides

**What does NOT belong here**:
- Code
- Configuration
- Test data
- Generated files

**Dependencies**: References all other modules

---

### `tools/`

**Purpose**: Development and analysis utilities.

```
tools/
├── __init__.py
├── analysis.py             # World state analysis
├── visualization.py        # Debug visualization
├── migration.py            # Data migration between versions
├── profiling.py            # Performance profiling
├── debugging.py            # Debugging utilities
└── scripts/                # Utility scripts
    ├── generate_report.py
    ├── convert_data.py
    └── benchmark.py
```

**What belongs here**:
- Development utilities
- Analysis tools
- Migration scripts
- Profiling code
- Debugging helpers

**What does NOT belong here**:
- Core simulation code
- Production algorithms
- Test code
- Documentation

**Dependencies**: Various modules (for analysis)

---

### `examples/`

**Purpose**: Example experiments and configurations.

```
examples/
├── basic/                  # Basic examples
│   ├── hello_world.toml
│   └── simple_pattern.toml
├── evolution/              # Evolutionary examples
│   ├── evolve_rules.toml
│   └── evolve_agents.toml
├── multi_target/           # Multiple target examples
│   ├── sequence.toml
│   └── animation.toml
├── long_running/           # Extended experiments
│   ├── day_long.toml
│   └── week_long.toml
└── README.md               # Example documentation
```

**What belongs here**:
- Example configuration files
- Example experiment definitions
- Documentation for examples
- Sample data

**What does NOT belong here**:
- Core code
- Tests
- Documentation (other than example-specific)

**Dependencies**: References `configs/` and `experiments/`

---

### `data/`

**Purpose**: Runtime data (generated, not committed).

```
data/
├── worlds/                 # World state files
├── snapshots/              # World snapshots
├── experiments/            # Experiment results
├── logs/                   # System logs
├── cache/                  # Temporary cache
└── .gitkeep                # Keep directory in git
```

**Note**: This directory is generated at runtime. It should be in `.gitignore`.

---

### `scripts/`

**Purpose**: Utility and setup scripts.

```
scripts/
├── setup.py                # Project setup
├── install.sh              # Installation script
├── benchmark.sh            # Benchmark runner
├── clean.sh                # Cleanup script
└── ci/                     # CI/CD scripts
    ├── test.sh
    ├── lint.sh
    └── deploy.sh
```

**What belongs here**:
- Setup and installation scripts
- CI/CD scripts
- Utility shell scripts
- Build scripts

**What does NOT belong here**:
- Python code (use appropriate modules)
- Documentation
- Configuration

**Dependencies**: Project root files

---

### `benchmarks/`

**Purpose**: Performance benchmarks and profiling.

```
benchmarks/
├── __init__.py
├── world_bench.py          # World operation benchmarks
├── rule_bench.py           # Rule computation benchmarks
├── render_bench.py         # Rendering benchmarks
├── storage_bench.py        # Storage benchmarks
├── rl_bench.py             # RL algorithm benchmarks
├── results/                # Benchmark results
└── README.md               # Benchmark documentation
```

**What belongs here**:
- Performance benchmark code
- Profiling scripts
- Benchmark results
- Performance documentation

**What does NOT belong here**:
- Unit tests (use `tests/`)
- Production code
- Configuration

**Dependencies**: All modules (for benchmarking)

---

## Dependency Rules

### Layer Architecture

The codebase follows a layered architecture with strict dependency rules:

```
Layer 4: applications/
         │
Layer 3: experiments/ agents/ rl/ evolution/
         │
Layer 2: patterns/ storage/ events/ configs/
         │
Layer 1: core/ world/
         │
Layer 0: (external libraries)
```

### Rules

1. **Lower layers never depend on higher layers**
   - `core/` cannot import from `agents/`
   - `world/` cannot import from `rl/`

2. **Same-layer dependencies are allowed but discouraged**
   - `agents/` can import from `rl/` (for learning)
   - But prefer interfaces over concrete implementations

3. **Cross-layer dependencies must go through interfaces**
   - Use abstract base classes defined in lower layers
   - Never import concrete implementations from other layers

4. **External dependencies must be justified**
   - Document why each external library is needed
   - Prefer standard library when possible
   - Consider maintenance and security implications

5. **Configuration is global**
   - All modules can access configuration
   - But modules should not modify configuration at runtime

### Import Rules

```python
# ALLOWED: Lower layer import
from core.engine import Engine

# ALLOWED: Same layer with interface
from agents.base import Agent

# FORBIDDEN: Higher layer import
from experiments.manager import ExperimentManager  # In core/

# FORBIDDEN: Circular import
# If A imports B and B imports A, restructure the code
```

### File Organization Rules

1. One class per file (for significant classes)
2. Related small classes can share a file
3. `__init__.py` files should be minimal (re-exports only)
4. Test files mirror source structure
5. Configuration files use TOML format

---

## Adding New Components

### New Rule Set

1. Create `core/rules/my_rule.py`
2. Implement `RuleSet` interface
3. Add configuration schema
4. Write unit tests
5. Update documentation

### New Agent Type

1. Create `agents/my_agent.py`
2. Implement `Agent` interface
3. Add configuration schema
4. Write unit tests
5. Update documentation

### New RL Algorithm

1. Create `rl/my_algorithm/` directory
2. Implement algorithm classes
3. Add configuration schema
4. Write unit tests
5. Update documentation

### New Storage Format

1. Create `storage/formats/my_format.py`
2. Implement serialization/deserialization
3. Add configuration options
4. Write unit tests
5. Update documentation

---

## Naming Conventions

### Files
- Lowercase with underscores: `my_module.py`
- Test files: `test_my_module.py`
- Configuration files: `my_config.toml`

### Classes
- PascalCase: `MyModule`
- Interfaces: `IMyInterface` or `MyInterface`
- Abstract classes: `AbstractMyClass` or `BaseMyClass`

### Functions
- Lowercase with underscores: `my_function()`
- Private functions: `_my_function()`
- Test functions: `test_my_function()`

### Variables
- Lowercase with underscores: `my_variable`
- Constants: `MY_CONSTANT`
- Private variables: `_my_variable`

### Configuration Keys
- Lowercase with underscores: `my_parameter`
- Namespaced: `module.my_parameter`

---

## Summary

This structure provides:

1. **Clear separation of concerns**: Each directory has a single responsibility
2. **Scalable organization**: New components fit naturally into the hierarchy
3. **Dependency management**: Layer architecture prevents circular dependencies
4. **Testability**: Clear separation makes testing straightforward
5. **Maintainability**: Predictable file locations reduce cognitive load
6. **Extensibility**: Adding new components follows established patterns

The structure is designed to support the project from prototype to mature research platform, growing organically as the project evolves.
