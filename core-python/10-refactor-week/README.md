# Day 10 - Refactor Week

Instead of a new project, Day 10 goes back over Days 1-9 and cleans up
a repeated pattern: **every project that reads a number from the user
was writing its own validation loop.**

## What changed

A shared `utils/validators.py` module was extracted with three
reusable functions:

- `get_valid_int(prompt, min_value=None, max_value=None)`
- `get_valid_float(prompt, min_value=None)`
- `confirm(prompt, default=True)`

### Before (duplicated in Day 1, Day 3, Day 9)
```python
try:
    user_input = int(input("Enter task number to delete: "))
    if 1 <= user_input <= len(tasks):
        ...
except ValueError:
    print("Please enter a valid number ❗")
```

### After (one shared, tested helper)
```python
from utils.validators import get_valid_int

index = get_valid_int("Enter task number to delete: ", min_value=1, max_value=len(tasks)) - 1
```

## Why this matters

- **DRY**: one bug fix or improvement (e.g. supporting negative numbers,
  or adding a retry limit) now applies everywhere instead of needing to
  be copy-pasted into every project.
- **Testability**: the validation logic can be unit-tested in isolation
  by monkeypatching `input()` (see `test_validators.py`), instead of
  only being tested by manually running each program.
- **Readability**: each project's own `main.py` now focuses on *what*
  it does, not on *how* it parses input.

## How to test
```bash
pytest test_validators.py
```

## Next step
Days 1, 3, and 9 can be updated to import from `utils.validators`
instead of their local input-parsing code — left as a follow-up since
the goal of this day was to identify and extract the duplication, not
rewrite every project.
