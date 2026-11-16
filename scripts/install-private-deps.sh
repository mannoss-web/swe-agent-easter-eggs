#!/usr/bin/env bash
# Placeholder for private dependency installation.
# BuildKit injects MY_TOKEN. This script does not install or print anything.
set -euo pipefail

if [[ -z "${MY_TOKEN:-}" ]]; then
  echo "error: MY_TOKEN is empty. Pass it as a BuildKit secret: --secret id=MY_TOKEN,env=MY_TOKEN" >&2
  exit 1
fi

# TODO: install private dependencies with MY_TOKEN.
