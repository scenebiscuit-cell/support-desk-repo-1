"""Load macros, pick the right one, and fill in placeholders."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def load_macros(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(macros: list[dict]) -> dict[str, dict]:
    return {m["id"]: m for m in macros}


def choose_macro(category: str, text: str, churn_risk: bool) -> str:
    """Pick a macro id from the category plus a few telling words."""
    t = text.lower()
    if category == "refund":
        if "annual" in t or "year" in t:
            return "M02"
        if any(w in t for w in ("twice", "duplicate", "double charge", "charged me", "charged us", "wrong plan")):
            return "M01"
        return "M03"
    if category == "cancellation":
        # Someone relaying the owner's request can't cancel themselves: explain the owner path.
        if "owner" in t or not churn_risk:
            return "M04"
        return "M05"
    if category == "workspace_setup":
        return "M08" if any(w in t for w in ("time zone", "timezone", "day early", "day earlier", "due date")) else "M09"
    if category == "account_access":
        return "M12" if any(w in t for w in ("2fa", "code", "phone", "two-factor", "authenticator")) else "M11"
    if category == "seats":
        return "M14" if "owner" in t else "M13"
    if category == "data_privacy":
        return "M16" if "export" in t and "delet" not in t else "M15"
    return {
        "billing": "M22", "integrations": "M06", "notifications": "M07", "bug": "M10",
        "outage": "M17", "security": "M18", "feature_request": "M19", "presales": "M20",
        "feedback": "M21", "spam": "M23",
    }.get(category, "M09")


def fill(body: str, values: dict[str, str]) -> tuple[str, list[str]]:
    """Replace {{placeholders}}. Unknown ones become [[fill in: name]] for a human to finish."""
    missing: list[str] = []

    def sub(m: re.Match) -> str:
        key = m.group(1)
        if values.get(key):
            return values[key]
        missing.append(key)
        return f"[[fill in: {key.replace('_', ' ')}]]"

    return PLACEHOLDER.sub(sub, body), missing


def export_csv(macros: list[dict], path: Path) -> None:
    """Flat CSV that pastes cleanly into most helpdesks' saved-reply importers or a spreadsheet."""
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "category", "tags", "set_priority", "set_status", "internal_note", "body"])
        for m in macros:
            a = m.get("actions", {})
            w.writerow([m["id"], m["title"], m["category"], " ".join(a.get("tags", [])),
                        a.get("priority", ""), a.get("status", ""), m.get("internal_note", ""), m["body"]])


def export_markdown(macros: list[dict], path: Path) -> None:
    lines = ["# Pharos macro library", "",
             f"{len(macros)} macros. Placeholders look like `{{{{customer_first_name}}}}`.", ""]
    for m in macros:
        a = m.get("actions", {})
        lines += [f"## {m['id']} · {m['title']}", "",
                  f"**Category:** {m['category']}  ·  **Tags:** {', '.join(a.get('tags', []))}  ·  "
                  f"**Sets priority:** {a.get('priority', '-')}  ·  **Sets status:** {a.get('status', '-')}", ""]
        if m.get("internal_note"):
            lines += [f"> Internal note: {m['internal_note']}", ""]
        lines += ["```", m["body"] or "(no reply sent)", "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
