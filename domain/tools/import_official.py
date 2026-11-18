"""把手工保存的官方 wiki HTML 解析成结构化 JSON。

官方 wiki 是 MediaWiki（`mw-content-text` + `mw-parser-output` + `wikitable`）。
输入：domain/kb/manual/**/*.html（浏览器「网页，仅 HTML」保存的页面）
输出：domain/kb/raw_official/<category>/<slug>.json
   {
     "page": ..., "title": ..., "category": ..., "slug": ...,
     "version": "0.6.2.6:260903-1430",
     "entities": [{"name":..., "section":..., "fields": {...}}],
     "sections": [{"heading": "A › B", "kind": ..., "text": ...}]
   }
"""

from __future__ import annotations

import html as html_mod
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
MANUAL = ROOT / "kb" / "manual"
OUT = ROOT / "kb" / "raw_official"

VERSION = "0.6.2.6:260903-1430"

SKIP_TAGS = {"script", "style", "sup", "noscript"}
SKIP_CLASSES = {"mw-editsection", "navbox", "toc", "mw-jump-link", "noprint", "printfooter"}

ENTITY_PAGES = {
    "Components": "component",
    "Munitions & Missiles": "munition",
    "Ships": "hull",
    "Spacecraft": "craft",
    "Factions": "faction",
    "List of Maps": "map",
}

