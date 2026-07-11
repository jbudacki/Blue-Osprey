#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
SKILLS_HOME=${CODEX_SKILLS_HOME:-"$HOME/.agents/skills"}
STAMP=$(date -u '+%Y%m%dT%H%M%SZ')-$$
DRY_RUN=0
WITH_USER_CONFIG=0

usage() {
  printf '%s\n' \
    'Usage: ./install.sh [--dry-run] [--with-user-config]' \
    '' \
    '  --dry-run           Show destinations without changing files.' \
    '  --with-user-config  Replace config.toml with the portable snapshot.'
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --with-user-config) WITH_USER_CONFIG=1 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$arg" >&2; usage >&2; exit 2 ;;
  esac
done

backup_destination() {
  destination=$1
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    backup="${destination}.backup-${STAMP}"
    printf 'Back up %s -> %s\n' "$destination" "$backup"
    if [ "$DRY_RUN" -eq 0 ]; then
      mv "$destination" "$backup"
    fi
  fi
}

install_file() {
  source_file=$1
  destination=$2
  printf 'Install %s -> %s\n' "$source_file" "$destination"
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$(dirname -- "$destination")"
    backup_destination "$destination"
    cp "$source_file" "$destination"
  fi
}

install_directory() {
  source_directory=$1
  destination=$2
  printf 'Install %s -> %s\n' "$source_directory" "$destination"
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$(dirname -- "$destination")"
    backup_destination "$destination"
    cp -R "$source_directory" "$destination"
  fi
}

install_file "$ROOT/config/blue-osprey.config.toml" "$CODEX_HOME/blue-osprey.config.toml"
install_file "$ROOT/config/AGENTS.md" "$CODEX_HOME/AGENTS.md"

for source_skill in "$ROOT"/blue-osprey/skills/*; do
  [ -d "$source_skill" ] || continue
  skill_name=${source_skill##*/}
  install_directory "$source_skill" "$SKILLS_HOME/$skill_name"
done

if [ "$WITH_USER_CONFIG" -eq 1 ]; then
  install_file "$ROOT/config/config.portable.toml" "$CODEX_HOME/config.toml"
else
  printf '%s\n' 'Personal config not replaced. Use --with-user-config to opt in.'
fi

if [ "$DRY_RUN" -eq 1 ]; then
  printf '%s\n' 'Dry run complete; no files changed.'
else
  printf '%s\n' 'Install complete. Restart Codex, then use --profile blue-osprey in the CLI.'
fi
