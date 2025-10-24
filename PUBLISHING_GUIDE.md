# Complete Publishing Guide: mcp-md-pdf

This guide contains everything you need to publish your Python package to GitHub and PyPI.

---

## ✅ What I've Done For You

I've created the following files:

1. **`.github/workflows/tests.yml`** - Runs tests on every push/PR
2. **`.github/workflows/publish.yml`** - Auto-publishes to PyPI when you create a git tag
3. **`.github/RELEASE_CHECKLIST.md`** - Step-by-step release process
4. **Updated `README.md`** - Added professional badges
5. **Updated `pyproject.toml`** - Changed name to `mcp-md-pdf` (MCP naming convention)

---

## 🎯 What You Need To Do

### Phase 1: GitHub Setup (10 minutes)

#### 1. Create GitHub Repository

Go to: https://github.com/new

- **Name:** `mcp-md-pdf`
- **Description:** "Model Context Protocol server for Markdown to Word/PDF conversion"
- **Visibility:** Public
- **DO NOT** initialize with README (we have one)

#### 2. Push Code to GitHub

Replace `sham-devs` with your actual GitHub username:

\`\`\`bash
# Initialize git (if not already done)
git init

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: mcp-md-pdf v0.1.0"

# Add GitHub remote (REPLACE sham-devs!)
git remote add origin https://github.com/sham-devs/mcp-md-pdf.git

# Push to GitHub
git branch -M main
git push -u origin main
\`\`\`

#### 3. Update README Badges

Edit `README.md` and replace `sham-devs` with your actual username in the badge URLs (lines 5-6).

---

### Phase 2: PyPI Setup (5 minutes)

#### 1. Create Accounts

**PyPI (Production):**
- Go to: https://pypi.org/account/register/
- Verify email
- (Optional) Enable 2FA for security

**TestPyPI (Testing):**
- Go to: https://test.pypi.org/account/register/
- Verify email

#### 2. Configure Trusted Publishing

This is the MODERN way (2025) - no API tokens needed!

**For TestPyPI:**
1. Visit: https://test.pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name:** `mcp-md-pdf`
   - **Owner:** `sham-devs`
   - **Repository name:** `mcp-md-pdf`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `testpypi`
4. Click "Add"

**For PyPI (Real):**
1. Visit: https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name:** `mcp-md-pdf`
   - **Owner:** `sham-devs`
   - **Repository name:** `mcp-md-pdf`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`
4. Click "Add"

---

### Phase 3: GitHub Environments (2 minutes)

Create two environments in your GitHub repository:

1. Go to: https://github.com/sham-devs/mcp-md-pdf/settings/environments
2. Click "New environment"
3. Name: `testpypi` → Click "Configure environment"
4. Click "New environment" again
5. Name: `pypi` → Click "Configure environment"

(No other settings needed - Trusted Publishing handles authentication!)

---

## 🚀 Publishing Your First Release

### Pre-Flight Check

\`\`\`bash
# Run tests
pytest tests/ -v

# Check package can be built
python -m pip install build
python -m build

# Verify package structure
python -m pip install twine
twine check dist/*
\`\`\`

### Release Process

#### 1. Update Version Number

Edit `pyproject.toml`:
\`\`\`toml
[project]
version = "0.1.0"  # Change to your desired version
\`\`\`

#### 2. Commit and Tag

\`\`\`bash
# Commit version bump
git add pyproject.toml
git commit -m "Bump version to 0.1.0"
git push

# Create and push tag (this triggers publishing!)
git tag -a v0.1.0 -m "Release v0.1.0: Initial public release"
git push origin v0.1.0
\`\`\`

#### 3. Watch It Happen!

1. Go to: https://github.com/sham-devs/mcp-md-pdf/actions
2. You'll see "Publish to PyPI" workflow running
3. It will:
   - Build your package
   - Publish to TestPyPI first
   - Then publish to PyPI

#### 4. Verify Publication

**TestPyPI:**
\`\`\`bash
# View on TestPyPI
open https://test.pypi.org/project/mcp-md-pdf/

# Test installation
pip install --index-url https://test.pypi.org/simple/ mcp-md-pdf
\`\`\`

**PyPI:**
\`\`\`bash
# View on PyPI
open https://pypi.org/project/mcp-md-pdf/

# Install from PyPI
pip install mcp-md-pdf

# Test it works
mcp-md-pdf --help
\`\`\`

---

## 📊 CI/CD Explained

### What Happens Automatically

**On Every Push/PR:**
- Tests run on Python 3.10, 3.11, 3.12
- Tests run on Windows, macOS, Linux
- Package build is validated
- Linting checks run

**On Git Tag Push (v*):**
- Package is built
- Published to TestPyPI
- Published to PyPI
- No manual intervention needed!

### Viewing Results

- **Tests:** https://github.com/sham-devs/mcp-md-pdf/actions/workflows/tests.yml
- **Releases:** https://github.com/sham-devs/mcp-md-pdf/actions/workflows/publish.yml

---

## 🔧 Future Releases

For subsequent releases, just:

1. Update version in `pyproject.toml`
2. Commit: `git commit -am "Bump version to X.Y.Z"`
3. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4. Push: `git push && git push origin vX.Y.Z`
5. GitHub Actions does the rest!

---

## 🆘 Troubleshooting

### "OIDC token validation failed"
→ Check Trusted Publishing configuration matches exactly

### "Environment not found"
→ Create `pypi` and `testpypi` environments in GitHub repo settings

### "Package already exists on PyPI"
→ Increment version number in pyproject.toml

### Tests failing in CI but pass locally
→ Check Python version compatibility
→ Review GitHub Actions logs for details

---

## 📚 Additional Resources

- **PyPI Trusted Publishing:** https://docs.pypi.org/trusted-publishers/
- **GitHub Actions:** https://docs.github.com/actions
- **Python Packaging Guide:** https://packaging.python.org/

---

## ✨ Summary

**Modern 2025 workflow:**
- ✅ No API tokens to manage
- ✅ Automated testing on 3 OSes, 3 Python versions
- ✅ One command to publish (`git push origin vX.Y.Z`)
- ✅ Secure (OIDC-based authentication)
- ✅ Free (GitHub Actions, PyPI hosting)

**You're ready to publish!** 🎉
