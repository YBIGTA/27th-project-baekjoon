#!/usr/bin/env bash
set -euo pipefail

# Ensure directory exists
mkdir -p "$HOME/.boj-cli"
chmod 700 "$HOME/.boj-cli"

# If BOJ_KEY provided, write/update file (avoid layer caching secrets)
if [[ -n "${BOJ_KEY:-}" ]]; then
  echo -n "$BOJ_KEY" > "$HOME/.boj-cli/key"
  chmod 644 "$HOME/.boj-cli/key"
fi

# If BOJ_CREDENTIAL provided, write/update file
if [[ -n "${BOJ_CREDENTIAL:-}" ]]; then
  echo -n "$BOJ_CREDENTIAL" > "$HOME/.boj-cli/credential"
  chmod 644 "$HOME/.boj-cli/credential"
fi

# Execute the passed command
exec "$@"