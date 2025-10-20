# Docker Image Size Comparison

This document compares different Docker base images for PDF conversion.

## TL;DR - Key Finding

**The original Debian + LibreOffice (1.14 GB) is the SMALLEST and BEST option.**

We tested 4 different approaches expecting Alpine or Pandoc to be smaller:
- ✅ **Debian + LibreOffice**: 1.14 GB (baseline, **WINNER**)
- ❌ **Pandoc + Debian**: 1.35 GB (+18% larger due to 753 MB TeXLive packages)
- ❌ **Pandoc + Alpine**: 1.42 GB (+25% larger, Alpine provides NO advantage)
- ❌ **Alpine + LibreOffice**: 2.02 GB (+77% larger due to bundled dependencies)

**Conclusion:** Debian has the most optimized LibreOffice packaging. Stick with the default `Dockerfile`.

---

## Options Tested

### Option 1: Debian (python:3.11-slim)
**Current Dockerfile**

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    --no-install-recommends
```

**Size**: ~1.14 GB

**Pros:**
- Full LibreOffice suite
- Well-tested and stable
- Comprehensive font support

**Cons:**
- Very large image size
- Includes many unused components

---

### Option 2: Alpine (python:3.11-alpine)
**Dockerfile.alpine**

```dockerfile
FROM python:3.11-alpine
RUN apk add --no-cache \
    libreoffice \
    openjdk11-jre-headless \
    ttf-dejavu
```

**Expected Size**: ~400-600 MB (60-70% smaller!)

**Pros:**
- Much smaller base image
- Faster download and deployment
- Minimal attack surface

**Cons:**
- May have compatibility issues with some DOCX features
- Limited font selection (can be expanded)

---

### Option 3: Pandoc (Direct Markdown → PDF)
**Alternative approach: Skip DOCX step**

```dockerfile
FROM pandoc/core:latest
# Size: ~100-200 MB
```

**Pros:**
- Smallest possible image
- Direct Markdown → PDF conversion
- No LibreOffice needed

**Cons:**
- **Cannot use .dotx templates** (dealbreaker!)
- Different styling approach
- Requires complete rewrite of converter.py

---

### Option 4: Python-only (docx2pdf, pypandoc)

All Python libraries for DOCX→PDF conversion require external dependencies:
- `docx2pdf`: Requires LibreOffice or MS Word
- `pypandoc`: Requires Pandoc installation
- `aspose-words`: Commercial/paid ($1000+ license)

**None of these reduce Docker image size.**

---

## Actual Test Results

We built and tested **FOUR** options to find the optimal Docker image size:

| Image | Expected Size | Actual Size | vs Debian | Result |
|-------|--------------|-------------|-----------|--------|
| **Debian + LibreOffice** | 1.14 GB | **1.14 GB** | baseline | ✅ WINNER |
| Pandoc + Debian | 200-300 MB | **1.35 GB** | +18% | ❌ Larger |
| Pandoc + Alpine | 150-200 MB | **1.42 GB** | +25% | ❌ Larger |
| Alpine + LibreOffice | 400-600 MB | **2.02 GB** | +77% | ❌ Much larger |

### Why the Surprises?

**Alpine + LibreOffice (2.02 GB):**
- Alpine packages LibreOffice with ALL dependencies bundled
- Includes full OpenJDK 11 JRE (Java runtime)
- Bundles fonts that Debian links from system packages
- LibreOffice layer alone: **1.27 GB**

**Pandoc + Debian + TeXLive (1.35 GB):**
- Pandoc requires full LaTeX distribution for quality PDFs
- texlive-latex-extra alone is massive (thousands of packages)
- Total TeXLive packages on Debian: **753 MB**
- Defeats the "lightweight" purpose

**Pandoc + Alpine + TeXLive (1.42 GB):**
- Alpine's TeXLive packages are similar in size to Debian's
- Alpine base is smaller (~50 MB vs ~200 MB)
- But texlive, texlive-luatex packages are still massive (666 MB)
- Result: Alpine provides NO size advantage for Pandoc

**Debian + LibreOffice (1.14 GB):**
- Most optimized LibreOffice packaging
- Shared system dependencies (fonts, Java)
- LibreOffice uses system libraries efficiently

## Recommendation

**Use Debian + LibreOffice (Dockerfile)** for ALL deployments:

1. **Smallest image**: 1.14 GB (smallest of all tested options!)
2. **Most tested**: Proven LibreOffice packaging since 2003
3. **Best compatibility**: Full font and document support
4. **Fastest builds**: Debian APT cache is optimized
5. **Most reliable**: LibreOffice headless mode is industry standard

**Why NOT use alternatives?**

- **Alpine + LibreOffice**: 77% larger (2.02 GB) due to bundled dependencies
- **Pandoc + Debian**: 18% larger (1.35 GB) due to massive TeXLive packages
- **Pandoc + Alpine**: 25% larger (1.42 GB) - Alpine provides no advantage for Pandoc

**Pandoc Alternative (Already Available):**
- Pandoc support is already implemented in `converter.py`
- Automatically uses Pandoc if available (priority over LibreOffice)
- Cross-platform benefit: Works same on Windows/macOS/Linux
- **For local development**: Install Pandoc separately if desired
- **For Docker**: Stick with LibreOffice (smaller and more reliable)

---

## Build Commands

```bash
# Recommended: Debian + LibreOffice (1.14 GB)
docker build -t md-pdf-mcp .

# Test alternatives (not recommended due to size):

# Alpine + LibreOffice (2.02 GB - LARGEST)
docker build -f Dockerfile.alpine -t md-pdf-mcp:alpine .

# Pandoc + Debian (1.35 GB)
docker build -f Dockerfile.pandoc -t md-pdf-mcp:pandoc .

# Pandoc + Alpine (1.42 GB)
docker build -f Dockerfile.pandoc-alpine -t md-pdf-mcp:pandoc-alpine .

# Compare sizes (sorted by size)
docker images md-pdf-mcp --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -k3 -h
```

**Output:**
```
REPOSITORY   TAG             SIZE
md-pdf-mcp   latest          1.14GB  ✅ WINNER
md-pdf-mcp   pandoc          1.35GB
md-pdf-mcp   pandoc-alpine   1.42GB
md-pdf-mcp   alpine          2.02GB  ❌ LARGEST
```

---

## Testing Checklist

Before switching to Alpine in production, test:

- [ ] DOCX creation with headings (H1-H6)
- [ ] .dotx template application
- [ ] PDF conversion with LibreOffice
- [ ] Unicode and emoji support
- [ ] Table rendering
- [ ] Code blocks and formatting
- [ ] Complex nested lists

If Alpine fails any tests, fall back to Debian.
