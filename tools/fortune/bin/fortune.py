#!/usr/bin/env python3
"""Hidden SWE-agent Easter egg. Not enabled in default configs.

Python entry point so the fortune tool can run when bash is missing
(for example on Windows). Keep the proverb list in sync with the
``fortune`` bash script in this directory.
"""

from __future__ import annotations

import random
import sys

PROVERBS = (
    "First, make it work. Then, make it pretty. Then, make it fast.",
    "Premature optimization is the root of all evil. — Donald Knuth",
    "Deleted code is debugged code.",
    "A clean test is a love letter to your future self.",
    "If it is not written down, it did not happen. Commit early.",
    "The best code is no code at all.",
    "There are only two hard things in computer science: cache invalidation, naming things, and off-by-one errors.",
    "It works on my machine is not a test plan.",
    "Read the error message. Then read it again.",
    "Fix the test, not the assertion — unless the assertion was wrong.",
)


def _reconfigure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is None:
        return
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower().replace("-", "").replace("_", "")
    if encoding in {"utf8", "utf8sig", "cp65001"}:
        return
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> None:
    _reconfigure_stdout()
    proverb = random.choice(PROVERBS)
    try:
        print(proverb)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        print(proverb.replace("—", "-").encode(encoding, errors="replace").decode(encoding))


if __name__ == "__main__":
    main()
