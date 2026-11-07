"""Integrity and isolation of the immutable Git preservation-fixture reader."""
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import git_fixtures as fixtures

BASE = 'cf443c3b1facc2ae422fc6c55d546528671be1d0'


class GitFixtureTests(unittest.TestCase):
    def tearDown(self):
        fixtures.close_readers()

    def test_real_git_blobs_match_git_show_with_one_reused_process(self):
        first_process = None
        for relative in ['index.html', 'assets/consent.js', 'TOOL_REGISTRY.json']:
            expected = subprocess.check_output(['git', 'show', BASE + ':' + relative], cwd=ROOT)
            self.assertEqual(fixtures.git_blob(ROOT, BASE, relative), expected)
            process = fixtures._READERS[ROOT.resolve()]._process
            if first_process is None:
                first_process = process
            self.assertIs(process, first_process)

    def test_unsafe_paths_and_mutable_or_abbreviated_revisions_are_rejected(self):
        reader = fixtures.GitBlobReader(ROOT)
        self.addCleanup(reader.close)
        for relative in ['../index.html', '/index.html', 'C:/outside', 'assets\\consent.js', 'index.html\nHEAD:index.html', 'a/./b', '%2e%2e/file', 'a\0b']:
            with self.subTest(path=relative), self.assertRaises(ValueError):
                reader.read(BASE, relative)
        for revision in ['HEAD', 'main', BASE[:8], BASE + '\n', BASE.upper(), '0' * 64]:
            with self.subTest(revision=revision), self.assertRaises(ValueError):
                reader.read(revision, 'index.html')
        self.assertEqual(reader.read(BASE, 'CNAME'), subprocess.check_output(['git', 'show', BASE + ':CNAME'], cwd=ROOT))

    def test_missing_blob_closes_process_and_next_call_recovers(self):
        with self.assertRaises(ValueError):
            fixtures.git_blob(ROOT, BASE, 'nonexistent-fixture-file')
        old = fixtures._READERS[ROOT.resolve()]
        self.assertTrue(old._closed)
        self.assertIsNotNone(old._process.poll())
        self.assertEqual(fixtures.git_blob(ROOT, BASE, 'CNAME'), subprocess.check_output(['git', 'show', BASE + ':CNAME'], cwd=ROOT))
        self.assertIsNot(fixtures._READERS[ROOT.resolve()], old)

    def test_repository_root_is_bound_and_subdirectory_is_not_a_root(self):
        with self.assertRaises(ValueError):
            fixtures.GitBlobReader(ROOT / 'scripts')

    def test_committed_bytes_are_independent_of_later_working_tree_changes(self):
        with tempfile.TemporaryDirectory(prefix='edb-git-fixture-') as temporary:
            root = Path(temporary).resolve()
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
            original = b'committed\r\n\x00binary bytes\n'
            (root / 'fixture.bin').write_bytes(original)
            subprocess.run(['git', '-C', str(root), 'add', 'fixture.bin'], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--quiet', '-m', 'fixture'], check=True, capture_output=True)
            revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            self.assertEqual(fixtures.git_blob(root, revision, 'fixture.bin'), original)
            (root / 'fixture.bin').write_bytes(b'changed working file')
            self.assertEqual(fixtures.git_blob(root, revision, 'fixture.bin'), original)
            fixtures.close_readers()

    def test_batch_records_reject_wrong_identity_type_length_and_framing(self):
        raw = b'hello\x00world\r\n'
        identity = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest().encode()
        valid = identity + b' blob ' + str(len(raw)).encode() + b'\n' + raw + b'\n'
        self.assertEqual(fixtures._record(io.BytesIO(valid), 'sha1'), raw)
        cases = [valid.replace(identity, b'0' * 40, 1), valid.replace(b' blob ', b' tree ', 1),
                 valid.replace(b' blob 13\n', b' blob 14\n', 1), valid[:-2], valid[:-1] + b'X',
                 identity + b' blob 67108865\n', b'HEAD:missing missing\n', b'x' * 2049 + b'\n']
        for record in cases:
            with self.subTest(record=record[:70]), self.assertRaises(ValueError):
                fixtures._record(io.BytesIO(record), 'sha1')

    def test_sha256_git_object_identity_is_verified(self):
        raw = b'exact bytes'
        identity = hashlib.sha256(b'blob 11\0' + raw).hexdigest().encode()
        record = identity + b' blob 11\n' + raw + b'\n'
        self.assertEqual(fixtures._record(io.BytesIO(record), 'sha256'), raw)
        with self.assertRaises(ValueError):
            fixtures._record(io.BytesIO(record), 'sha1')

    def test_unresponsive_process_has_a_bounded_failure_and_shutdown(self):
        process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(10)'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        with patch.object(fixtures, '_spawn', return_value=process):
            reader = fixtures.GitBlobReader(ROOT, response_timeout=0.05)
        self.addCleanup(reader.close)
        with self.assertRaises(ValueError):
            reader.read(BASE, 'index.html')
        self.assertTrue(reader._closed)
        self.assertIsNotNone(process.poll())
        reader.close()


if __name__ == '__main__':
    unittest.main()
