#!/usr/bin/env bash
# PreToolUse hook: this repo uses bun (frontend) and uv (backend) exclusively.
# Block npm/npx/pnpm/yarn before they create stray lockfiles.
input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // empty')"

if printf '%s' "$command" | grep -qE '(^|[;&| ])(npm|npx|pnpm|yarn)( |$)'; then
  echo "Blocked: use 'bun'/'bunx' (frontend) or 'uv'/'uvx' (backend) instead of npm/npx/pnpm/yarn." >&2
  exit 2
fi
exit 0
