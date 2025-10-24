# Git Branch Strategy for mcp-md-pdf

## 🌳 Current Branch Structure

### ✅ **main** (Clean, Production-Ready)
- **Purpose:** Clean history with single initial commit
- **Status:** Ready for GitHub and PyPI publishing
- **Commits:** 1 commit
- **Use for:** Production releases, PyPI publishing

```bash
# Current commit
1393027 Initial release: mcp-md-pdf v0.1.0
```

### 🚧 **develop** (Active Development)
- **Purpose:** Ongoing development work with full commit history
- **Status:** All recent work including publishing setup
- **Commits:** 15+ commits (full history)
- **Use for:** New features, bug fixes, experiments

```bash
# Latest commits
ac74dbc Prepare for PyPI publishing
4a35daf Clean up remaining Docker references
e8a3b2a Remove Docker support
8fe6055 Enhance Claude Desktop integration
...
```

### 📦 **master-old** (Backup)
- **Purpose:** Original master branch (backup copy)
- **Status:** Identical to develop
- **Use for:** Reference only, can be deleted after first successful publish

---

## 🎯 Recommended Workflow

### For Publishing to GitHub/PyPI (First Time)

**Push clean main branch:**
```bash
# Switch to main
git checkout main

# Push to GitHub as main branch
git push -u origin main
```

### For Ongoing Development

**Use develop branch:**
```bash
# Switch to develop
git checkout develop

# Create feature branches from develop
git checkout -b feature/new-feature

# Work on your feature
git add .
git commit -m "Add new feature"

# Merge back to develop
git checkout develop
git merge feature/new-feature
```

### For New Releases

**Option 1: Merge develop into main (keeps history clean)**
```bash
# Switch to main
git checkout main

# Squash merge from develop (creates 1 commit)
git merge --squash develop
git commit -m "Release v0.2.0: Description of changes"

# Tag the release
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin main --tags
```

**Option 2: Cherry-pick specific commits**
```bash
# Switch to main
git checkout main

# Cherry-pick specific commits from develop
git cherry-pick <commit-hash>
git push origin main
```

---

## 🔄 Suggested Git Workflow Going Forward

### 1. Daily Development
```bash
# Always work in develop
git checkout develop

# Make changes
git add .
git commit -m "Your commit message"
git push origin develop
```

### 2. When Ready to Release
```bash
# Update version in pyproject.toml
# Commit version bump
git add pyproject.toml
git commit -m "Bump version to 0.2.0"

# Merge to main (squash for clean history)
git checkout main
git merge --squash develop
git commit -m "Release v0.2.0: List of major changes"

# Tag and push
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin main --tags
```

### 3. GitHub Actions Will
- Run tests on develop branch (on every push)
- Publish to PyPI when you push tags to main

---

## 📊 Branch Comparison

| Branch | Commits | Purpose | Push to GitHub? |
|--------|---------|---------|----------------|
| **main** | 1 (clean) | Production releases | ✅ Yes (first!) |
| **develop** | 15+ | Active development | ✅ Yes |
| **master-old** | 15+ | Backup | ❌ No (delete later) |

---

## 🚀 Next Steps

1. **Push main to GitHub:**
   ```bash
   git checkout main
   git push -u origin main
   ```

2. **Push develop to GitHub:**
   ```bash
   git checkout develop
   git push -u origin develop
   ```

3. **Set main as default branch on GitHub:**
   - Go to: https://github.com/sham-devs/mcp-md-pdf/settings
   - Under "Default branch", select `main`

4. **Optional: Delete master-old after confirming everything works:**
   ```bash
   git branch -d master-old
   ```

---

## ✨ Benefits of This Approach

- ✅ Clean production history in main (easy to review)
- ✅ Full development history in develop (for debugging)
- ✅ Professional Git workflow (industry standard)
- ✅ Easy to see what went into each release
- ✅ Backup of original work preserved

---

## 🆘 Quick Reference

**Where am I?**
```bash
git branch  # Shows all branches, * indicates current
```

**Switch branches:**
```bash
git checkout main     # Go to main
git checkout develop  # Go to develop
```

**See branch history:**
```bash
git log --oneline --graph --all  # Visual graph of all branches
```

**Check differences:**
```bash
git diff main develop  # See what's different between branches
```

---

**Current Status:** ✅ Ready to push to GitHub!
