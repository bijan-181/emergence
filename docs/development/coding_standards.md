# Coding Standards

## Overview

This document defines the coding standards for the Emergence project. These standards ensure consistency, readability, and maintainability across the codebase.

---

## Python Style

### General Rules

1. Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
2. Maximum line length: 88 characters (Black default)
3. Use consistent indentation: 4 spaces
4. Use blank lines to separate logical sections
5. Use type hints for all public functions

### Example

```python
from typing import Optional

def calculate_fitness(
    world_state: WorldState,
    target_pattern: BinaryPattern,
    weight: float = 1.0
) -> float:
    """Calculate fitness score for world state.
    
    Args:
        world_state: Current world state to evaluate.
        target_pattern: Target pattern to match against.
        weight: Weight factor for fitness calculation.
    
    Returns:
        Fitness score between 0.0 and 1.0.
    """
    similarity = compute_similarity(world_state, target_pattern)
    return similarity * weight
```

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

```python
class World:
    """Manages persistent world state."""
    pass

class AbstractAgent:
    """Base class for all agents."""
    pass

class IRuleSet:
    """Interface for rule sets."""
    pass
```

### Functions

- Lowercase with underscores: `my_function()`
- Private functions: `_my_function()`
- Test functions: `test_my_function()`

```python
def compute_neighborhood(grid: Grid, x: int, y: int) -> list[Cell]:
    """Compute neighborhood for cell at position."""
    pass

def _validate_state(state: WorldState) -> bool:
    """Validate world state internally."""
    pass
```

### Variables

- Lowercase with underscores: `my_variable`
- Constants: `MY_CONSTANT`
- Private variables: `_my_variable`

```python
MAX_WORLD_SIZE = 1000
current_generation = 0
_private_cache = {}
```

### Configuration Keys

- Lowercase with underscores: `my_parameter`
- Namespaced: `module.my_parameter`

```toml
[world]
max_size = 1000
boundary = "wrap"

[agents]
learning_rate = 0.001
```

---

## Module Organization

### File Structure

Each module should follow this structure:

```python
"""Module docstring."""

# Imports
import os
from typing import Optional

# Constants
MAX_SIZE = 1000

# Types
class MyClass:
    pass

# Functions
def my_function() -> None:
    pass

# Main execution
if __name__ == "__main__":
    pass
```

### Import Order

1. Standard library imports
2. Third-party imports
3. Local imports

Separate each group with a blank line:

```python
import os
from typing import Optional

import numpy as np
import pygame

from core.world import World
from agents.base import Agent
```

---

## Documentation Requirements

### Module Docstrings

Every module must have a docstring:

```python
"""Core engine for Emergence simulation.

This module provides the main simulation loop and lifecycle
management for the Emergence system.
"""
```

### Class Docstrings

Every class must have a docstring:

```python
class World:
    """Manages persistent world state.
    
    The World is a two-dimensional grid of cells that persists
    indefinitely and evolves continuously.
    
    Attributes:
        width: Width of the world grid.
        height: Height of the world grid.
        generation: Current generation number.
    """
    pass
```

### Function Docstrings

Every public function must have a docstring:

```python
def compute_fitness(
    state: WorldState,
    target: BinaryPattern
) -> float:
    """Compute fitness score for world state.
    
    Calculates how well the current world state matches the
    target pattern using multiple metrics.
    
    Args:
        state: Current world state to evaluate.
        target: Target pattern to match against.
    
    Returns:
        Fitness score between 0.0 and 1.0, where 1.0
        indicates a perfect match.
    
    Raises:
        ValueError: If state and target dimensions don't match.
    """
    pass
```

### Type Hints

All public functions must have type hints:

```python
def process_input(
    data: bytes,
    format: str,
    options: Optional[dict] = None
) -> BinaryPattern:
    """Process input data into binary pattern."""
    pass
```

---

## Commenting Philosophy

### When to Comment

