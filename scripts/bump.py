#!/usr/bin/env python3
"""Set the version and every sha256 of the formula and the cask from a release's SHA256SUMS.

Usage:
    scripts/bump.py --version 0.2.0 --sums SHA256SUMS [--formula Formula/knode.rb] [--cask Casks/knode.rb]

Each `sha256` takes the checksum of the asset its `url` points at, with `#{version}` replaced by
the new version. The formula's archives must all be in SHA256SUMS. When the release has no
`Knode-<version>.dmg`, the cask is left as it is and a warning is printed.

Standard library only, so it runs on any runner with Python 3.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_LINE = re.compile(r'^(\s*version\s+)"[^"]*"', re.MULTILINE)
URL_LINE = re.compile(r'^\s*url\s+"([^"]+)"')
SHA_LINE = re.compile(r'^(\s*sha256\s+)"[^"]*"')
HEX_RE = re.compile(r"^[0-9a-f]{64}$")


class BumpError(Exception):
    pass


def parse_sums(text: str) -> dict[str, str]:
    """Parse `sha256sum` output: `<hex>  <name>` (or `<hex> *<name>`) per line."""
    sums: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or not HEX_RE.match(parts[0].lower()):
            raise BumpError(f"SHA256SUMS line {number} is not '<sha256>  <file>': {line!r}")
        name = parts[1].lstrip("*").strip()
        sums[Path(name).name] = parts[0].lower()
    if not sums:
        raise BumpError("SHA256SUMS is empty")
    return sums


def asset_name(url: str, version: str) -> str:
    return url.replace("#{version}", version).rsplit("/", 1)[-1]


def set_version(text: str, version: str, path: str) -> str:
    new, count = VERSION_LINE.subn(rf'\g<1>"{version}"', text)
    if count != 1:
        raise BumpError(f"{path}: expected one `version` line, found {count}")
    return new


def bump_formula(text: str, version: str, sums: dict[str, str], path: str = "formula") -> str:
    """In the formula every `sha256` follows the `url` it belongs to."""
    lines = set_version(text, version, path).splitlines(keepends=True)
    url = None
    changed = 0
    for i, line in enumerate(lines):
        if m := URL_LINE.match(line):
            url = m.group(1)
            continue
        if m := SHA_LINE.match(line):
            if url is None:
                raise BumpError(f"{path}:{i + 1}: `sha256` without a `url` before it")
            name = asset_name(url, version)
            if name not in sums:
                raise BumpError(f"{path}: {name} is not in SHA256SUMS")
            lines[i] = SHA_LINE.sub(rf'\g<1>"{sums[name]}"', line)
            url = None
            changed += 1
    if changed == 0:
        raise BumpError(f"{path}: no `sha256` lines found")
    return "".join(lines)


def cask_asset(text: str, version: str, path: str = "cask") -> str:
    urls = [m.group(1) for line in text.splitlines() if (m := URL_LINE.match(line))]
    # The livecheck block uses `url :url`, which the pattern does not match.
    if len(urls) != 1:
        raise BumpError(f"{path}: expected one download `url`, found {len(urls)}")
    return asset_name(urls[0], version)


def bump_cask(text: str, version: str, sums: dict[str, str], path: str = "cask") -> str:
    """The cask has one `sha256` and one download `url`, in either order."""
    name = cask_asset(text, version, path)
    if name not in sums:
        raise BumpError(f"{path}: {name} is not in SHA256SUMS")
    text = set_version(text, version, path)
    lines = text.splitlines(keepends=True)
    shas = [i for i, line in enumerate(lines) if SHA_LINE.match(line)]
    if len(shas) != 1:
        raise BumpError(f"{path}: expected one `sha256` line, found {len(shas)}")
    lines[shas[0]] = SHA_LINE.sub(rf'\g<1>"{sums[name]}"', lines[shas[0]])
    return "".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--version", required=True, help="the release version, X.Y.Z without the v")
    parser.add_argument("--sums", required=True, type=Path, help="the release's SHA256SUMS")
    parser.add_argument("--formula", type=Path, default=Path("Formula/knode.rb"))
    parser.add_argument("--cask", type=Path, default=Path("Casks/knode.rb"))
    args = parser.parse_args(argv)

    try:
        if not VERSION_RE.match(args.version):
            raise BumpError(f"version {args.version!r} is not X.Y.Z (pre-releases are not offered)")
        sums = parse_sums(args.sums.read_text())

        # Both files are checked before either is written.
        formula = bump_formula(args.formula.read_text(), args.version, sums, str(args.formula))
        cask = args.cask.read_text()
        name = cask_asset(cask, args.version, str(args.cask))
        new_cask = bump_cask(cask, args.version, sums, str(args.cask)) if name in sums else None

        args.formula.write_text(formula)
        print(f"{args.formula}: {args.version}")
        if new_cask is not None:
            args.cask.write_text(new_cask)
            print(f"{args.cask}: {args.version}")
        else:
            print(f"::warning::{name} is not in SHA256SUMS, {args.cask} is left as it is")
    except (BumpError, OSError) as error:
        print(f"::error::{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
