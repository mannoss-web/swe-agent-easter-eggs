"""Hidden, harmless Easter eggs. Not part of the documented interface."""

from __future__ import annotations

import logging
import os
import random
import re
import sys
from collections.abc import Mapping
from datetime import date

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
    "☕": "(coffee)",
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


_COFFEE_ART = r"""
      )  (
     (   ) )
      ) ( (
    _______)_
 .-'---------|
( C|         |
 '-|         |
   '_________'
    '-------'
"""

_COFFEE_QUOTES = (
    "The bug was no match for a fresh cup.",
    "One cup for the code, one for the tests.",
    "Brewed, not stirred.",
)


def print_coffee() -> None:
    """Print a cup of coffee and a short quote."""
    quote = random.choice(_COFFEE_QUOTES)
    _egg_print(f"[bold yellow]{_COFFEE_ART}[/bold yellow]")
    _egg_print("[bold]SWE-agent coffee[/bold]  ☕")
    _egg_print(f"[italic]{quote}[/italic]")


_PARTY_TRUTHY = {"1", "true", "yes", "on"}
PARTY_BANNER = "🎉 SWE-AGENT PARTY MODE 🎉  Let's fix some bugs and maybe dance a little. 🦖🤠"

# Month, day -> one startup line. Logged only; never written into a trajectory.
_NOTABLE_DATES: dict[tuple[int, int], str] = {
    (3, 14): "Pi day. May your patches be as well-rounded as 3.14159.",
    (4, 1): "April 1st. All bugs reported today are features. Probably.",
    (5, 6): "Happy birthday to the SWE-agent paper (6 May 2024). The interface was the lever.",
}

# About one finished run in a hundred. A private RNG is used so this never
# advances the process-wide random stream (batch shuffling uses that).
FORTUNE_PROBABILITY = 0.01
_RUN_FORTUNES = (
    "Read the traceback from the bottom.",
    "A failing test is a breadcrumb, not an insult.",
    "The container is fine. The assumption was not.",
    "Smaller diff, happier reviewer.",
    "If you cannot explain the patch, do not submit it yet.",
)

# Exact agent actions only. Anything else, including a prefix or extra command, is ignored.
_MAGIC_REPLIES = {
    "sudo make me a sandwich": "What? Make it yourself.",
    "sudo make me a sandwich --please": "Okay.",
    "open the pod bay doors": "I'm sorry, Dave. I'm afraid I can't do that.",
}


def party_mode_enabled(environ: Mapping[str, str] | None = None) -> bool:
    """True when SWEAGENT_PARTY or SWE_AGENT_PARTY is set to a truthy value."""
    env = os.environ if environ is None else environ
    for name in ("SWEAGENT_PARTY", "SWE_AGENT_PARTY"):
        if env.get(name, "").strip().lower() in _PARTY_TRUTHY:
            return True
    return False


def notable_date_message(today: date | None = None) -> str | None:
    """Return a one-line greeting on Pi day, April 1st, or 6 May, else None."""
    current = date.today() if today is None else today
    return _NOTABLE_DATES.get((current.month, current.day))


def rare_fortune(
    rng: random.Random | None = None,
    *,
    probability: float = FORTUNE_PROBABILITY,
) -> str | None:
    """Return a fortune with `probability`, otherwise None.

    Pass an rng in tests. The default roller is a fresh `random.Random()`,
    which does not touch the global random state.
    """
    roller = random.Random() if rng is None else rng
    if roller.random() >= probability:
        return None
    return roller.choice(_RUN_FORTUNES)


def log_rare_fortune(logger: logging.Logger) -> None:
    """Maybe log one fortune after a run has already been saved.

    Skipped under pytest so the suite stays deterministic. `SWE_AGENT_FORTUNE=1`
    forces a line; `0` silences it. The line is log-only and is not written
    into trajectories, predictions, or model prompts.
    """
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return
    forced = os.environ.get("SWE_AGENT_FORTUNE", "").strip().lower()
    if forced in {"0", "false", "no", "off"}:
        return
    probability = 1.0 if forced in _PARTY_TRUTHY else FORTUNE_PROBABILITY
    line = rare_fortune(probability=probability)
    if line:
        logger.info("Fortune: %s", line)


def magic_tool_reply(action: str) -> str | None:
    """Playful observation for one exact action, or None for everything else."""
    return _MAGIC_REPLIES.get(action.strip())
