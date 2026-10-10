#!/usr/bin/env python3
"""Check explicit slice contracts without expanding ownership globs."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path, PurePosixPath
import re


HEADER = re.compile(r"^#{2,4} (L(\d+)([A-Z]+)) (easy-ui|hard-ui|easy|hard)\. (.+)$", re.M)
TIERS = {"easy": 0, "easy-ui": 1, "hard": 2, "hard-ui": 3}
SHARED = {"AGENTS.md", "lessons.md", "shared_frontend_manifest.json"}
SHARED_PREFIXES = (".github/", "scripts/ci/", "lessons/", "backend/alembic/", "migrations/")  # extend with your repo's shared control paths
SOURCE_TEXT_PROOF = re.compile(r"static dead[- ]owner absence|source[- ]text (?:deleted[- ]name absence|syntax)", re.I)


def letter_number(letters: str) -> int:
    value = 0
    for letter in letters:
        value = value * 26 + ord(letter) - ord("A") + 1
    return value


def check(paths: list[Path]) -> tuple[int, list[str]]:
    errors: list[str] = []
    layers: dict[int, list[tuple[int, str, str]]] = defaultdict(list)
    owners: dict[tuple[int, str], str] = {}
    ids: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        headers = list(HEADER.finditer(text))
        valid_starts = {match.start() for match in headers}
        for candidate in re.finditer(r"^#{2,4} L\d+[A-Z]+\b.*$", text, re.M):
            if candidate.start() not in valid_starts:
                errors.append(f"{path.name}: malformed slice heading {candidate.group(0)}")
        for index, match in enumerate(headers):
            slice_id, layer_text, letters, tier, _ = match.groups()
            layer = int(layer_text)
            end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
            body = text[match.end():end]
            if slice_id in ids:
                errors.append(f"duplicate slice {slice_id}")
            ids.add(slice_id)
            layers[layer].append((letter_number(letters), tier, slice_id))
            for label in ("Owns", "Forbidden", "Depends", "Done when"):
                if not re.search(rf"^{label}:[ \t]*\S", body, re.M):
                    errors.append(f"{slice_id}: missing {label}")
            done = re.search(r"^Done when:[ \t]*(.+)$", body, re.M)
            if done and SOURCE_TEXT_PROOF.search(done.group(1)):
                errors.append(f"{slice_id}: source-text deletion/syntax is not behavior proof; follow AGENTS test policy")
            owns_line = re.search(r"^Owns:[ \t]*(.+)$", body, re.M)
            files = re.findall(r"`([^`]+)`", owns_line.group(1)) if owns_line else []
            if not files:
                errors.append(f"{slice_id}: Owns needs exact backticked paths")
            for file in files:
                if Path(file).is_dir():
                    errors.append(f"{slice_id}: directory ownership {file}")
                if "*" in file or "?" in file:
                    errors.append(f"{slice_id}: ownership glob {file}")
                if file in SHARED or file.startswith(SHARED_PREFIXES) or Path(file).name in {"Cargo.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock", "shared_frontend_manifest.json"}:
                    errors.append(f"{slice_id}: parent-controlled path {file}")
                if PurePosixPath(file).is_absolute() or str(PurePosixPath(file)) != file or ".." in PurePosixPath(file).parts:
                    errors.append(f"{slice_id}: noncanonical owner path {file}")
                    continue
                for (other_layer, other_file), other_id in owners.items():
                    if layer == other_layer and (file.startswith(other_file + "/") or other_file.startswith(file + "/")):
                        errors.append(f"{slice_id} has ancestor ownership overlap with {other_id}: {file}, {other_file}")
                key = layer, file
                if key in owners:
                    errors.append(f"{slice_id} overlaps {owners[key]}: {file}")
                owners[key] = slice_id
            depends = re.search(r"^Depends:[ \t]*(.+)$", body, re.M)
            if depends and re.search(rf"\bL{layer}[A-Z]+\b", depends.group(1)):
                errors.append(f"{slice_id}: same-layer dependency")
    for layer, rows in sorted(layers.items()):
        if rows != sorted(rows):
            errors.append(f"L{layer}: slice letters are not in order")
        if [TIERS[tier] for _, tier, _ in rows] != sorted(TIERS[tier] for _, tier, _ in rows):
            errors.append(f"L{layer}: tiers must form easy, easy-ui, hard, hard-ui blocks")
    if not ids:
        errors.append("no slice contracts found")
    return len(ids), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parts", nargs="+", type=Path)
    args = parser.parse_args()
    count, errors = check(args.parts)
    for error in errors:
        print(error)
    print(f"{count} slices; {len(errors)} errors")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
