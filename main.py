#!/usr/bin/env python3
"""Save the one-line roast of my own agent to /output/entry.txt.

No input is read, no service is contacted, and neither the clock
nor any source of randomness is involved, so the file written out
is byte-for-byte the same on every single run.
"""

import sys
from pathlib import Path

SENTENCE = (
    "My agent has one skill: turning a five-minute task into "
    "a three-hour investigation of a typo it introduced itself."
)
CEILING = 200
TARGET = Path("/output/entry.txt")


class EntryProblem(ValueError):
    """The frozen roast failed one of its own checks."""


def screen_entry(value):
    """Put the roast through its checks, shortest verdicts first."""
    if value is None or value.strip() == "":
        raise EntryProblem("roast is empty or nothing but whitespace")
    if len(value) > CEILING:
        raise EntryProblem("roast is over the 200-character ceiling")
    if "\t" in value:
        raise EntryProblem("roast must not contain a tab")
    if "\n" in value:
        raise EntryProblem("roast must be a single line")
    if "  " in value:
        raise EntryProblem("roast must not contain a double space")
    if value != value.strip():
        raise EntryProblem("roast must not start or end with a space")
    if any(ord(ch) < 32 for ch in value):
        raise EntryProblem("roast must not contain a control character")
    if all(not ch.isalnum() and not ch.isspace() for ch in value):
        raise EntryProblem("roast must not be punctuation alone")
    if value.isdigit():
        raise EntryProblem("roast must not be digits only")
    if not any(ch.isalpha() for ch in value):
        raise EntryProblem("roast must contain at least one letter")
    return value


def main():
    """Screen the frozen roast, then write it to disk."""
    try:
        passed = screen_entry(SENTENCE)
    except EntryProblem as trouble:
        print(f"rejected entry: {trouble}", file=sys.stderr)
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(passed, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
