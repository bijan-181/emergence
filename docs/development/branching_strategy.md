# Branching Strategy

## Overview

This document describes the branching strategy for the Emergence project. The strategy is designed for a small research team working on a long-term project.

---

## Branch Types

### Main Branch

**Branch**: `main`

**Purpose**: The primary branch containing stable, production-ready code.

**Rules**:
- Never commit directly to `main`
- All changes go through pull requests
- All tests must pass before merge
- Squash and merge for clean history
- Always deployable

**Protection Rules**:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict force pushes

---

### Feature Branches

**Pattern**: `feature/*`

**Purpose**: Development of new features.

**Examples**:
- `feature/cell-state`
- `feature/agent-perception`
- `feature/rule-engine`

**Lifecycle**:
1. Create from `main`
2. Develop with regular commits
3. Create pull request when ready
4. Merge to `main` via squash and merge
5. Delete branch after merge

---

### Fix Branches

**Pattern**: `fix/*`

**Purpose**: Bug fixes.

**Examples**:
- `fix/neighbor-count`
- `fix/state-corruption`
- `fix/memory-leak`

**Lifecycle**:
1. Create from `main`
2. Make minimal changes
3. Create pull request with `urgent` label if critical
4. Merge to `main` via squash and merge
5. Delete branch after merge

---

### Documentation Branches

**Pattern**: `docs/*`

**Purpose**: Documentation changes.

**Examples**:
- `docs/architecture`
- `docs/api-reference`
- `docs/README`

**Lifecycle**:
1. Create from `main`
2. Update documentation
3. Create pull request
4. Merge to `main` via squash and merge
5. Delete branch after merge

---

### Refactor Branches

**Pattern**: `refactor/*`

**Purpose**: Code refactoring without behavior changes.

**Examples**:
- `refactor/rule-engine`
- `refactor/agent-system`
- `refactor/state-management`

**Lifecycle**:
1. Create from `main`
2. Refactor code
3. Ensure all tests pass
4. Create pull request
5. Merge to `main` via squash and merge
6. Delete branch after merge

---

### Test Branches

**Pattern**: `test/*`

**Purpose**: Adding or improving tests.

**Examples**:
- `test/engine-unit`
- `test/agent-integration`
- `test/performance`

**Lifecycle**:
1. Create from `main`
2. Add or improve tests
3. Create pull request
4. Merge to `main` via squash and merge
5. Delete branch after merge

---

### Experimental Branches

**Pattern**: `experimental/*`

**Purpose**: Research experiments and prototypes.

**Examples**:
- `experimental/new-algorithm`
- `experimental/performance-test`
- `experimental/alternative-approach`

**Lifecycle**:
1. Create from `main`
2. Experiment freely
3. May or may not create pull request
4. Merge if successful, delete if not
5. Document findings regardless

---

### Release Branches

**Pattern**: `release/*`

**Purpose**: Prepare releases (future use).

**Examples**:
- `release/1.0.0`
- `release/1.1.0`

**Lifecycle**:
1. Create from `main` when ready to release
2. Final testing and documentation
3. Create tag when ready
4. Merge to `main`
5. Delete branch after release

---

### Hotfix Branches

**Pattern**: `hotfix/*`

**Purpose**: Critical fixes for production (future use).

**Examples**:
- `hotfix/security-patch`
- `hotfix/critical-bug`

**Lifecycle**:
1. Create from latest release tag
2. Make minimal changes
3. Create pull request with `critical` label
4. Merge to `main` and release branch
5. Delete branch after merge

---

## Branch Naming Conventions

### Format

```
<type>/<short-description>
```

### Rules

1. **Lowercase**: All branch names are lowercase
2. **Hyphens**: Use hyphens to separate words
3. **Descriptive**: Name should describe the change
4. **Concise**: Keep under 50 characters
5. **No special characters**: Only letters, numbers, hyphens

### Examples

```bash
# Good
feature/cell-state
fix/neighbor-count
docs/architecture
refactor/rule-engine

# Bad
feature/CellState
fix neighbor count
docs/architecture_v2
refactor_rule_engine
```

---

## Merge Policies

### Main Branch

**Strategy**: Squash and merge

**Why**:
- Keeps main branch history clean
- Each commit on main represents a complete feature/fix
- Easy to revert entire features
- Clean bisectable history

**Process**:
1. Create pull request
2. Get review approval
3. Ensure all tests pass
4. Squash and merge
5. Delete feature branch

### Feature Branches

**Strategy**: Regular merge

**Why**:
- Preserves development history
- Allows multiple commits per feature
- Enables work-in-progress commits
- Maintains context of changes

**Process**:
1. Pull latest from main
2. Merge main into feature branch
3. Resolve conflicts if any
4. Continue development

---

## Branch Protection Rules

### Main Branch

```yaml
# GitHub branch protection rules
required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true
  require_code_owner_reviews: false

required_status_checks:
  strict: true
  contexts:
    - tests
    - lint

restrictions:
  users: []
  teams: []

enforce_admins: false
allow_force_pushes: false
allow_deletions: false
```

### Feature Branches

No protection rules (temporary branches).

---

## Workflow Example

### Starting a New Feature

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/cell-state

# 3. Develop feature
git add src/core/cell.py
git commit -m "feat(core): add cell state type"

git add src/core/world.py
git commit -m "feat(core): integrate cell state"

# 4. Push to remote
git push origin feature/cell-state

# 5. Create pull request on GitHub
```

### Handling Review Feedback

```bash
# 1. Make requested changes
git add src/core/cell.py
git commit -m "fix(core): address review feedback"

# 2. Push changes
git push origin feature/cell-state

# 3. Pull request updates automatically
```

### Merging to Main

```bash
# 1. Squash and merge via GitHub UI
# 2. Delete feature branch via GitHub UI
# 3. Pull latest main
git checkout main
git pull origin main
```

---

## Emergency Procedures

### Critical Bug Fix

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Make minimal fix
git add src/core/engine.py
git commit -m "fix(core): critical bug fix"

# 3. Push and create PR with 'critical' label
git push origin hotfix/critical-bug

# 4. Get immediate review and merge
```

### Reverting a Change

```bash
# 1. Create revert commit
git checkout main
git pull origin main
git revert <commit-hash>

# 2. Push and create PR
git push origin main
```

---

## Best Practices

1. **Keep branches short-lived**: Merge within a few days
2. **Regular pulls**: Pull main daily to avoid conflicts
3. **Small commits**: Make commits frequently
4. **Clear naming**: Branch name should describe the change
5. **Clean up**: Delete branches after merge
6. **Document**: Update documentation with changes
7. **Test**: Ensure tests pass before creating PR
8. **Review**: Get review before merging to main
