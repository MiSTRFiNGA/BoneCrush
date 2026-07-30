"""Bone Crush packaging QA — run from D:\\Dev\\BoneCrush after build.py.

Checks:
  - dist zips exist
  - CrazyGames size gates (Basic <= 50 MB, mobile homepage <= 20 MB)
  - file count <= 1500
  - PLATFORM_SDK / PSDK adapter injected before game body
  - relative paths only in zip namelist
"""
from __future__ import annotations

import os
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MB = 1024 * 1024


class TestBoneCrushPackaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cg = DIST / "bonecrush-crazygames.zip"
        cls.poki = DIST / "bonecrush-poki.zip"
        if not cls.cg.is_file() or not cls.poki.is_file():
            raise unittest.SkipTest("dist zips missing — run python build.py first")

    def _zip_info(self, path: Path):
        size = path.stat().st_size
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            html = zf.read("index.html").decode("utf-8", errors="replace")
        return size, names, html

    def test_cg_size_and_filecount(self):
        size, names, _ = self._zip_info(self.cg)
        print(f"CG zip: {size} bytes ({size/MB:.2f} MB), {len(names)} files")
        self.assertLessEqual(size, 50 * MB, "Basic Launch 50 MB gate")
        self.assertLessEqual(size, 20 * MB, "mobile homepage 20 MB gate")
        self.assertLessEqual(len(names), 1500)
        self.assertIn("index.html", names)

    def test_poki_size_and_filecount(self):
        size, names, _ = self._zip_info(self.poki)
        print(f"Poki zip: {size} bytes ({size/MB:.2f} MB), {len(names)} files")
        self.assertLessEqual(size, 50 * MB)
        self.assertLessEqual(len(names), 1500)
        self.assertIn("index.html", names)

    def test_cg_psdk_injected_before_game(self):
        _, _, html = self._zip_info(self.cg)
        self.assertNotIn("<!-- PLATFORM_SDK -->", html, "marker should be replaced")
        self.assertIn("CrazyGames", html)
        self.assertIn("window.PSDK", html)
        # adapter must appear before typical game bootstrap markers
        psdk_at = html.find("window.PSDK")
        self.assertGreaterEqual(psdk_at, 0)
        # game canvas / main script body usually after head injection
        body_at = html.lower().find("<body")
        if body_at >= 0:
            self.assertLess(psdk_at, body_at + 5000, "PSDK should be early in document")

    def test_poki_psdk_injected(self):
        _, _, html = self._zip_info(self.poki)
        self.assertNotIn("<!-- PLATFORM_SDK -->", html)
        self.assertIn("PokiSDK", html)
        self.assertIn("window.PSDK", html)

    def test_relative_paths_only(self):
        for path in (self.cg, self.poki):
            with zipfile.ZipFile(path, "r") as zf:
                for n in zf.namelist():
                    self.assertFalse(n.startswith("/") or n.startswith("\\"), n)
                    self.assertNotIn("..", n.split("/"))
                    if len(n) >= 2:
                        self.assertFalse(n[1] == ":", f"absolute/drive path: {n}")


if __name__ == "__main__":
    os.chdir(ROOT)
    unittest.main(verbosity=2)
