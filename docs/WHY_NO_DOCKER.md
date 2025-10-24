# Why MD-PDF-MCP Doesn't Support Docker

This document explains our journey with Docker and why we ultimately decided that **native deployment is the only viable approach** for MD-PDF-MCP.

---

## TL;DR - The Conclusion

**Docker is architecturally incompatible with MD-PDF-MCP's use case.**

- ✅ **Native deployment works perfectly**: Direct filesystem access, simple setup, fast execution
- ❌ **Docker deployment fails fundamentally**: Requires complex volume configuration, path translation, and defeats the tool's purpose

**For developers:** Continue using native Python installation (`pip install mcp-md-pdf` or `uvx mcp-md-pdf`)
**For CI/CD:** Docker can still be used for testing in isolated environments

---

## Table of Contents

1. [The Problem: Filesystem Access Patterns](#the-problem-filesystem-access-patterns)
2. [Our Docker Journey](#our-docker-journey)
3. [Research: How Real MCP Servers Handle Docker](#research-how-real-mcp-servers-handle-docker)
4. [Why the Workspace-Centric Pattern Doesn't Work for Us](#why-the-workspace-centric-pattern-doesnt-work-for-us)
5. [What About Mounting the Entire Filesystem?](#what-about-mounting-the-entire-filesystem)
6. [Image Size Experiments](#image-size-experiments)
7. [The Formatting Problem](#the-formatting-problem)
8. [Final Decision](#final-decision)

---

## The Problem: Filesystem Access Patterns

### What MD-PDF-MCP Does

MD-PDF-MCP converts Markdown files to Word/PDF documents:

```python
# server.py:36-39
def _convert_markdown_impl(markdown_path: str, output_path: str, ...):
    if not os.path.exists(markdown_path):
        return f"❌ Error: Markdown file not found: {markdown_path}"

    if template_path and not os.path.exists(template_path):
        return f"❌ Error: Template file not found: {template_path}"
```

**Key Insight**: The server accepts **arbitrary absolute file paths** from the client (Claude Desktop).

### The Docker Conflict

When Claude Desktop calls the MCP tool:

```
User: "Claude, convert C:\Users\basel\Desktop\meeting-notes.md to PDF"
```

Claude Desktop sends the host path `C:\Users\basel\Desktop\meeting-notes.md` to the Docker container.

**The Problem**: The Docker container can't see `C:\Users\basel\Desktop\` unless it's explicitly mounted in the configuration.

---

## Our Docker Journey

### Phase 1: Initial Docker Implementation

We started with a straightforward Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install LibreOffice for PDF conversion
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "md_pdf_mcp.server"]
```

**Claude Desktop Configuration**:
```json
{
  "mcpServers": {
    "mcp-md-pdf": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "C:\\Users\\YOUR_USERNAME\\Documents:/workspace",
        "mcp-md-pdf"
      ]
    }
  }
}
```

**Problems Encountered**:
1. Files outside `/workspace/` couldn't be accessed
2. Users had to manually configure volume mounts for every folder they might use
3. Path translation wasn't happening (container received host paths)
4. Template files in different locations required additional mounts

---

### Phase 2: Image Size Optimization

We experimented with multiple approaches to reduce image size:

| Approach | Size | Result |
|----------|------|--------|
| Debian + LibreOffice (original) | 1.14 GB | ✅ Works, reasonable size |
| Alpine + LibreOffice | 2.02 GB | ❌ Larger! Alpine doesn't help with LibreOffice |
| Pandoc + Debian (our build) | 1.35 GB | ❌ Larger + formatting issues |
| Pandoc + Alpine (our build) | 1.42 GB | ❌ Larger + formatting issues |
| Official pandoc/latex | 1.03 GB | ✅ Smallest, but formatting issues |
| libreofficedocker/libreoffice-unoserver | 2.64 GB | ❌ Largest |

**Key Findings**:
- Alpine doesn't reduce size for LibreOffice-based images (Java dependencies are heavy)
- Official pandoc/latex is smallest but has critical formatting issues (see below)
- Size optimization doesn't solve the filesystem access problem

---

### Phase 3: The Ephemeral Pattern

We adopted Docker's recommended "ephemeral pattern" for MCP servers:

```json
{
  "mcpServers": {
    "mcp-md-pdf": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "/local:/workspace", "mcp-md-pdf"]
    }
  }
}
```

**How It Works**:
1. Claude Desktop spawns a fresh container for each tool call
2. Container processes the request
3. Container automatically destroys itself (`--rm` flag)

**Advantages**:
- ✅ Secure (no persistent containers)
- ✅ Clean (no leftover containers)
- ✅ Follows MCP best practices

**Still Doesn't Solve**:
- ❌ Filesystem access problem persists
- ❌ Users still need pre-configured volume mounts
- ❌ Can't access files outside mounted directories

---

## Research: How Real MCP Servers Handle Docker

We researched real-world MCP filesystem servers to find solutions. **Every single one uses a workspace-centric design.**

### 1. Official Anthropic MCP Filesystem Server

**From `modelcontextprotocol/servers` (official reference implementation)**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--mount", "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
        "--mount", "type=bind,src=/path/to/allowed/dir,dst=/projects/other,ro",
        "mcp/filesystem",
        "/projects"
      ]
    }
  }
}
```

**Key Points**:
- Users **pre-configure explicit volume mounts** for EACH directory
- Files are accessed via **container paths** (`/projects/Desktop/file.md`)
- Server only sees `/projects/` directory
- Workspace-centric by design

---

### 2. mark3labs/mcp-filesystem-server

```json
{
  "filesystem": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm",
      "--volume=/allowed/directory/in/host:/allowed/directory/in/container",
      "ghcr.io/mark3labs/mcp-filesystem-server:latest",
      "/allowed/directory/in/container"
    ]
  }
}
```

**Pattern**: Same workspace-centric design. No arbitrary path access.

---

### 3. bsmi021/mcp-file-operations-server

```bash
docker run -it --rm -v "$(pwd):/workspace" ghcr.io/bsmi021/mcp-file-operations-server
```

**Constraint**: Works only within `/workspace` directory.

---

### 4. Docker Hub Official `mcp/filesystem`

```json
{
  "filesystem": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm",
      "-v", "/local-directory:/local-directory",
      "mcp/filesystem",
      "/local-directory"
    ]
  }
}
```

**Conclusion**: Even Docker's official MCP catalog uses explicit mounts.

---

## Why the Workspace-Centric Pattern Doesn't Work for Us

### Filesystem MCP Servers vs. Document Conversion Tools

| Aspect | **Filesystem MCP Servers** | **MD-PDF-MCP** |
|--------|---------------------------|----------------|
| **Use Case** | Browse/explore workspace files | Convert specific documents |
| **User Intent** | "Work with my project directory" | "Convert this file on my Desktop" |
| **Path Pattern** | Workspace-centric (fixed mount points) | File-specific (arbitrary locations) |
| **User Experience** | Configure once, use many times | Ad-hoc conversions anywhere |
| **Typical Files** | Code repositories, project files | Random documents, notes, reports |

### Real-World Example

**Filesystem Server (Works Fine)**:
```
User: "Claude, read all files in my project and summarize"
→ Project is in /Users/basel/workspace (already mounted as /workspace/)
→ Container accesses /workspace/file.md
→ ✅ Works!
```

**MD-PDF-MCP (Breaks)**:
```
User: "Claude, convert C:\Users\basel\Desktop\meeting-notes.md to PDF"
→ Desktop is NOT in mounted volume
→ Container can't access C:\Users\basel\Desktop\
→ ❌ File not found!

User: "Convert my Downloads/report.md with template from Documents/template.dotx"
→ Requires TWO volume mounts (Downloads + Documents)
→ User must pre-configure both in claude_desktop_config.json
→ ❌ Too complex!
```

---

## What About Mounting the Entire Filesystem?

**Theoretical Solution**:
```json
{
  "mcp-md-pdf": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm",
      "-v", "C:\\Users:/Users",
      "-v", "C:\\Documents:/Documents",
      "mcp-md-pdf"
    ]
  }
}
```

### Why This Fails

#### 1. **Security Risk**
Container sees ALL user files:
- Passwords
- SSH keys
- Browser data
- Personal documents
- Company confidential files

#### 2. **Path Translation Complexity**
Still need code to translate:
- Windows: `C:\Users\basel\file.md` → `/Users/basel/file.md`
- macOS: `/Users/basel/file.md` → `/Users/basel/file.md`
- Linux: `/home/basel/file.md` → ???

Different OS conventions require platform-specific logic.

#### 3. **User Configuration Burden**
Users must:
- Manually set up multiple volume mounts
- Understand Docker volume syntax
- Debug mount point issues
- Restart Claude Desktop after changes

#### 4. **Defeats Docker's Purpose**
If we mount everything, why use Docker?
- No isolation benefits
- No security advantages
- Added complexity
- Slower execution

#### 5. **Simpler Native Alternative**
```bash
# Native installation
pip install mcp-md-pdf

# Done! Works with ANY file path immediately.
```

---

## Image Size Experiments

### Test Results

We built and tested **SEVEN** approaches:

| Image | Size | Result |
|-------|------|--------|
| **mcp-md-pdf:pandoc-official** | **1.03 GB** | ✅ Smallest (but formatting issues) |
| pandoc/latex (base only) | **782 MB** | Base image |
| Debian + LibreOffice | **1.14 GB** | ✅ Best option (preserves formatting) |
| Pandoc + Debian (our build) | **1.35 GB** | ❌ Inefficient TeXLive install |
| Pandoc + Alpine (our build) | **1.42 GB** | ❌ No size advantage |
| Alpine + LibreOffice | **2.02 GB** | ❌ 96% larger! |
| libreofficedocker/libreoffice-unoserver | **2.64 GB** | ❌ 156% larger! |

### Why the Surprises?

#### Alpine + LibreOffice (2.02 GB - Larger!)

Alpine packages LibreOffice with ALL dependencies bundled:
- Full OpenJDK 11 JRE (Java runtime)
- All fonts bundled (Debian links to system packages)
- LibreOffice layer alone: **1.27 GB**

**Lesson**: Alpine doesn't help for Java-based applications like LibreOffice.

#### Pandoc Builds (1.35-1.42 GB - Larger!)

Pandoc requires full LaTeX distribution for quality PDFs:
- `texlive-latex-extra`: Thousands of packages
- Total TeXLive on Debian: **753 MB**
- Total TeXLive on Alpine: **666 MB**

**Lesson**: LaTeX is heavy regardless of base image.

#### Official pandoc/latex (1.03 GB - Smallest!)

- Pandoc team optimized TeXLive installation
- Alpine-based but well-optimized
- **But has critical formatting issues** (see next section)

---

## The Formatting Problem

### CRITICAL ISSUE: Pandoc DOCX→PDF Loses Formatting

We discovered Pandoc cannot preserve Word formatting during DOCX→PDF conversion:

| Feature | **LibreOffice** | **Pandoc** |
|---------|----------------|------------|
| Colors | ✅ Preserved | ❌ Stripped |
| Backgrounds | ✅ Preserved | ❌ Stripped |
| Borders | ✅ Preserved | ❌ Stripped |
| Table styling | ✅ Preserved | ❌ Lost |
| Code block backgrounds | ✅ Preserved | ❌ Removed |
| Professional appearance | ✅ Yes | ❌ Plain text look |

### Example Comparison

**LibreOffice PDF Output**:
```
┌─────────────────────────────┐
│ Code Block                  │ ← Gray background (#F5F5F5)
│ function hello() {          │
│   return "world";           │
│ }                           │
└─────────────────────────────┘
```

**Pandoc PDF Output**:
```
Code Block                     ← No background
function hello() {
  return "world";
}
```

### Why This Happens

Pandoc treats DOCX as **semantic markup**, not **visual formatting**:
- Focuses on document structure (headings, lists, paragraphs)
- Ignores presentation layer (colors, borders, backgrounds)
- Designed for Markdown ↔ DOCX conversion, not DOCX ↔ PDF

LibreOffice treats DOCX as **visual document**:
- Preserves ALL OpenXML formatting
- Renders exactly as Word would
- Industry standard for document conversion since 2003

### Web Research Confirms

From Stack Overflow:
> **Q:** "How do you keep the styling when you convert docx to pdf in Pandoc?"
> **A:** "You can't. Pandoc doesn't preserve visual formatting in DOCX→PDF conversion."

From GitHub Issues:
- Multiple reports of formatting loss in Pandoc DOCX→PDF
- Recommended solution: Use LibreOffice for formatting preservation

---

## Final Decision

### Why Native Deployment is the ONLY Solution

| Factor | Native | Docker |
|--------|--------|--------|
| **Filesystem Access** | ✅ Direct access anywhere | ❌ Requires complex volume mounts |
| **User Experience** | ✅ `pip install` + use | ❌ Build image + configure mounts + debug |
| **Setup Complexity** | ✅ Simple | ❌ High |
| **Performance** | ✅ Fast (no overhead) | ❌ Slower (container startup) |
| **Security** | ✅ User's own permissions | ❌ Either too restrictive or too permissive |
| **Maintenance** | ✅ Easy updates | ❌ Rebuild images + reconfigure |
| **Cross-Platform** | ✅ Works everywhere | ❌ Path translation issues |
| **Use Case Fit** | ✅ Perfect for ad-hoc conversions | ❌ Designed for workspace tools |

### The Architecture Mismatch

**MD-PDF-MCP is designed for**:
- Converting random documents from any location
- Ad-hoc usage ("convert this file right now")
- Flexible file access patterns
- Template files in various locations

**Docker MCP servers are designed for**:
- Working within predefined workspaces
- Consistent directory structures
- Project-based workflows
- Pre-configured file access

**These are fundamentally incompatible designs.**

---

## Current Recommendation

### ✅ PRIMARY DEPLOYMENT: Native (uvx/pip)

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "mcp-md-pdf": {
      "command": "uvx",
      "args": ["mcp-md-pdf"]
    }
  }
}
```

**User Setup**:
1. Install LibreOffice (one-time, like installing Node.js)
   - Windows: Download from libreoffice.org or use Microsoft Word
   - macOS: `brew install --cask libreoffice`
   - Linux: `sudo apt-get install libreoffice`
2. `pip install mcp-md-pdf` or use `uvx mcp-md-pdf`
3. Configure Claude Desktop (above)
4. Done - works with files ANYWHERE on system

---

### 🔧 SECONDARY: Docker for CI/CD Only

Docker is still useful for:
- GitHub Actions testing
- GitLab CI pipelines
- Isolated test environments
- Cross-platform testing

**Example CI/CD usage**:
```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t mcp-md-pdf:test .
      - name: Run tests
        run: docker run --rm mcp-md-pdf:test pytest -m "not slow"
```

**Why this works**:
- CI environments have predictable file locations
- Tests use temporary directories (no arbitrary paths)
- Isolation is beneficial for testing
- No user configuration needed

---

## Lessons Learned

1. **Not everything should be Dockerized**: Docker is powerful but not universal
2. **Understand your use case**: Workspace tools ≠ Document conversion tools
3. **Research real-world implementations**: All filesystem MCP servers use workspace-centric design
4. **Prioritize user experience**: Native installation is simpler than Docker configuration
5. **Formatting matters**: Size optimization means nothing if PDFs look terrible
6. **Architecture dictates deployment**: Our "accept any path" design requires native deployment

---

## FAQ

### Q: Can I still use Docker for MD-PDF-MCP?

**A:** Yes, but only for CI/CD and testing. Not recommended for end-user deployment via Claude Desktop.

### Q: What about Windows path translation?

**A:** This is exactly why Docker doesn't work. Translating Windows paths to container paths is fragile and breaks with edge cases.

### Q: Why not use Docker MCP Gateway?

**A:** Gateway doesn't solve the filesystem access problem. It's still constrained by volume mounts.

### Q: Is native installation secure?

**A:** Yes. Native installation runs with the user's own filesystem permissions (same as any other application like VS Code, Word, or Chrome).

### Q: What if I need complete isolation?

**A:** Use MD-PDF-MCP in a dedicated VM or isolated environment. Docker's isolation doesn't provide additional security benefits for this use case.

---

## Conclusion

After extensive research, testing, and analysis, we conclude that:

**Docker is architecturally incompatible with MD-PDF-MCP's design.**

The tool's strength—accepting arbitrary file paths for flexible document conversion—is fundamentally at odds with Docker's container isolation model.

**Native deployment is not a compromise. It's the correct architecture for this use case.**

---

## Timeline

- **Initial Docker implementation**: Worked but required complex configuration
- **Image size optimization**: Tried 7 approaches, found Pandoc has formatting issues
- **Ephemeral pattern adoption**: Cleaner but didn't solve filesystem access
- **Research phase**: Discovered all filesystem MCP servers use workspace-centric design
- **Architecture analysis**: Recognized fundamental incompatibility
- **Final decision**: Native-first deployment, Docker for CI/CD only

---

*This document serves as a reference for future contributors and users wondering "Why no Docker?"*

*Last updated: [Date of documentation]*
