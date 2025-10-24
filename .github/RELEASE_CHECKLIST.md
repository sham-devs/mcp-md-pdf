# Release Checklist for mcp-md-pdf

Use this checklist every time you want to publish a new version.

## Pre-Release Steps

- [ ] All tests pass locally: `pytest tests/ -v`
- [ ] Code is formatted: `black src/ tests/`
- [ ] Linting passes: `ruff check src/ tests/`
- [ ] README.md is up to date
- [ ] CHANGELOG.md is updated (if you have one)
- [ ] Version number updated in `pyproject.toml`

## Release Steps

### 1. Update Version Number

Edit `pyproject.toml` and update the version:
\`\`\`toml
[project]
version = "0.2.0"  # Change to your new version
\`\`\`

### 2. Commit Version Bump

\`\`\`bash
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push
\`\`\`

### 3. Create Git Tag

\`\`\`bash
# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push tag to GitHub
git push origin v0.2.0
\`\`\`

### 4. Monitor GitHub Actions

1. Go to https://github.com/sham-devs/mcp-md-pdf/actions
2. Watch the "Publish to PyPI" workflow run
3. It will:
   - Build the package
   - Publish to TestPyPI first
   - Then publish to PyPI

### 5. Verify Publication

**TestPyPI:**
- URL: https://test.pypi.org/project/mcp-md-pdf/
- Test install: `pip install --index-url https://test.pypi.org/simple/ mcp-md-pdf`

**PyPI:**
- URL: https://pypi.org/project/mcp-md-pdf/
- Test install: `pip install mcp-md-pdf`

## Post-Release Steps

- [ ] Test installation: `pip install mcp-md-pdf`
- [ ] Test the package works: `mcp-md-pdf --help`
- [ ] Create GitHub Release with release notes
- [ ] Announce on social media / community (optional)

## Troubleshooting

**If publishing fails:**
1. Check GitHub Actions logs
2. Verify Trusted Publishing is configured on PyPI
3. Ensure environment names match (pypi/testpypi)
4. Check version number doesn't already exist on PyPI

**Common Issues:**
- "Package already exists" → Increment version number
- "OIDC token validation failed" → Check Trusted Publishing configuration
- "Environment not found" → Create environments in GitHub repo settings
