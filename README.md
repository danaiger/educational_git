# ugit - Git Internals from Scratch

A Python implementation of Git's core functionality, built to understand how version control really works under the hood.

## What is this?

`ugit` is a simplified Git implementation that recreates the fundamental concepts of Git from first principles:

- **Content-addressable storage** - Files stored by their SHA1 hash
- **Tree objects** - Directory snapshots as recursive data structures
- **Commits** - Snapshots with parent pointers forming a DAG (Directed Acyclic Graph)
- **Branches & tags** - Named references to commits
- **Index/staging area** - Intermediate state between working directory and commits
- **3-way merging** - Combining divergent histories
- **Remote operations** - Push and fetch between repositories

This isn't meant to replace Git - it's a learning tool that exposes how Git's elegant design actually works.

## Installation

Requires Python 3.8+

```bash
# Clone the repository
git clone https://github.com/danaiger/educational_git.git
cd educational_git

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Usage

### Basic workflow

```bash
# Initialize a new repository
ugit init

# Add files to the staging area
ugit add myfile.py
ugit add src/              # Can add entire directories

# Check what's staged and what's modified
ugit status

# Create a commit
ugit commit -m "Initial commit"

# View commit history
ugit log
```

### Branching

```bash
# Create a new branch
ugit branch feature-x

# Switch to a branch
ugit checkout feature-x

# List all branches
ugit branch

# Merge a branch into current branch
ugit merge main
```

### Viewing changes

```bash
# Diff working directory vs index (unstaged changes)
ugit diff

# Diff index vs HEAD (staged changes)
ugit diff --cached

# Diff against a specific commit
ugit diff abc123

# Show a commit with its diff
ugit show
ugit show abc123
```

### Other commands

```bash
# Create a tag
ugit tag v1.0

# Visualize commit graph (requires graphviz)
ugit k

# Find common ancestor of two commits
ugit merge-base branch1 branch2

# Reset HEAD to a commit
ugit reset abc123

# Low-level: hash a file
ugit hash-object myfile.py

# Low-level: view object contents
ugit cat-file abc123
```

### Remote operations

```bash
# Fetch from a remote repository (local path)
ugit fetch ../other-repo

# Push to a remote repository
ugit push ../other-repo main
```

## Project Structure

```
ugit/
├── cli.py      # Command-line interface and argument parsing
├── base.py     # High-level operations (commit, checkout, merge)
├── data.py     # Low-level storage (objects, refs, index)
├── diff.py     # Tree comparison and 3-way merge
└── remote.py   # Push and fetch operations
```

## How it works

### Object storage

Every piece of content is stored as an object identified by its SHA1 hash:

- **Blobs** - File contents
- **Trees** - Directory listings (name → blob/tree mappings)
- **Commits** - Tree pointer + parent pointer(s) + message

Objects live in `.ugit/objects/` and are immutable once created.

### References

Branches and tags are just files containing commit hashes:

- `.ugit/refs/heads/main` → commit hash
- `.ugit/refs/tags/v1.0` → commit hash
- `.ugit/HEAD` → `ref: refs/heads/main` (symbolic ref)

### The index

The staging area (`.ugit/index`) maps file paths to blob hashes. It sits between your working directory and the next commit, allowing you to craft commits precisely.

## Acknowledgments

This project was built following Nikita Leshenko's excellent [ugit tutorial](https://www.leshenko.net/p/ugit/). The hands-on, step-by-step approach made Git's internals tangible and understandable.

## License

MIT
