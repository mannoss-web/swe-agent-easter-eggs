"""Hidden, harmless Easter eggs. Not part of the documented interface."""

from __future__ import annotations

import os
import random
import re
import sys

import rich

# Characters that vanish on legacy Windows code pages (e.g. cp1252).
_EMOJI_FALLBACKS = {
    "🎮": "<game>",
    "🦖": ":rex:",
    "🦇": ":bat:",
    "♥": "<3",
    "🎉": "!",
    "🤠": ":)",
    "👋": ":wave:",
    "↑": "^",
    "↓": "v",
    "←": "<",
    "→": ">",
    "—": "-",
    "–": "-",
}


def _is_utf8_encoding(encoding: str | None) -> bool:
    name = (encoding or "").lower().replace("-", "").replace("_", "")
    return name in {"utf8", "utf8sig", "cp65001"}


def _reconfigure_utf8(stream) -> None:
    """Switch a text stream to UTF-8 if it is not already. Best-effort."""
    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is None or _is_utf8_encoding(getattr(stream, "encoding", None)):
        return
    try:
        reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def _enable_windows_vt_mode() -> None:
    """Turn on ANSI/VT processing on Windows consoles; no-op elsewhere."""
    if sys.platform != "win32":
        return
    try:
        # Classic Windows trick: the CRT enables ANSI escapes after this.
        os.system("")
    except Exception:
        pass
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        enable_vt = 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        for std_id in (-11, -12):  # STD_OUTPUT_HANDLE, STD_ERROR_HANDLE
            handle = kernel32.GetStdHandle(std_id)
            mode = ctypes.c_ulong()
            if handle and handle != -1 and kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | enable_vt)
        # Ask the console to decode UTF-8 so emoji actually render.
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:
        pass


def configure_output() -> None:
    """Make egg/console output safe on Windows and other legacy encodings.

    Enables virtual-terminal (ANSI) processing on Windows and, when stdout or
    stderr is not already UTF-8, reconfigures them to UTF-8 with a replace
    error handler so emoji and box-drawing characters do not crash the process.
    No-op on typical UTF-8 Linux and macOS terminals.
    """
    _enable_windows_vt_mode()
    for stream in (sys.stdout, sys.stderr):
        _reconfigure_utf8(stream)


def _legacy_safe(text: str) -> str:
    # Strip Rich markup first so replacements such as "<game>" are not removed.
    text = re.sub(r"\[/?[^\]]+\]", "", text)
    for src, dst in _EMOJI_FALLBACKS.items():
        text = text.replace(src, dst)
    encoding = getattr(sys.stdout, "encoding", None) or "ascii"
    return text.encode(encoding, errors="replace").decode(encoding)


def _egg_print(message: str) -> None:
    """Print with Rich, falling back to a legacy-code-page safe string."""
    configure_output()
    try:
        rich.print(message)
    except UnicodeEncodeError:
        sys.stdout.write(_legacy_safe(message) + "\n")


# A little T. rex — a nod to the SWE-ReX 🦖 mascot.
_DINO_ART = r"""
                   __
                  / _)
         _.----._/ /
        /         /
     __/ (  | (  |
    /__.-'|_|--|_|
"""

_DINO_QUIPS = (
    "SWE-ReX reporting for duty. Sandboxes are my natural habitat.",
    "I don't just debug code. I execute it... in a container.",
    "99 patch attempts later, the tests still pass in my head.",
    "Ask not what your runtime can do for you — ask what you can commit.",
    "Have you tried turning the container off and on again?",
)

_KONAMI_MESSAGE = """
🎮  Cheat code accepted.

    ↑ ↑ ↓ ↓ ← → ← → B A

    30 lives added. The agent is now invincible.
    (Cost limits still apply. Nice try.)
""".strip()


def print_dino() -> None:
    """Print ASCII art of the SWE-ReX mascot and a short quip."""
    quip = random.choice(_DINO_QUIPS)
    _egg_print(f"[bold green]{_DINO_ART}[/bold green]")
    _egg_print("[bold]SWE-ReX[/bold]  🦖")
    _egg_print(f"[italic]{quip}[/italic]")


_CASTLEVANIA_ART = r"""
          ^v^
                                 ( )
     o=======D~~~~~~~~~~~~~~*     '
    /|
    / \
"""

_CASTLEVANIA_QUIPS = (
    "What is a man? A miserable little pile of bugs!",
    "Die monster! You don't belong in this codebase!",
    "The whip is mightier than the stack trace.",
)


def print_konami() -> None:
    """Print a Konami-code reward message."""
    _egg_print(f"[bold magenta]{_KONAMI_MESSAGE}[/bold magenta]")


def print_castlevania() -> None:
    """Print a small Simon Belmont scene and a short quip."""
    quip = random.choice(_CASTLEVANIA_QUIPS)
    _egg_print(f"[bold red]{_CASTLEVANIA_ART}[/bold red]")
    _egg_print("[bold]Simon Belmont[/bold]  🦇")
    _egg_print(f"[italic]{quip}[/italic]")


# Powered-up scene: Konami code + Castlevania (Harmony of Dissonance unlocks Simon).
_CASTLEVANIA_KONAMI_ART = r"""
        ♥  ♥  ♥
          ^v^
                                                        ( )
    \o/***=======D~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*~*~*    *
     |                                                  '
    / \
"""

_CASTLEVANIA_KONAMI_MESSAGE = """
🎮  Cheat code accepted.

    ↑ ↑ ↓ ↓ ← → ← → B A  —  Vampire Killer unlocked!

    30 hearts added. Dracula's castle has no bugs left to hide.
""".strip()


def print_castlevania_konami() -> None:
    """Print the powered-up Simon Belmont scene (Konami code + Castlevania)."""
    _egg_print(f"[bold yellow]{_CASTLEVANIA_KONAMI_ART}[/bold yellow]")
    _egg_print("[bold]Simon Belmont[/bold]  🦇  [yellow]Vampire Killer[/yellow]")
    _egg_print(f"[bold magenta]{_CASTLEVANIA_KONAMI_MESSAGE}[/bold magenta]")
