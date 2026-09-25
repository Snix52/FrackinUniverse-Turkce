"""Load original game assets explicitly shipped alongside translation patches."""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath


def load_custom_assets(tools: Path) -> dict[str, bytes]:
    manifest = tools / 'custom_assets.json'
    root = tools / 'custom_assets'
    if not manifest.is_file():
        if root.exists():
            raise ValueError('Custom assets exist without a manifest')
        return {}

    specs = json.loads(manifest.read_text(encoding='utf-8'))['assets']
    if not isinstance(specs, list) or not specs or len(specs) != len(set(specs)):
        raise ValueError('Invalid custom asset inventory')
    files = {}
    for name in specs:
        if (not isinstance(name, str) or not name or '\\' in name
                or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts):
            raise ValueError('Unsafe custom asset path: ' + repr(name))
        source = root.joinpath(*PurePosixPath(name).parts)
        if not source.is_file() or source.is_symlink():
            raise ValueError('Missing or symlinked custom asset: ' + name)
        files[name] = source.read_bytes()
    discovered = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if discovered != set(files):
        raise ValueError('Unlisted custom assets: ' + repr(sorted(discovered - set(files))))
    return files
