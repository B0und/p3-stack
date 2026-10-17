#!/usr/bin/env bash
set -euo pipefail

P3_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
P3_PROJECT=""
P3_PROVIDER="all"

usage() {
  printf 'Usage: %s [--project PATH] [--provider all|codex|claude]\n' "$0"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 && -n "$2" && "$2" != --* ]] || { usage >&2; exit 2; }
      P3_PROJECT="$2"
      shift 2
      ;;
    --provider)
      [[ $# -ge 2 ]] || { usage >&2; exit 2; }
      P3_PROVIDER="$2"
      shift 2
      ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done

case "$P3_PROVIDER" in
  all|codex|claude) ;;
  *) usage >&2; exit 2 ;;
esac

install_into() {
  local target="$1" skill name destination existing installed=0 unchanged=0 skipped=0
  mkdir -p "$target"
  for skill in "$P3_ROOT"/skills/*/; do
    [[ -f "$skill/SKILL.md" ]] || continue
    name="$(basename "$skill")"
    destination="$target/$name"
    if [[ -L "$destination" ]]; then
      existing="$(readlink "$destination")"
      if [[ "$existing" == "$skill" || "$existing" == "${skill%/}" ]]; then
        unchanged=$((unchanged + 1))
      else
        printf 'skip %s (existing symlink)\n' "$destination"
        skipped=$((skipped + 1))
      fi
    elif [[ -e "$destination" ]]; then
      printf 'skip %s (existing file or directory)\n' "$destination"
      skipped=$((skipped + 1))
    else
      ln -s "$skill" "$destination"
      installed=$((installed + 1))
    fi
  done
  printf '%s: linked %d, unchanged %d, skipped %d\n' "$target" "$installed" "$unchanged" "$skipped"
}

if [[ "$P3_PROVIDER" == all || "$P3_PROVIDER" == codex ]]; then
  install_into "${P3_PROJECT:-$HOME}/.agents/skills"
fi
if [[ "$P3_PROVIDER" == all || "$P3_PROVIDER" == claude ]]; then
  if [[ -n "$P3_PROJECT" ]]; then
    install_into "$P3_PROJECT/.claude/skills"
  else
    install_into "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
  fi
fi
