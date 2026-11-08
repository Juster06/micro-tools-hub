"""Exact immutable Git blobs for preservation tests, without per-file processes.

This is test tooling, not working-tree approval. Each request names a full
commit identity and a safe path. A bounded cat-file process remains tied to
one canonical repository; every returned blob is framed and hashed anew.
"""
from __future__ import annotations

import atexit
import hashlib
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import threading

MAX_BLOB_BYTES = 64 * 1024 * 1024
MAX_HEADER_BYTES = 2048
RESPONSE_TIMEOUT = 10
_READERS = {}
_READERS_LOCK = threading.RLock()


def _relative_path(relative):
    if (not isinstance(relative, str) or len(relative) > 1024
            or not re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*', relative)
            or any(part in {'.', '..'} for part in relative.split('/'))):
        raise ValueError('Unsafe Git fixture path: ' + str(relative))
    return relative


def _record(stream, object_format):
    """Parse the actual binary batch protocol and verify the Git object ID."""
    lengths = {'sha1': 40, 'sha256': 64}
    if object_format not in lengths:
        raise ValueError('Unsupported Git object format')
    header = stream.readline(MAX_HEADER_BYTES + 1)
    match = re.fullmatch(rb'([0-9a-f]+) blob (0|[1-9][0-9]*)\n', header)
    if not match or len(header) > MAX_HEADER_BYTES or len(match[1]) != lengths[object_format]:
        raise ValueError('Missing Git blob or invalid batch record header')
    size = int(match[2])
    if size > MAX_BLOB_BYTES:
        raise ValueError('Git fixture blob exceeds the bounded reader size')
    data = stream.read(size)
    if len(data) != size or stream.read(1) != b'\n':
        raise ValueError('Truncated Git blob or invalid batch record framing')
    actual = hashlib.new(object_format, b'blob ' + str(size).encode('ascii') + b'\0' + data).hexdigest()
    if actual.encode('ascii') != match[1]:
        raise ValueError('Git fixture blob does not match its object identity')
    return data


def _spawn(root):
    return subprocess.Popen(
        ['git', '--no-replace-objects', '-C', str(root), 'cat-file', '--batch'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_REPLACE_OBJECTS': '1'},
    )


class GitBlobReader:
    """A single repository-bound reader; a failed response closes its process."""

    def __init__(self, root, *, response_timeout=RESPONSE_TIMEOUT):
        if not isinstance(response_timeout, (float, int)) or not 0 < response_timeout <= 30:
            raise ValueError('Git fixture response timeout must be bounded')
        self.root = Path(root).resolve(strict=True)
        probe = subprocess.run(
            ['git', '-C', str(self.root), 'rev-parse', '--show-toplevel', '--show-object-format'],
            capture_output=True, timeout=RESPONSE_TIMEOUT, check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        ).stdout.decode('utf-8').splitlines()
        if len(probe) != 2 or Path(probe[0]).resolve(strict=True) != self.root:
            raise ValueError('Git fixture root must be the canonical repository root')
        self.object_format = probe[1]
        if self.object_format not in {'sha1', 'sha256'}:
            raise ValueError('Unsupported Git object format')
        self.response_timeout = response_timeout
        self._lock = threading.RLock()
        self._responses = queue.Queue()
        self._process = _spawn(self.root)
        self._closed = False
        self._thread = threading.Thread(target=self._read_responses, name='git-fixture-reader', daemon=True)
        self._thread.start()

    def _read_responses(self):
        while True:
            try:
                self._responses.put(_record(self._process.stdout, self.object_format))
            except (OSError, ValueError) as error:
                self._responses.put(error)
                return

    def read(self, revision, relative):
        relative = _relative_path(relative)
        digits = 40 if self.object_format == 'sha1' else 64
        if not isinstance(revision, str) or not re.fullmatch('[0-9a-f]{' + str(digits) + '}', revision):
            raise ValueError('Git fixtures require an exact full revision identity')
        with self._lock:
            if self._closed:
                raise ValueError('Git fixture reader is closed')
            try:
                self._process.stdin.write((revision + ':' + relative + '\n').encode('ascii'))
                self._process.stdin.flush()
                response = self._responses.get(timeout=self.response_timeout)
                if isinstance(response, Exception):
                    raise response
                return response
            except (OSError, ValueError, queue.Empty) as error:
                self.close()
                raise ValueError('Git fixture read failed for ' + relative + ': ' + str(error)) from error

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True
            try:
                self._process.stdin.close()
                self._process.wait(timeout=0.5)
            except (OSError, subprocess.TimeoutExpired):
                self._process.kill()
                self._process.wait(timeout=2)
            finally:
                self._thread.join(timeout=1)
                self._process.stdout.close()


def git_blob(root, revision, relative):
    """Return exact bytes from a full Git revision, never from working files."""
    _relative_path(relative)
    canonical = Path(root).resolve(strict=True)
    with _READERS_LOCK:
        reader = _READERS.get(canonical)
        if reader is None or reader._closed:
            reader = GitBlobReader(canonical)
            _READERS[canonical] = reader
    return reader.read(revision, relative)


def close_readers():
    with _READERS_LOCK:
        for reader in _READERS.values():
            reader.close()
        _READERS.clear()


atexit.register(close_readers)
