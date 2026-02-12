# Claude Code Guidelines for ugit

## Project Overview
Educational Git implementation in Python. The codebase demonstrates Git internals through a minimal implementation.

## Development Workflow

### Planning First
Always plan before implementing. Use small, incremental steps:
1. Understand the task scope
2. Break into small, testable pieces
3. Plan each piece before coding
4. Implement one piece at a time
5. Verify before moving on

### Git Practices
- **Independent features in separate branches** - Each feature/fix gets its own branch
- **Clear commit history** - One logical change per commit
- **Descriptive branch names** - e.g., `add-test-infrastructure`, `fix-merge-conflict-handling`
- **PR per feature** - Keep PRs focused and reviewable

### Running the Project
```bash
# Run tests
uv run --extra dev pytest

# Run specific test file
uv run --extra dev pytest tests/test_data.py -v
```

## Code Standards

### Python Best Practices
- Use type hints for function signatures
- Follow PEP 8 style guidelines
- Keep functions focused and small
- Prefer explicit over implicit

### Testing Approach
- **Behavior-focused tests** - Test what functions do, not how they do it
- **No mocking where possible** - Use real objects, set up real state
- **Bottom-up testing** - Start with low-level functions, build up
- **Fixtures for setup** - Use pytest fixtures for common setup patterns
