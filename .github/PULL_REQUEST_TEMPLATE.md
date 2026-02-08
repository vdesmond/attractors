## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] New attractor system
- [ ] New solver
- [ ] New theme
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe):

---

## For New Attractor Submissions

<!-- If you're adding a new attractor, please complete this section -->

### Attractor Information

**Name**: <!-- e.g., "Lorenz Attractor" -->

**System name in code**: <!-- e.g., "lorenz" (lowercase, snake_case) -->

**Dimension**: <!-- 2D or 3D -->

**Historical context**:
<!-- Brief description: Who discovered it? When? What makes it interesting? -->

### Parameters

**Default parameters**:
```python
{
    "param1": value1,
    "param2": value2,
    # ...
}
```

**Parameter sources**: <!-- Literature reference, original paper, or your own exploration -->

**Initial conditions**: `[x, y, z]` <!-- e.g., [1.0, 1.0, 1.0] -->

### Validation Checklist

- [ ] System exhibits chaotic behavior (sensitive dependence on initial conditions)
- [ ] Trajectory is bounded (doesn't diverge to infinity)
- [ ] Equations are implemented with `@njit` decorator
- [ ] Default parameters produce stable, visually interesting results
- [ ] Tested with multiple `dt` values (0.001, 0.01, 0.1)
- [ ] Verified with different initial conditions
- [ ] Integration tests added
- [ ] Chaos validation test added (sensitivity to IC)
- [ ] Example visualization included in `examples/`

### Visual Preview

<!-- Optional but encouraged: Include a screenshot or link to visualization -->

---

## General Checklist

<!-- All PRs should complete this section -->

- [ ] Code follows style guidelines (`uv run ruff format`, `uv run ruff check`)
- [ ] Type hints pass validation (`uv run mypy src/`)
- [ ] All tests pass locally (`uv run pytest`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (if applicable)
- [ ] No unnecessary files added (temporary files, IDE configs, etc.)
- [ ] Commit messages are clear and descriptive

## Testing

<!-- Describe how you tested your changes -->

**Test command**:
```bash
uv run pytest tests/...
```

**Test results**:
<!-- Paste relevant output or describe what you verified -->

## Additional Context

<!-- Add any other context, screenshots, references, or notes about the PR -->

## References

<!-- Optional: Papers, articles, or resources related to this submission -->

---

**By submitting this PR, I confirm that my contribution is made under the terms of the MIT License.**
