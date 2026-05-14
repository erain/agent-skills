#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import secrets
import shutil
import subprocess
from os.path import samefile
from datetime import date
from pathlib import Path


DEFAULT_REPO = Path("/home/ubuntu/src/knowledge-pages")
DEFAULT_BASE_URL = "https://knowledge.11tech.xyz"


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def load_json(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a list")
    return data


def save_json(path: Path, data: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def destination(repo: Path, kind: str, visibility: str, slug: str) -> tuple[Path, str]:
    if visibility == "unlisted":
        return repo / "content" / "unlisted" / slug, f"u/{slug}/"
    if kind == "deck":
        return repo / "content" / "public" / "decks" / slug, f"decks/{slug}/"
    return repo / "content" / "public" / "pages" / slug, f"pages/{slug}/"


def upsert_artifact(repo: Path, item: dict[str, object]) -> None:
    manifest_path = repo / "content" / "artifacts.json"
    artifacts = load_json(manifest_path)
    slug = item["slug"]
    visibility = item["visibility"]
    updated = False
    for index, existing in enumerate(artifacts):
        if existing.get("slug") == slug and existing.get("visibility") == visibility:
            artifacts[index] = item
            updated = True
            break
    if not updated:
        artifacts.append(item)
    artifacts.sort(key=lambda entry: str(entry.get("updated", "")), reverse=True)
    save_json(manifest_path, artifacts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish an HTML artifact into knowledge-pages.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--kind", choices=["deck", "page"], default="deck")
    parser.add_argument("--visibility", choices=["public", "unlisted"], default="public")
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    source = args.source.resolve()
    repo = args.repo.resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    if "<!doctype html" not in source.read_text(encoding="utf-8").lower():
        raise ValueError("source must be a complete HTML document")
    if not (repo / ".git").exists():
        raise FileNotFoundError(f"target repo is not a git checkout: {repo}")

    slug = args.slug
    if args.visibility == "unlisted" and slug == "auto":
        slug = secrets.token_hex(10)

    dst, relative_url = destination(repo, args.kind, args.visibility, slug)
    dst.mkdir(parents=True, exist_ok=True)
    target = dst / "index.html"
    if not target.exists() or not samefile(source, target):
        shutil.copy2(source, target)

    item = {
        "title": args.title,
        "slug": slug,
        "kind": args.kind,
        "visibility": args.visibility,
        "summary": args.summary,
        "tags": args.tag,
        "updated": date.today().isoformat(),
    }
    upsert_artifact(repo, item)
    run(["python3", "scripts/build_site.py"], cwd=repo)

    url = f"{args.base_url.rstrip('/')}/{relative_url}"
    print(url)

    if args.commit or args.push:
        run(["git", "add", "content", "scripts", ".github", "README.md", ".gitignore"], cwd=repo)
        status = run(["git", "status", "--short"], cwd=repo)
        if status:
            run(["git", "commit", "-m", f"Publish {args.title}"], cwd=repo)
    if args.push:
        run(["git", "push", "origin", "main"], cwd=repo)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
