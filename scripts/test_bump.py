"""Tests for bump.py, run against copies of the real formula and cask.

    python3 -m unittest discover -s scripts
"""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import bump

ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.2.0"
TARGETS = [
    "aarch64-apple-darwin",
    "x86_64-apple-darwin",
    "universal-apple-darwin",
    "aarch64-unknown-linux-gnu",
    "x86_64-unknown-linux-gnu",
]


def fake_sha(seed: int) -> str:
    return f"{seed:x}" * 64 if seed < 16 else f"{seed:064x}"


def fake_sums(version: str = VERSION, dmg: bool = True) -> tuple[str, dict[str, str]]:
    names = [f"knode-v{version}-{target}.tar.gz" for target in TARGETS]
    if dmg:
        names.append(f"Knode-{version}.dmg")
    sums = {name: fake_sha(i + 1) for i, name in enumerate(names)}
    return "".join(f"{sha}  {name}\n" for name, sha in sums.items()), sums


class BumpTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir)
        self.formula = self.dir / "knode.rb"
        self.cask = self.dir / "cask.rb"
        shutil.copy(ROOT / "Formula" / "knode.rb", self.formula)
        shutil.copy(ROOT / "Casks" / "knode.rb", self.cask)
        self.sums_file = self.dir / "SHA256SUMS"

    def run_bump(self, version: str = VERSION, dmg: bool = True) -> tuple[int, str, dict[str, str]]:
        text, sums = fake_sums(version, dmg)
        self.sums_file.write_text(text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = bump.main([
                "--version", version, "--sums", str(self.sums_file),
                "--formula", str(self.formula), "--cask", str(self.cask),
            ])
        return code, out.getvalue(), sums

    def test_formula_and_cask(self):
        before_formula = self.formula.read_text()
        code, _, sums = self.run_bump()
        self.assertEqual(code, 0)
        formula = self.formula.read_text()
        self.assertIn(f'version "{VERSION}"', formula)
        for target in ["aarch64-apple-darwin", "x86_64-apple-darwin",
                       "aarch64-unknown-linux-gnu", "x86_64-unknown-linux-gnu"]:
            sha = sums[f"knode-v{VERSION}-{target}.tar.gz"]
            url_at = formula.index(f"-{target}.tar.gz")
            self.assertEqual(formula.index(f'sha256 "{sha}"', url_at),
                             formula.index("sha256", url_at))
        self.assertNotIn("0" * 64, formula)
        self.assertEqual(len(formula.splitlines()), len(before_formula.splitlines()))
        cask = self.cask.read_text()
        self.assertIn(f'version "{VERSION}"', cask)
        self.assertIn(f'sha256 "{sums[f"Knode-{VERSION}.dmg"]}"', cask)

    def test_only_version_and_sha_lines_change(self):
        before = self.formula.read_text().splitlines()
        self.run_bump()
        after = self.formula.read_text().splitlines()
        changed = [b for b, a in zip(before, after) if b != a]
        self.assertEqual(len(changed), 5)
        self.assertTrue(all("version" in line or "sha256" in line for line in changed))

    def test_twice_is_the_same(self):
        self.run_bump()
        first = (self.formula.read_text(), self.cask.read_text())
        self.run_bump()
        self.assertEqual(first, (self.formula.read_text(), self.cask.read_text()))

    def test_no_dmg_leaves_the_cask(self):
        before = self.cask.read_text()
        code, out, _ = self.run_bump(dmg=False)
        self.assertEqual(code, 0)
        self.assertIn("::warning::", out)
        self.assertEqual(self.cask.read_text(), before)
        self.assertIn(f'version "{VERSION}"', self.formula.read_text())

    def test_missing_archive_fails_and_writes_nothing(self):
        before = self.formula.read_text()
        text, _ = fake_sums()
        self.sums_file.write_text("\n".join(l for l in text.splitlines() if "linux" not in l))
        with contextlib.redirect_stderr(io.StringIO()):
            code = bump.main(["--version", VERSION, "--sums", str(self.sums_file),
                              "--formula", str(self.formula), "--cask", str(self.cask)])
        self.assertEqual(code, 1)
        self.assertEqual(self.formula.read_text(), before)

    def test_prerelease_is_refused(self):
        code, out, _ = self.run_bump(version="0.2.0-rc.1")
        self.assertEqual(code, 1)
        self.assertIn("not X.Y.Z", out)

    def test_parse_sums_formats(self):
        sha = "a" * 64
        self.assertEqual(bump.parse_sums(f"{sha}  dist/x.tar.gz\n{sha.upper()} *y.dmg\n\n"),
                         {"x.tar.gz": sha, "y.dmg": sha})
        with self.assertRaises(bump.BumpError):
            bump.parse_sums("not a checksum  x.tar.gz\n")
        with self.assertRaises(bump.BumpError):
            bump.parse_sums("\n")


if __name__ == "__main__":
    unittest.main()
