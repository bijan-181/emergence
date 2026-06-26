# Git Workflow

## Overview

This document describes the Git workflow for the Emergence project. The workflow is designed for a small research team working on a long-term project.

---

## Repository Access

- **Repository**: `github.com/bijan-181/emergence`
- **Primary branch**: `main`
- **Access**: Write access for maintainers, pull requests for contributors

---

## Daily Development Workflow

### 1. Start of Day

```bash
# Pull latest changes
git pull origin main

# Create or switch to feature branch
git checkout -b feature/my-feature
```

### 2. During Development

```bash
# Stage specific files
git add path/to/file.py

# Commit with conventional commit message
git commit -m "feat(core): add cell state management"

# Push to remote
git push origin feature/my-feature
```

### 3. End of Day

```bash
# Push all commits
git push origin feature/my-feature

# If done, create pull request
```

---

## Pull Request Process

### Creating a Pull Request

1. Ensure all tests pass
2. Update documentation if needed
3. Push branch to remote
4. Create pull request with:
   - Clear title using conventional commit format
   - Description of changes
   - Reference to issue if applicable
   - Screenshots for visual changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Test addition

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added for new functionality
```

---

## Review Process

### For Authors

1. Self-review all changes
2. Ensure tests pass locally
3. Write clear commit messages
4. Keep pull requests focused

### For Reviewers

1. Review code quality
2. Check test coverage
3. Verify documentation
4. Test locally if needed
5. Approve or request changes

---

## Merge Strategy

### Main Branch

- **Strategy**: Squash and merge
- **Reason**: Keeps main branch history clean
- **Commit message**: Use PR title (conventional commit format)

### Feature Branches

- **Strategy**: Regular merge
- **Reason**: Preserves development history
- **When**: Merging main into feature branches

---

## Branch Naming

| Pattern | Example | Description |
|---------|---------|-------------|
| `feature/*` | `feature/cell-state` | New features |
| `fix/*` | `fix/neighbor-count` | Bug fixes |
| `docs/*` | `docs/architecture` | Documentation |
| `refactor/*` | `refactor/rule-engine` | Code refactoring |
| `test/*` | `test/engine-unit` | Test additions |
| `chore/*` | `chore/dependencies` | Maintenance |

---

## Repository Maintenance

### Weekly

- Review open pull requests
- Close stale branches
- Update dependencies

### Monthly

- Review branch protection rules
- Audit access permissions
- Clean up old releases

### Quarterly

- Review workflow efficiency
- Update documentation
- Assess tooling needs

---

## Commit Message Format

See [commit_conventions.md](commit_conventions.md) for detailed commit message format.

---

## Emergency Procedures

### Hotfix

1. Create `fix/urgent-fix` branch from `main`
2. Make minimal changes
3. Create pull request with `urgent` label
4. Get immediate review
5. Merge and deploy

### Revert

1. Create new commit reverting changes
2. Do not rewrite history
3. Document reason for revert
4. Create pull request
