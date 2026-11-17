"""Load the pure modules of kedi_kumu without importing Home Assistant."""

import importlib
import sys
import types
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent / "custom_components" / "kedi_kumu"


def load(name: str):
    if "kedi_kumu" not in sys.modules:
        pkg = types.ModuleType("kedi_kumu")
        pkg.__path__ = [str(PKG_DIR)]
        sys.modules["kedi_kumu"] = pkg
    return importlib.import_module(f"kedi_kumu.{name}")
