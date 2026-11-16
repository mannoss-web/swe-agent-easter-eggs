"""Hidden, harmless Easter eggs. Not part of the documented interface."""

from __future__ import annotations

import random

import rich

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
    rich.print(f"[bold green]{_DINO_ART}[/bold green]")
    rich.print("[bold]SWE-ReX[/bold]  🦖")
    rich.print(f"[italic]{quip}[/italic]")


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
    rich.print(f"[bold magenta]{_KONAMI_MESSAGE}[/bold magenta]")


def print_castlevania() -> None:
    """Print a small Simon Belmont scene and a short quip."""
    quip = random.choice(_CASTLEVANIA_QUIPS)
    rich.print(f"[bold red]{_CASTLEVANIA_ART}[/bold red]")
    rich.print("[bold]Simon Belmont[/bold]  🦇")
    rich.print(f"[italic]{quip}[/italic]")


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
    rich.print(f"[bold yellow]{_CASTLEVANIA_KONAMI_ART}[/bold yellow]")
    rich.print("[bold]Simon Belmont[/bold]  🦇  [yellow]Vampire Killer[/yellow]")
    rich.print(f"[bold magenta]{_CASTLEVANIA_KONAMI_MESSAGE}[/bold magenta]")
