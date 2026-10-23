#!/usr/bin/env python3
"""Keep the stable BookshelfNG container aliases on one release build."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/build.yml"
ALIASES = ("hardcover", "main", "master", "latest", "stable")
STABLE_CONDITION = "${{ github.ref_type == 'tag' }}"
RELEASE_GATE = (
    "github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v') "
    "&& vars.BOOKSHELFNG_RELEASE_READY == 'true'"
)


class ConfigurationError(RuntimeError):
    pass


def action_block(source: str, step_id: str) -> str:
    marker = re.search(
        rf"^\s+id:\s*{re.escape(step_id)}\s*$", source, re.MULTILINE
    )
    if marker is None:
        raise ConfigurationError(f"Missing workflow step id: {step_id}")

    next_step = re.search(r"^ {6}- uses:", source[marker.end() :], re.MULTILINE)
    end = marker.end() + next_step.start() if next_step else len(source)
    return source[marker.start() : end]


def job_block(source: str, job_id: str) -> str:
    marker = re.search(rf"^  {re.escape(job_id)}:\s*$", source, re.MULTILINE)
    if marker is None:
        raise ConfigurationError(f"Missing workflow job: {job_id}")

    next_job = re.search(r"^  [A-Za-z0-9_-]+:\s*$", source[marker.end() :], re.MULTILINE)
    end = marker.end() + next_job.start() if next_job else len(source)
    return source[marker.start() : end]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigurationError(message)


def main() -> int:
    source = WORKFLOW.read_text(encoding="utf-8")
    metadata = action_block(source, "hc_meta")
    hardcover_build = action_block(source, "hardcover_image")
    publish_job = job_block(source, "publish-images")

    declared: dict[str, list[str]] = {}
    for tag, condition in re.findall(
        r"^\s*type=raw,value=([a-z0-9-]+),enable=(.+?)\s*$",
        metadata,
        re.MULTILINE,
    ):
        if tag in ALIASES:
            declared.setdefault(tag, []).append(condition)

    for alias in ALIASES:
        require(
            declared.get(alias) == [STABLE_CONDITION],
            f"{alias!r} must be declared exactly once in hc_meta and only for release tags.",
        )

    require(
        "ghcr.io/${{ github.repository }}" in metadata
        and "docker.io/snapetech/bookshelfng" in metadata,
        "Stable aliases must target both GHCR and Docker Hub from the same metadata action.",
    )
    require(
        "tags: ${{ steps.hc_meta.outputs.tags }}" in hardcover_build,
        "Stable aliases must be attached to the same Hardcover image build.",
    )
    require(
        "platforms: \"linux/amd64,linux/arm64\"" in hardcover_build,
        "Stable aliases must remain on the multi-architecture release image.",
    )
    require(
        "IMAGE_FLAVOR=hardcover" in hardcover_build,
        "Stable aliases must refer to the Hardcover image flavor.",
    )
    require(
        RELEASE_GATE in publish_job,
        "Stable image publication must stay limited to approved main release tags.",
    )
    require(
        "bash scripts/verify-stable-container-aliases.sh" in publish_job,
        "The release job must verify published tag digests after pushing the image.",
    )

    print(
        "Stable aliases are grouped on the same approved multi-architecture "
        "Hardcover release: "
        + ", ".join(ALIASES)
        + "."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConfigurationError as error:
        print(f"Stable container alias check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
