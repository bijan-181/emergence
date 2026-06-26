# Release Process

## Overview

This document describes the release process for the Emergence project. The process ensures consistent, reliable releases with proper documentation and versioning.

---

## Versioning Strategy

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

### Version Examples

```
1.0.0   - Initial release
1.0.1   - Bug fix
1.1.0   - New feature
2.0.0   - Breaking change
```

### Pre-release Versions

```
1.0.0-alpha.1   - Alpha release
1.0.0-beta.1    - Beta release
1.0.0-rc.1      - Release candidate
```

---

## Release Workflow

### 1. Preparation

```bash
# Ensure all tests pass
pytest tests/

# Run linter
ruff check .

# Run type checker
mypy .

# Update dependencies
pip-compile requirements.in
```

### 2. Version Bump

```bash
# Update version in pyproject.toml
# Update CHANGELOG.md
# Commit changes
git commit -m "chore: prepare release v1.1.0"
```

### 3. Create Release Branch

```bash
# Create release branch from main
git checkout main
git pull origin main
git checkout -b release/1.1.0

# Final testing
pytest tests/
```

### 4. Create Pull Request

```bash
# Push release branch
git push origin release/1.1.0

# Create pull request with 'release' label
```

### 5. Merge and Tag

```bash
# After review and approval
# Squash and merge to main

# Create tag
git checkout main
git pull origin main
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

### 6. Publish Release

```bash
# Build distribution
python -m build

# Upload to PyPI
twine upload dist/*

# Create GitHub release
gh release create v1.1.0 --title "v1.1.0" --notes "Release notes"
```

---

## Changelog Generation

### Format

```markdown
# Changelog

## [1.1.0] - 2024-01-15

### Added
- New feature X
- New feature Y

### Changed
- Improved performance of Z
- Updated documentation

### Fixed
- Bug in module A
- Issue with component B

### Deprecated
- Feature C (will be removed in 2.0.0)

### Removed
- Legacy module D

### Security
- Fixed vulnerability in E
```

### Automation

Use [git-cliff](https://github.com/orhun/git-cliff) for changelog generation:

```bash
# Install
cargo install git-cliff

# Generate changelog
git cliff --tag v1.1.0 -o CHANGELOG.md
```

---

## Release Checklist

### Pre-release

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in pyproject.toml
- [ ] No breaking changes (or documented)
- [ ] Dependencies reviewed and updated

### Release

- [ ] Release branch created
- [ ] Pull request created and approved
- [ ] Merged to main
- [ ] Tag created
- [ ] Distribution built
- [ ] Published to PyPI
- [ ] GitHub release created

### Post-release

- [ ] Release announcement
- [ ] Documentation deployed
- [ ] Issues closed
- [ ] Milestone updated

---

## Tagging Strategy

### Tag Format

```
vMAJOR.MINOR.PATCH
```

### Examples

```
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

### Tag Message

```
Release v1.1.0

## Changes
- Added new feature X
- Fixed bug in Y
- Improved performance of Z

## Breaking Changes
None

## Upgrade Notes
No special upgrade steps required.
```

---

## Release Automation

### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

### Automated Version Bump

```yaml
# .github/workflows/version-bump.yml
name: Version Bump

on:
  push:
    branches:
      - main

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Bump version
        uses: paulhatch/semantic-version@v5.3.0
        with:
          major_pattern: "BREAKING CHANGE"
          minor_pattern: "feat"
          patch_pattern: "fix"
```

---

## Hotfix Process

### Critical Bug

1. Create hotfix branch from latest release tag
2. Make minimal fix
3. Create pull request with `critical` label
4. Get immediate review
5. Merge to main and release branch
6. Create patch release
7. Deploy immediately

### Hotfix Branch

```bash
# Create from latest tag
git checkout v1.0.0
git checkout -b hotfix/critical-bug

# Make fix
git add src/core/engine.py
git commit -m "fix(core): critical bug fix"

# Push and create PR
git push origin hotfix/critical-bug
```

---

## Release Communication

### Pre-release

- Announce upcoming release on discussion board
- Highlight new features and breaking changes
- Provide upgrade guide if needed

### Post-release

- Publish release notes
- Update documentation
- Announce on social media (if applicable)
- Thank contributors

---

## Emergency Procedures

### Revert Release

```bash
# Revert tag
git tag -d v1.1.0
git push origin :refs/tags/v1.1.0

# Revert commit
git revert <commit-hash>
git push origin main

# Create new release
git tag -a v1.1.1 -m "Hotfix release"
git push origin v1.1.1
```

### Yank Release

```bash
# Yank from PyPI
twine upload --skip-existing dist/*
```

---

## Future Improvements

1. **Automated testing**: Run full test suite before release
2. **Canary releases**: Test with small audience before full release
3. **Rollback mechanism**: Easy rollback if issues arise
4. **Release notes generation**: Automatic from commits
5. **Dependency updates**: Automated security patches
