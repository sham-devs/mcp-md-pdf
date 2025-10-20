# Docker Image Size Comparison

This document compares different Docker base images for PDF conversion.

## TL;DR - Key Finding

**🎉 BREAKTHROUGH: Using official pandoc/latex image = 10% smaller than Debian!**

We tested 7 different approaches including official Docker images:
- ✅ **md-pdf-mcp:pandoc-official**: 1.03 GB (uses official `pandoc/latex` base) **WINNER!**
- ✅ **Debian + LibreOffice**: 1.14 GB (previous best, still good option)
- ❌ **Pandoc + Debian** (our build): 1.35 GB (+32% larger due to inefficient TeXLive install)
- ❌ **Pandoc + Alpine** (our build): 1.42 GB (+38% larger)
- ❌ **Alpine + LibreOffice**: 2.02 GB (+96% larger)
- ❌ **libreofficedocker/libreoffice-unoserver**: 2.64 GB (+156% larger!)

**Conclusion:** Official pandoc/latex image (782 MB) + Python (250 MB) = **smallest full-featured image!**

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

We built and tested **SEVEN** options including official Docker images:

| Image | Expected | Actual | vs Best | Result |
|-------|----------|--------|---------|--------|
| **md-pdf-mcp:pandoc-official** | ~1.0 GB | **1.03 GB** | baseline | ✅ **WINNER** |
| pandoc/latex (base only) | N/A | **782 MB** | N/A | Base image |
| Debian + LibreOffice | 1.14 GB | **1.14 GB** | +11% | ✅ Good alternative |
| Pandoc + Debian (our build) | 200-300 MB | **1.35 GB** | +31% | ❌ Inefficient |
| Pandoc + Alpine (our build) | 150-200 MB | **1.42 GB** | +38% | ❌ Inefficient |
| Alpine + LibreOffice | 400-600 MB | **2.02 GB** | +96% | ❌ Much larger |
| libreofficedocker/libreoffice-unoserver | Unknown | **2.64 GB** | +156% | ❌ Largest |

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

**md-pdf-mcp:pandoc-official (1.03 GB) - THE WINNER:**
- Uses official `pandoc/latex:latest` (782 MB Alpine-based image)
- Official Pandoc team optimized TeXLive installation
- Python layer adds only ~250 MB
- **10% smaller than Debian + LibreOffice**
- Best of both worlds: small base + full features

**libreofficedocker/libreoffice-unoserver (2.64 GB) - LARGEST:**
- Official LibreOffice image but not optimized for size
- Includes unoserver REST API (extra overhead)
- Based on Alpine but still massive due to full LibreOffice stack

## Recommendation

**🏆 Use Official Pandoc Image (Dockerfile.pandoc-official)** for NEW deployments:

```dockerfile
FROM pandoc/latex:latest
# ... install Python and dependencies
```

**Advantages:**
1. **Smallest image**: 1.03 GB (10% smaller than Debian!)
2. **Official Pandoc**: Maintained by Pandoc team, always up-to-date
3. **Optimized TeXLive**: Minimal LaTeX packages, expertly selected
4. **Cross-platform**: Same Pandoc behavior on all systems
5. **Well-maintained**: Updated regularly with security patches

**Build command:**
```bash
docker build -f Dockerfile.pandoc-official -t md-pdf-mcp:pandoc-official .
```

---

**Alternative: Debian + LibreOffice (Dockerfile)** for EXISTING deployments:

Keep using this if you're already deployed and it works well.

**Advantages:**
1. **Proven stability**: LibreOffice headless mode since 2003
2. **Good size**: 1.14 GB (only 11% larger than Pandoc)
3. **Wide compatibility**: Handles complex Word documents
4. **Familiar**: Most DevOps teams know LibreOffice

**Build command:**
```bash
docker build -t md-pdf-mcp .
```

---

**Why NOT use other alternatives?**

- ❌ **Our Pandoc builds** (Debian/Alpine): 31-38% larger due to inefficient TeXLive install
- ❌ **Alpine + LibreOffice**: 96% larger (2.02 GB) - Alpine doesn't help for LibreOffice
- ❌ **libreofficedocker/libreoffice-unoserver**: 156% larger (2.64 GB) - includes unnecessary REST API

---

## Build Commands

```bash
# RECOMMENDED: Official Pandoc (1.03 GB - SMALLEST!)
docker build -f Dockerfile.pandoc-official -t md-pdf-mcp:pandoc-official .

# Alternative: Debian + LibreOffice (1.14 GB)
docker build -t md-pdf-mcp .

# NOT RECOMMENDED: Our inefficient builds

# Pandoc + Debian (1.35 GB - our build, inefficient TeXLive)
docker build -f Dockerfile.pandoc -t md-pdf-mcp:pandoc .

# Pandoc + Alpine (1.42 GB - our build, still inefficient)
docker build -f Dockerfile.pandoc-alpine -t md-pdf-mcp:pandoc-alpine .

# Alpine + LibreOffice (2.02 GB - LARGE!)
docker build -f Dockerfile.alpine -t md-pdf-mcp:alpine .

# Compare all sizes (sorted by size)
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(pandoc|libreoffice|md-pdf-mcp)" | sort -k3 -h
```

**Output:**
```
REPOSITORY                                TAG             SIZE
pandoc/core                               latest          319MB   (base image, no Python)
pandoc/latex                              latest          782MB   (base image, no Python)
md-pdf-mcp                                pandoc-official 1.03GB  ✅ WINNER (smallest full-featured)
md-pdf-mcp                                latest          1.14GB  ✅ Good alternative
md-pdf-mcp                                pandoc          1.35GB  ❌ Inefficient (our build)
md-pdf-mcp                                pandoc-alpine   1.42GB  ❌ Inefficient (our build)
md-pdf-mcp                                alpine          2.02GB  ❌ Large
libreofficedocker/libreoffice-unoserver   edge            2.64GB  ❌ Largest
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
