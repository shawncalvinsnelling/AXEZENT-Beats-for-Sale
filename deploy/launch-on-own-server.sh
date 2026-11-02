#!/usr/bin/env bash
# Start AXEZENT on your own Linux computer / server.
# Needs Docker Compose, a real DNS hostname and all 50 private tagged MP3s.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker with Docker Compose is required on your own server." >&2
  exit 1
fi
if [[ ! -f .env ]]; then
  echo "ERROR: Copy .env.example to .env and set AXEZENT_DOMAIN to a REAL domain." >&2
  exit 1
fi
set -a; . ./.env; set +a
if [[ -z "$AXEZENT_DOMAIN" ]] ||
   [[ "$AXEZENT_DOMAIN" == *example* ]] ||
   [[ "$AXEZENT_DOMAIN" == *localhost* ]] ||
   [[ "$AXEZENT_DOMAIN" != *.* ]] ||
   [[ ! "$AXEZENT_DOMAIN" =~ ^[a-zA-Z0-9.-]+$ ]]; then
  echo "ERROR: AXEZENT_DOMAIN is not a usable public hostname." >&2
  exit 1
fi

mkdir -p private_previews
if [[ -L private_previews ]]; then
  echo "ERROR: private_previews must be a real private directory, not a symlink." >&2
  exit 1
fi
chmod 700 private_previews

python3 scripts/check_owned_preview_library.py --preview-dir private_previews
# Docker must have the same identity as the user who owns the 0700 MP3 folder.
export AXEZENT_UID
export AXEZENT_GID
AXEZENT_UID="$(id -u)"
AXEZENT_GID="$(id -g)"
if [[ "$AXEZENT_UID" == "0" ]]; then
  echo "WARNING: Run this script as the normal Linux account that owns the private previews, not sudo." >&2
fi

echo "Starting AXEZENT site at https://$AXEZENT_DOMAIN/"
echo "This does not by itself configure your router, DNS, or public Internet access."
docker compose config --quiet
docker compose up --detach --build

echo "Own server containers started or starting."
echo "Check from mobile data: https://$AXEZENT_DOMAIN/api/ready"
echo "When the public API is ready, use the GitHub Actions workflow"
echo "'Activate one-click AXEZENT player link' to verify all 50 and add the link to the README."
