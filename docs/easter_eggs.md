# Easter eggs

!!! warning "Spoilers"
    Hidden extras. None of them run unless you ask, the date matches, or (for one log line) you win a 1-in-100 roll. Ordinary runs, benchmark scores, trajectory files, and the prompts sent to the model stay the same.

## `sweagent dino`

```bash
sweagent dino
# or: sweagent rex
```

Prints an ASCII SWE-ReX and a short quip. Not listed in `sweagent --help`.

## `sweagent coffee`

```bash
sweagent coffee
# or: sweagent brew
```

Prints a cup of coffee and a quote. Not listed in `sweagent --help`.

## Konami code

```bash
sweagent --uuddlrlrba
```

Prints a cheat-code message and exits. The flag is not listed in `--help`.

## Castlevania

```bash
sweagent castlevania
# or: sweagent belmont
```

Prints a small Simon Belmont scene. Combine it with the Konami code for the powered-up version:

```bash
sweagent castlevania --uuddlrlrba
```

## Party mode

```bash
SWEAGENT_PARTY=1 sweagent --help
# or: SWE_AGENT_PARTY=1 sweagent --help
```

Truthy values are `1`, `true`, `yes`, and `on`. The startup log gains one festive line. Console formatting otherwise stays as it was.

## Notable dates

On 14 March (Pi day), 1 April, and 6 May (the SWE-agent paper, arXiv:2405.15793, first posted in 2024), startup logs one extra greeting. Any other day is silent. The line is not written into a trajectory.

## Rare fortune

About one finished `run`, `run-batch`, or `shell` in a hundred logs a single tip after predictions are saved:

```text
Fortune: Read the traceback from the bottom.
```

It uses its own random generator, so it does not change batch shuffling. It is not stored in the trajectory or the prediction file.

```bash
SWE_AGENT_FORTUNE=1 sweagent run ...   # always log one
SWE_AGENT_FORTUNE=0 sweagent run ...   # never log one
```

## Magic words

If the agent's action is exactly one of these strings, the tool layer answers in character and does not run the command:

| Action | Reply |
| --- | --- |
| `sudo make me a sandwich` | What? Make it yourself. |
| `sudo make me a sandwich --please` | Okay. |
| `open the pod bay doors` | I'm sorry, Dave. I'm afraid I can't do that. |

Any other action, including one that merely contains these words, is executed as usual. The strings are not added to the system prompt or the tool docs.

## `fortune` tool

`tools/fortune` is a tool bundle that prints a software-engineering proverb. It is not enabled in the default configs, so the model never sees it unless you opt in:

```yaml
agent:
  tools:
    bundles:
      - path: tools/fortune
```

Then the agent (or you, inside the shell) can run `fortune`.