SECTION_PAGES = {
    "Armor": "mechanics", "Crew": "mechanics", "Component Damage": "mechanics",
    "Damage Control": "mechanics", "Electronic Warfare": "mechanics",
    "Intelligence": "mechanics", "Movement": "mechanics", "Radar": "mechanics",
    "Beginner's Guide": "guide", "Starter Fleet Guides": "guide",
    "Campaign Comprehensive Guide": "guide", "Ship Building Megaguide": "guide",
    "Missile Defense": "guide",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii") or text
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80] or "page"


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class WikiParser(HTMLParser):
    """把 MediaWiki 正文切成 heading / p / li / table 块。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.in_content = False
        self.skip_depth = 0
        self.blocks: list[dict] = []
        self.stack: list[str] = []
        self.buf: list[str] = []
        self.buf_kind: str | None = None
        self.heading_level = 0
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None
        # Faction-specific parts carry a faction roundel image in the name cell.
        self.cell_imgs: list[str] | None = None
        self.row_imgs: list[list[str]] = []
        self.table_imgs: list[list[list[str]]] = []

    # -- helpers -------------------------------------------------------
    def _flush(self) -> None:
        text = clean("".join(self.buf))
        kind, self.buf_kind = self.buf_kind, None
        self.buf = []
        if not text or kind is None:
            return
        if kind == "heading":
            self.blocks.append({"kind": "heading", "level": self.heading_level, "text": text})
        elif kind == "li":
            self.blocks.append({"kind": "li", "depth": self.stack.count("li"), "text": text})
        else:
            self.blocks.append({"kind": kind, "text": text})

    def _flush_cell(self) -> None:
        if self.cell is not None and self.row is not None:
            self.row.append(clean("".join(self.cell)))
            self.row_imgs.append(self.cell_imgs or [])
        self.cell = None
        self.cell_imgs = None

    def _classy_skip(self, attrs) -> bool:
        for key, value in attrs:
            if key == "class" and value:
                for token in value.split():
                    if token in SKIP_CLASSES:
                        return True
            if key == "id" and value in {"toc", "mw-toc-heading"}:
                return True
        return False

    # -- HTMLParser hooks ----------------------------------------------
    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "div" and attrs_d.get("id") == "mw-content-text":
            self.in_content = True
        if not self.in_content:
            return
        if self._classy_skip(attrs):
            self.skip_depth += 1
            return
        if self.skip_depth:
            return

        if tag in ("h2", "h3", "h4"):
            self._flush()
            self.heading_level = int(tag[1])
            self.buf_kind = "heading"
        elif tag == "p":
            self._flush()
            self.buf_kind = "p"
        elif tag == "li":
            self._flush()
            self.stack.append("li")
            self.buf_kind = "li"
        elif tag in ("dd", "dt"):
            self._flush()
            self.buf_kind = "li"
        elif tag == "table":
            self._flush()
            self.table = []
            self.table_imgs = []
        elif tag == "tr" and self.table is not None:
            self._flush_cell()
            self.row = []
            self.row_imgs = []
        elif tag in ("td", "th") and self.row is not None:
            self._flush_cell()
            self.cell = []
            self.cell_imgs = []
        elif tag == "img" and self.cell_imgs is not None:
            src = attrs_d.get("src") or ""
            name = src.rsplit("/", 1)[-1]
            if name:
                self.cell_imgs.append(name)
        elif tag == "br":
            if self.cell is not None:
                self.cell.append(" ")
            elif self.buf_kind:
                self.buf.append(" ")

    def handle_endtag(self, tag):
        if not self.in_content:
            return
        if tag in SKIP_TAGS and self.skip_depth == 0:
            return
        if self.skip_depth:
            if tag == "div":
                self.skip_depth -= 1
            return
        if tag in ("h2", "h3", "h4"):
            self._flush()
        elif tag == "p":
            self._flush()
        elif tag == "li":
            self._flush()
            if self.stack and self.stack[-1] == "li":
                self.stack.pop()
        elif tag in ("dd", "dt"):
            self._flush()
        elif tag in ("td", "th"):
            self._flush_cell()
        elif tag == "tr" and self.table is not None and self.row is not None:
            self._flush_cell()
            if any(c for c in self.row):
                self.table.append(self.row)
                self.table_imgs.append(self.row_imgs)
            self.row = None
            self.row_imgs = []
        elif tag == "table" and self.table is not None:
            self._flush()
            if self.table:
                self.blocks.append({"kind": "table", "rows": self.table,
                                    "imgs": self.table_imgs})
            self.table = None
            self.table_imgs = []

    def handle_data(self, data):
        if not self.in_content or self.skip_depth:
            return
        if self.cell is not None:
            self.cell.append(data)
        elif self.buf_kind:
            self.buf.append(data)


def page_title(t: str) -> str:
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if not m:
        return "Untitled"
    return clean(html_mod.unescape(m.group(1)).split(" - ")[0])


def parse_file(path: Path) -> dict:
    t = path.read_text(encoding="utf-8", errors="replace")
    parser = WikiParser()
    parser.feed(t)
    parser.close()
    return {"page": path.stem, "title": page_title(t), "blocks": parser.blocks}


def split_sections(blocks: list[dict]) -> list[dict]:
    """按 h2/h3 切段；返回 [{heading, blocks}]。"""
    out: list[dict] = []
    chain: list[tuple[int, str]] = []
    current = {"heading": "(页面开头)", "blocks": []}
    for blk in blocks:
        if blk["kind"] == "heading":
            level = blk["level"]
            while chain and chain[-1][0] >= level:
                chain.pop()
            chain.append((level, blk["text"]))
            if out or current["blocks"]:
                out.append(current)
            current = {"heading": " › ".join(x[1] for x in chain), "blocks": []}
        else:
            current["blocks"].append(blk)
    if current["blocks"]:
        out.append(current)
    return out


NAME_COLUMNS = {
    "mount", "compartment", "module", "hull", "ship", "name", "munition", "missile",
    "weapon",
    "missile body", "payload", "avionics package", "seeker", "auxiliary",
    "mine body", "bomb body", "rocket body", "decoy body", "shell classification",
}
SKIP_HEADINGS = ("Posture controls", "Guidelines")
# 弹药表：第一列是弹种，需要拿章节里的口径做前缀（"Ballistic › 100mm" → "100mm "）
CALIBER_RE = re.compile(r"^(?:Ballistic|Energy Weapons|Point Defense)\s*›\s*(\d+\s*mm)", re.I)

# 官方 wiki 用「名字后面的阵营徽记 PNG」表示该部件只属于这个阵营；
# 两个徽记表示两阵营通用，没有徽记表示页面上没标。
ROUNDEL_FACTION = {
    "Alliance_Roundel.png": "Shelter Alliance (SA)",
    "OSP_Roundel.png": "Outlying Systems Protectorate (OSP)",
}


def roundel_factions(table_imgs: list[list[list[str]]], row_index: int) -> str:
    """Read the faction roundels tucked into the name cell of one table row."""
    if row_index >= len(table_imgs):
        return ""
    row = table_imgs[row_index]
    if not row:
        return ""
    found: list[str] = []
    for name in row[0] or []:
        # thumbnails arrive as "25px-Alliance_Roundel.png"
        label = ROUNDEL_FACTION.get(re.sub(r"^\d+px-", "", name))
        if label and label not in found:
            found.append(label)
    return "; ".join(found)


def build_entities(page: str, sections: list[dict]) -> tuple[list[dict], list[dict]]:
    """返回 (实体列表, 表格体检表)。体检表用于核对"页面上有几行、实际抽了几个"。"""
    entities: list[dict] = []
    audit: list[dict] = []
    for sec in sections:
        if sec["heading"].startswith(SKIP_HEADINGS):
            continue
        m = CALIBER_RE.match(sec["heading"])
        caliber = m.group(1) if m else ""
        for blk in sec["blocks"]:
            if blk["kind"] != "table":
                continue
            rows = blk["rows"]
            if len(rows) < 2:
                continue
            headers = rows[0]
            first = headers[0].strip().lower() if headers else ""
            if first not in NAME_COLUMNS:
                audit.append({"section": sec["heading"], "header": rows[0][0] if rows[0] else "",
                              "rows": len(rows) - 1, "used": 0, "unused": []})
                continue
            blk["entity_table"] = True
            used = 0
            unused: list[str] = []
            table_imgs = blk.get("imgs") or []
            for row_index, row in enumerate(rows[1:], start=1):
                if not row or not row[0]:
                    unused.append("(空)")
                    continue
                name = row[0].strip()
                if first == "shell classification" and caliber and "mm" not in name.lower():
                    name = f"{caliber} {name}"
                if first == "ship":
                    # "Ship | Type | …" tables list a hull's built-in parts; the part
                    # name is <hull> <type> ("Sprinter Main"), not the hull alone.
                    part_type = row[1].strip() if len(row) > 1 else ""
                    if part_type:
                        name = f"{name} {part_type}"
                fields = {}
                for i, head in enumerate(headers):
                    value = row[i] if i < len(row) else ""
                    if value:
                        fields[head.strip()] = value
                faction = roundel_factions(table_imgs, row_index)
                if faction:
                    fields["Faction (wiki logo)"] = faction
                entities.append({"name": name, "section": sec["heading"], "fields": fields})
                used += 1
            audit.append({"section": sec["heading"], "header": rows[0][0],
                          "rows": len(rows) - 1, "used": used, "unused": unused})
    return entities, audit


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    total_files = 0
    total_entities = 0
    for path in sorted(MANUAL.rglob("*.html")):
        parsed = parse_file(path)
        page = parsed["title"]
        category = ENTITY_PAGES.get(page) or SECTION_PAGES.get(page) or "other"
        sections = split_sections(parsed["blocks"])
        if page in ENTITY_PAGES:
            entities, audit = build_entities(page, sections)
        else:
            entities, audit = [], []
        record = {
            "page": parsed["page"],
            "title": page,
            "category": category,
            "slug": slugify(page),
            "version": VERSION,
            "source": "官方 wiki（wiki.hoodedhorse.com）",
            "entities": entities,
            "tables": audit,
            "sections": [
                {"heading": s["heading"], "blocks": s["blocks"]}
                for s in sections
            ],
        }
        out_dir = OUT / category
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{record['slug']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        total_files += 1
        total_entities += len(entities)
        print(f"  {category:9s} {len(entities):3d} 实体  {page}")
    print(f"共 {total_files} 页，{total_entities} 个实体 → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
