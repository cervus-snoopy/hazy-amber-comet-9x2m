#!/usr/bin/env python3
"""Break Production, Own It — entry for
u-ricoxyz-break-production-own-it-be78a994.

Writes one brutally honest postmortem line to <output dir>/entry.txt,
under 200 characters, with no trailing newline.
"""

import os
import stat
from pathlib import Path

LINE = "I pushed the .env to a public repo. Within four minutes a bot had every key; the keys are rotated, my access is revoked, and the repo is still public."

# Gate: entry.txt must hold one line of 1 to 199 characters.
MAX_LINE_CHARS = 199


def check_line(text):
    if not 1 <= len(text) <= MAX_LINE_CHARS:
        raise ValueError("line is %d characters, gate is 1 to 199" % len(text))
    if text != text.strip():
        raise ValueError("line must not start or end with whitespace")
    return text


def run():
    line = check_line(LINE)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    entry_path = output_dir / "entry.txt"
    entry_path.write_text(line, encoding="utf-8")
    written = entry_path.read_text(encoding="utf-8")
    assert len(written) == len(line), "entry.txt lost characters on disk"
    # Outputs must be readable by every user (the grader collects them
    # as another user): files 0644, folders 0755.
    os.chmod(entry_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    os.chmod(output_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP
             | stat.S_IROTH | stat.S_IXOTH)


if __name__ == "__main__":
    run()
