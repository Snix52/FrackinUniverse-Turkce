#!/usr/bin/env python3
"""Publish generated files only over the exact source SHA; never rebase or force-push."""
from __future__ import annotations
import argparse
import os
import re
import subprocess
from pathlib import Path

GENERATED_PATHS = ('dist', 'FU_Turkce', 'tools/test_raporu.json', 'tools/GELISTIRME.txt')


def git(repo: Path, *args: str, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, check=check)


def remote_head(repo: Path, remote: str, branch: str) -> str:
    git(repo, 'fetch', remote, branch)
    return git(repo, 'rev-parse', 'FETCH_HEAD').stdout.strip()


def publish(repo: Path, source_sha: str, remote='origin', branch='main') -> str:
    if not re.fullmatch(r'[0-9a-f]{40}', source_sha):
        raise ValueError('A full source/base SHA is required')
    if remote_head(repo, remote, branch) != source_sha:
        return 'SKIP_STALE'
    if git(repo, 'rev-parse', 'HEAD').stdout.strip() != source_sha:
        raise ValueError('Checkout HEAD is not the source/base SHA')
    # A caller must not accidentally include unrelated staged source edits.
    staged = git(repo, 'diff', '--cached', '--name-only', '-z').stdout.split('\0')
    if any(p and not any(p == allowed or p.startswith(allowed + '/') for allowed in GENERATED_PATHS)
           for p in staged):
        raise ValueError('Unrelated staged changes cannot be published')
    paths = [p for p in GENERATED_PATHS if (repo / p).exists()
             or git(repo, 'ls-files', '--', p).stdout.strip()]
    git(repo, 'add', '-A', '--', *paths)
    diff = git(repo, 'diff', '--cached', '--quiet', check=False)
    if diff.returncode == 0:
        return 'SKIP_UNCHANGED'
    if diff.returncode != 1:
        raise RuntimeError(diff.stderr)
    git(repo, 'commit', '-m', 'build: refresh verified package and QA evidence [skip ci]')
    # HEAD now points to the generated commit: compare remote to source_sha, not HEAD.
    if remote_head(repo, remote, branch) != source_sha:
        return 'SKIP_STALE_BEFORE_PUSH'
    result = git(repo, 'push', remote, f'HEAD:refs/heads/{branch}', check=False)
    if result.returncode:
        # Only a demonstrated race is a skip. Auth/network/protection failures stay red.
        if remote_head(repo, remote, branch) != source_sha:
            return 'SKIP_STALE_DURING_PUSH'
        raise RuntimeError('Artifact push failed without a newer source commit: ' + result.stderr)
    generated = git(repo, 'rev-parse', 'HEAD').stdout.strip()
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with Path(summary).open('a', encoding='utf-8') as out:
            out.write(f'\nArtifact publication: **PASS**\n\nSource: `{source_sha}`\n\nGenerated commit: `{generated}`\n')
    return 'PUBLISHED'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--remote', default='origin')
    parser.add_argument('--branch', default='main')
    args = parser.parse_args()
    print(publish(args.repo.resolve(), args.source_sha, args.remote, args.branch))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
