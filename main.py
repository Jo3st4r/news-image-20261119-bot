"""news-image-20261119 entrypoint.

Ships the vendored poster (assets/entry.png) to /output/entry.png,
byte-for-byte. Standard library only: no network access, no clock,
no randomness, so every run writes identical bytes.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POSTER = HERE / "assets" / "entry.png"
OUT_DIR = Path("/output")
OUT_FILE = OUT_DIR / "entry.png"


def digest_hex(data: bytes) -> str:
    """Hex SHA-256 of a byte string."""
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if not POSTER.is_file():
        print(f"poster not found: {POSTER}", file=sys.stderr)
        return 1
    payload = POSTER.read_bytes()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_bytes(payload)
    print(
        f"wrote {OUT_FILE} "
        f"({len(payload)} bytes, sha256 {digest_hex(payload)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
