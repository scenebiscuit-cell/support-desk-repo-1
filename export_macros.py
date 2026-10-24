#!/usr/bin/env python3
"""Export macros/macros.json to macros.csv (for helpdesk import or a spreadsheet)
and macros.md (a readable library to share with a client)."""
from pathlib import Path

from support_ops.macros import export_csv, export_markdown, load_macros

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    macros = load_macros(ROOT / "macros" / "macros.json")
    export_csv(macros, ROOT / "macros" / "macros.csv")
    export_markdown(macros, ROOT / "macros" / "macros.md")
    print(f"Exported {len(macros)} macros to macros/macros.csv and macros/macros.md")
