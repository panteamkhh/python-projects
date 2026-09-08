"""
Shared input-validation helpers used across the Day 1-9 projects.

Extracting these into one place is the main goal of Refactor Week:
several projects (Guess Number, Todo App, Banking System) were each
implementing their own "keep asking until the user enters a valid
number" loop. That logic now lives in one tested place.
"""


def get_valid_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Repeatedly prompt until the user enters a valid int within range."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue

        return value


def get_valid_float(prompt: str, min_value: float = None) -> float:
    """Repeatedly prompt until the user enters a valid float."""
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue

        return value


def confirm(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question and return a bool."""
    suffix = " (Y/n): " if default else " (y/N): "
    raw = input(prompt + suffix).strip().lower()
    if raw == "":
        return default
    return raw.startswith("y")
