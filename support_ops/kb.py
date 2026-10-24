"""Knowledge base loading and search.

Help-center articles are markdown files with a small front-matter block.
Each article is split into chunks at its "## " headings, and chunks are
ranked with BM25 (the same scoring idea search engines use). No vector
database or embeddings needed, which keeps the demo free and easy to run.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

HELP_CENTER_URL = "https://help.pharos.example"

STOPWORDS = set(
    """a an and are as at be but by can could do does for from had has have how i if in into is it its
    me my of on or our so that the their them then there these they this to too was we were what when
    where which who why will with would you your yours im ive id dont cant isnt just like get got please
    hi hello hey thanks thank any some also about all been being am up out over only very more most much
    other than such should need want know""".split()
)

# Map customer words onto the words the docs actually use.
SYNONYMS = {
    "subscription": "plan", "membership": "plan", "tier": "plan",
    "unsubscribe": "cancel", "cancellation": "cancel", "quit": "cancel",
    "money": "refund", "reimburse": "refund", "refunded": "refund",
    "text": "sms", "texts": "sms", "sm": "sms",
    "2fa": "two-factor", "authenticator": "two-factor", "mfa": "two-factor",
    "signin": "login", "logins": "login", "locked": "lock",
    "cost": "price", "pricing": "price", "costs": "price", "expensive": "price",
    "doublebooked": "double", "overlap": "double",
    "employee": "staff", "employees": "staff", "stylist": "staff", "stylists": "staff",
    "worker": "staff", "seat": "staff", "seats": "staff",
    "delete": "delet", "deletion": "delet", "remove": "delet", "erase": "delet",
    "down": "outage", "offline": "outage",
    "timezone": "time-zone",
    "outlook": "calendar", "gcal": "calendar",
    "domain": "domain", "url": "domain", "website": "domain",
}


def stem(word: str) -> str:
    """A tiny suffix stripper. Good enough to match 'reminders' to 'reminder'."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > 4 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


PHRASES = {"how much": "price", "double booked": "double booking", "log in": "login", "sign in": "login",
           "two factor": "two-factor", "time zone": "timezone", "no show": "no-show"}


def tokenize(text: str) -> list[str]:
    text = text.lower()
    for phrase, repl in PHRASES.items():
        text = text.replace(phrase, repl)
    words = re.findall(r"[a-z0-9][a-z0-9\-']*", text)
    out = []
    for w in words:
        w = w.strip("'-").replace("'", "")
        if not w or w in STOPWORDS:
            continue
        w = SYNONYMS.get(w, w)
        out.append(stem(w))
    return out


@dataclass
class Chunk:
    slug: str
    title: str
    heading: str
    text: str
    intro: str = ""  # a short article-level note that applies to every section
    tokens: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"{HELP_CENTER_URL}/{self.slug}"

    def to_dict(self) -> dict:
        return {"slug": self.slug, "title": self.title, "heading": self.heading,
                "text": self.text, "intro": self.intro, "url": self.url}


def parse_front_matter(raw: str) -> tuple[dict, str]:
    meta: dict = {}
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        return meta, body.strip()
    return meta, raw


def load_articles(docs_dir: Path) -> list[dict]:
    articles = []
    for path in sorted(docs_dir.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        articles.append({
            "slug": meta.get("slug", path.stem),
            "title": meta.get("title", path.stem),
            "category": meta.get("category", ""),
            "body": body,
        })
    return articles


def chunk_article(article: dict) -> list[Chunk]:
    chunks = []
    intro_lines: list[str] = []
    heading, lines = None, []

    def flush():
        if heading is None:
            return
        text = "\n".join(lines).strip()
        if text:
            chunks.append(Chunk(article["slug"], article["title"], heading, text))

    for line in article["body"].splitlines():
        if line.startswith("## "):
            flush()
            heading, lines = line[3:].strip(), []
        elif line.startswith("# "):
            continue
        elif heading is None:
            intro_lines.append(line)
        else:
            lines.append(line)
    flush()
    intro = "\n".join(intro_lines).strip()
    if intro and len(intro.split()) < 25:
        # A one-line intro ("Only the owner can cancel") is context every section needs.
        for c in chunks:
            c.intro = intro
    elif intro:
        chunks.insert(0, Chunk(article["slug"], article["title"], "Overview", intro))
    return chunks


class KnowledgeBase:
    """BM25 search over help-center chunks."""

    k1 = 1.4
    b = 0.75

    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        for c in chunks:
            # Title and heading words count extra: they say what the chunk is about.
            c.tokens = tokenize(f"{c.title} {c.heading} {c.heading} {c.intro} {c.text}")
        self.avgdl = sum(len(c.tokens) for c in chunks) / max(len(chunks), 1)
        df: dict[str, int] = {}
        for c in chunks:
            for t in set(c.tokens):
                df[t] = df.get(t, 0) + 1
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    @classmethod
    def from_dir(cls, docs_dir: Path) -> "KnowledgeBase":
        chunks = [c for a in load_articles(docs_dir) for c in chunk_article(a)]
        return cls(chunks)

    def search(self, query: str, k: int = 3) -> list[tuple[Chunk, float, float]]:
        """Return (chunk, bm25_score, coverage) for the top k chunks.

        coverage = share of the query's distinct words found in the chunk.
        Low coverage is the signal that the docs don't answer the question.
        """
        q = tokenize(query)
        if not q:
            return []
        q_set = set(q)
        results = []
        for c in self.chunks:
            tf: dict[str, int] = {}
            for t in c.tokens:
                if t in q_set:
                    tf[t] = tf.get(t, 0) + 1
            if not tf:
                continue
            dl = len(c.tokens)
            score = 0.0
            for t, f in tf.items():
                idf = self.idf.get(t, 0.0)
                score += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            coverage = len(tf) / len(q_set)
            results.append((c, score, coverage))
        results.sort(key=lambda r: r[1], reverse=True)
        return results[:k]

    def export_json(self, path: Path) -> None:
        path.write_text(json.dumps([c.to_dict() for c in self.chunks], indent=2), encoding="utf-8")
