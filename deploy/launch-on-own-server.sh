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

python3 - <<'PY'
import json
from pathlib import Path
root=Path("private_previews")
catalog=json.loads(Path("data/catalog.json").read_text(encoding="utf-8"))
first=[b for b in catalog if isinstance(b.get("releaseRank"),int) and 1<=b["releaseRank"]<=50]
if len(first)!=50 or len({b["id"] for b in first})!=50:
    raise SystemExit("ERROR: First 50 beats are not uniquely identified in catalog.")
missing=[]
for b in first:
    p=root/(b["id"]+"-tagged.mp3")
    if not p.is_file() or p.is_symlink() or not (100_000<=p.stat().st_size<=10*1024*1024):
        missing.append(b["id"])
    else:
        with p.open("rb") as f: header=f.read(3)
        if not (header==b"ID3" or header[:2] in (b"\xff\xfb",b"\xff\xf3",b"\xff\xf2")):
            missing.append(b["id"])
if missing:
    raise SystemExit("ERROR: %d/50 private MP3 previews absent/invalid. First missing: %s"%
                     (len(missing),", ".join(missing[:6])))
print("PASS: 50/50 private preview MP3 files present; no masters are included in public source.")
PY

echo "Starting AXEZENT site at https://$AXEZENT_DOMAIN/"
echo "This does not by itself configure your router, DNS, or public Internet access."
docker compose config --quiet
docker compose up --detach --build

echo "Own server containers started or starting."
echo "Check from mobile data: https://$AXEZENT_DOMAIN/api/ready"
echo "When the public API is ready, use the GitHub Actions workflow"
echo "'Activate one-click AXEZENT player link' to verify all 50 and add the link to the README."
