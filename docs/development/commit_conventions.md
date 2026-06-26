# Commit Conventions

## Overview

This document defines the commit message conventions for the Emergence project. We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

---

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Rules

1. **Subject line**: Maximum 72 characters
2. **Type**: Required, lowercase
3. **Scope**: Optional, in parentheses
4. **Description**: Imperative mood, lowercase, no period
5. **Body**: Optional, wrap at 72 characters
6. **Footer**: Optional, for breaking changes or issue references

---

## Types

### `feat`

A new feature

```bash
git commit -m "feat(core): add cell state management"
git commit -m "feat(renderer): implement pygame visualization"
git commit -m "feat(agents): add reactive agent type"
```

### `fix`

A bug fix

```bash
git commit -m "fix(core): correct neighbor counting in Moore neighborhood"
git commit -m "fix(engine): prevent race condition in state updates"
```

### `docs`

Documentation only changes

```bash
git commit -m "docs: add architecture documentation"
git commit -m "docs(core): update API reference"
git commit -m "docs: fix typo in README"
```

### `refactor`

Code change that neither fixes a bug nor adds a feature

```bash
git commit -m "refactor(core): simplify world update pipeline"
git commit -m "refactor(agents): extract perception into separate module"
```

### `test`

Adding missing tests or correcting existing tests

```bash
git commit -m "test(core): add engine unit tests"
git commit -m "test(agents): add integration tests for agent-world interaction"
```

### `chore`

Other changes that don't modify src or test files

```bash
git commit -m "chore: update dependencies"
git commit -m "chore: improve .gitignore"
git commit -m "chore: add pre-commit hooks"
```

### `perf`

A code change that improves performance

```bash
git commit -m "perf(core): vectorize cell update with NumPy"
git commit -m "perf(renderer): optimize rendering pipeline"
```

### `build`

Changes that affect the build system or external dependencies

```bash
git commit -m "build: add CMake configuration"
git commit -m "build: update Python version requirement"
```

### `ci`

Changes to CI configuration files and scripts

```bash
git commit -m "ci: add GitHub Actions workflow"
git commit -m "ci: update test matrix"
```

---

## Scope

Scope is optional and should be the name of the module affected:

- `core` - Core engine
- `world` - World state management
- `agents` - Agent system
- `rl` - Reinforcement learning
- `evolution` - Evolutionary algorithms
- `patterns` - Pattern generation
- `renderer` - Visualization
- `storage` - Persistence layer
- `events` - Event system
- `configs` - Configuration

---

## Examples

### Simple Feature

```
feat(core): add cell age tracking
```

### Feature with Body

```
feat(agents): implement learning agent

Add reinforcement learning agent that can improve its policy
through experience. Uses Q-learning with experience replay.

Closes #42
```

### Breaking Change

```
feat(world)!: change cell state representation

BREAKING CHANGE: Cell state is now stored as uint8 instead of
boolean. All existing snapshots must be migrated.
```

### Multiple Changes

```
refactor(core): simplify state management

- Remove redundant state copies
- Use view-based access patterns
- Reduce memory allocation in hot path
```

---

## Multiple Commits vs One Large Commit

### When to Use Multiple Commits

1. **Logical separation**: Different concerns in one change
2. **Reviewable chunks**: Each commit is self-contained
3. **Reversible units**: Each commit can be reverted independently
4. **Bisectable**: Each commit maintains working state

### When to Use One Commit

1. **Atomic change**: All changes are tightly coupled
2. **Small change**: Total change is less than 50 lines
3. **Single concern**: All changes address the same issue

### Examples

**Good: Multiple commits**
```
feat(core): add cell state type
feat(core): implement state transitions
test(core): add state transition tests
```

**Bad: One large commit**
```
feat(core): add cell state type and implement transitions and add tests
```

**Good: One commit**
```
fix(core): correct off-by-one error in neighbor count
```

**Bad: Multiple commits for a small fix**
```
fix(core): change 5 to 4
test(core): add test for neighbor count
```

---

## Commit Message Validation

### Pre-commit Hook

The project uses pre-commit hooks to validate commit messages:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Validation Rules

1. Type must be one of: feat, fix, docs, refactor, test, chore, perf, build, ci
2. Subject line must be lowercase
3. Subject line must not end with period
4. Subject line must be under 72 characters
5. Body lines must be under 72 characters

---

## Tips

1. **Write in imperative mood**: "add feature" not "added feature"
2. **Keep it concise**: Subject line under 72 characters
3. **Be specific**: "fix memory leak" not "fix bug"
4. **Reference issues**: Use "Closes #123" or "Fixes #123"
5. **Explain why, not what**: The code shows what changed, commit message explains why