1. **Explain why**, not what
2. **Complex algorithms**: Explain the approach
3. **Non-obvious decisions**: Document the reasoning
4. **Workarounds**: Explain the limitation and why this approach
5. **TODOs**: Mark future work with issue references

### When NOT to Comment

1. **Obvious code**: Don't explain what the code does
2. **Redundant comments**: Don't repeat the code
3. **Outdated comments**: Remove or update them
4. **Commented-out code**: Delete it, use version control

### Comment Style

```python
# Good: Explains why
# Use view instead of copy to reduce memory allocation
# in the hot path of the simulation loop
state_view = grid.view()

# Bad: Explains what
# Get a view of the state
state_view = grid.view()
```

### TODO Format

```python
# TODO(#42): Implement caching for large worlds
# FIXME: This breaks when world size exceeds 1000
# HACK: Workaround for upstream bug in numpy
```

---

## Formatting

### Tools

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **Mypy**: Type checking

### Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
```

---

## Testing Expectations

### Test Coverage

- Minimum coverage: 80%
- New code must have tests
- Critical paths must have tests

### Test Structure

```python
import pytest
from core.world import World

class TestWorld:
    """Tests for World class."""
    
    def test_initialization(self):
        """Test world initializes correctly."""
        world = World(width=10, height=10)
        assert world.width == 10
        assert world.height == 10
    
    def test_cell_update(self):
        """Test cell state updates correctly."""
        world = World(width=10, height=10)
        world.set_cell(5, 5, state=1)
        assert world.get_cell(5, 5).state == 1
```

### Test Naming

- Test files: `test_<module>.py`
- Test classes: `Test<Class>`
- Test methods: `test_<description>`

---

## Architecture Principles

### Separation of Concerns

Each module has a single responsibility:

- `core/` - Simulation engine
- `world/` - World state
- `agents/` - Agent logic
- `rl/` - Reinforcement learning
- `evolution/` - Evolutionary algorithms
- `patterns/` - Pattern processing
- `renderer/` - Visualization
- `storage/` - Persistence
- `events/` - Communication
- `configs/` - Configuration

### Dependency Rules

1. Lower layers never depend on higher layers
2. Same-layer dependencies are discouraged
3. Cross-layer dependencies must go through interfaces
4. Configuration is global

### Interface-Based Design

Use abstract base classes for replaceable components:

```python
from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract base class for agents."""
    
    @abstractmethod
    def observe(self, world: World) -> Observation:
        """Observe world state."""
        pass
    
    @abstractmethod
    def act(self, observation: Observation) -> Action:
        """Select action based on observation."""
        pass
```

---

## Dependency Management

### Adding Dependencies

1. Check if standard library provides the functionality
2. Check if existing dependency already includes it
3. Evaluate maintenance status and community
4. Add to `requirements.txt` with version constraint
5. Document why the dependency is needed

### Version Constraints

```
# Exact version (for critical dependencies)
numpy==1.24.0

# Minimum version (for most dependencies)
pygame>=2.5.0

# Compatible version (for stable libraries)
Pillow~=10.0.0
```

### Dependency Review

- Monthly review of dependencies
- Update to latest stable versions
- Check for security vulnerabilities
- Remove unused dependencies

---

## Performance Considerations

### Hot Paths

1. Profile before optimizing
2. Use NumPy vectorization
3. Consider Numba JIT compilation
4. Avoid unnecessary allocations
5. Cache expensive computations

### Memory Management

1. Use views instead of copies when possible
2. Release resources explicitly
3. Use generators for large sequences
4. Monitor memory usage in long runs

### Parallel Processing

1. Use multiprocessing for CPU-bound work
2. Use threading for I/O-bound work
3. Avoid shared state between threads
4. Use locks when shared state is necessary

---

## Summary

These coding standards ensure:

1. **Consistency**: Code looks the same across the project
2. **Readability**: Code is easy to understand
3. **Maintainability**: Code is easy to modify
4. **Quality**: Code is tested and documented
5. **Performance**: Code is efficient

Follow these standards to maintain a professional, high-quality codebase.
