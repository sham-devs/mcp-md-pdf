# Quick Setup Checklist - mcp-md-pdf

## ✅ Completed

- [x] Package renamed to `mcp-md-pdf` (MCP naming convention)
- [x] GitHub remote configured: `git@github.com:sham-devs/mcp-md-pdf.git`
- [x] All files updated with `sham-devs` organization
- [x] PyPI account created
- [x] TestPyPI account created
- [x] Clean git history in main branch
- [x] Full history preserved in develop branch

---

## 📋 Current Step: Configure PyPI Trusted Publishing

### TestPyPI Configuration

**URL:** https://test.pypi.org/manage/account/publishing/

**Form Values:**
```
PyPI Project Name:  mcp-md-pdf
Owner:              sham-devs
Repository name:    mcp-md-pdf
Workflow name:      publish.yml
Environment name:   testpypi
```

### PyPI Configuration

**URL:** https://pypi.org/manage/account/publishing/

**Form Values:**
```
PyPI Project Name:  mcp-md-pdf
Owner:              sham-devs
Repository name:    mcp-md-pdf
Workflow name:      publish.yml
Environment name:   pypi
```

---

## 🔜 Next Steps (After PyPI Config)

### 1. Push to GitHub
```bash
git push -u origin main
git push -u origin develop
```

### 2. Create GitHub Environments

Go to: https://github.com/sham-devs/mcp-md-pdf/settings/environments

Create two environments:
- Name: `testpypi`
- Name: `pypi`

### 3. Create First Release

```bash
# Make sure version in pyproject.toml is 0.1.0
git tag -a v0.1.0 -m "Release v0.1.0: Initial public release"
git push origin v0.1.0
```

### 4. Watch It Publish! 🚀

GitHub Actions will automatically:
1. Build the package
2. Publish to TestPyPI
3. Publish to PyPI

Monitor at: https://github.com/sham-devs/mcp-md-pdf/actions

---

## 🆘 Quick Links

- **Repository:** https://github.com/sham-devs/mcp-md-pdf
- **TestPyPI:** https://test.pypi.org/project/mcp-md-pdf/
- **PyPI:** https://pypi.org/project/mcp-md-pdf/
- **GitHub Actions:** https://github.com/sham-devs/mcp-md-pdf/actions

---

## 📚 Detailed Guides

- **PUBLISHING_GUIDE.md** - Complete setup instructions
- **BRANCH_STRATEGY.md** - Git workflow guide
- **.github/RELEASE_CHECKLIST.md** - Release process

---

**Current Status:** ⏳ Waiting for PyPI Trusted Publishing configuration
