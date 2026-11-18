"""把知识库里的每一艘「样板船」导出成独立的 `.fleet` 文件。

样板船的来源是 `domain/data/class_templates.json` 里每个舰级的 `samples`（与
`domain/kb/builds/<class>-sample-N.md` 一一对应）。导出时**直接搬运原存档里的 `<Ship>`
节点**，而不是按表格重建 —— 这样 `<ComponentData>`（弹药装载）、`<WeaponGroups>`、
`<SocketMap>`、导弹模板名全部原样保留，拖进游戏就能用。

输出：
  * `sample fleets/<舰级> - <船名>.fleet`
  * `domain/reports/sample-ships.md`（清单：舰级 / 船名 / 舰体 / 点数 / 来源舰队 / 文件）
"""

from __future__ import annotations

import json
import re
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import fleet_templates  # noqa: E402

TEMPLATES = ROOT / "domain" / "data" / "class_templates.json"
OUT_DIR = ROOT / "sample fleets"
REPORT = ROOT / "domain" / "reports" / "sample-ships.md"
MERGE = ROOT / "domain" / "tools" / "merge_fleets.py"

BAD = re.compile(r'[\\/:*?"<>|]')


def safe(text: str) -> str:
    return BAD.sub("-", re.sub(r"\s+", " ", text).strip())


def merge_all() -> list[tuple[str, str, int, float]]:
    """把刚导出的样板船再合成「全样板船」舰队；返回 (文件, 阵营, 船数, 总点数)。"""
    if not MERGE.exists():
        return []
    import subprocess

    subprocess.run([sys.executable, str(MERGE)], check=False)
    out: list[tuple[str, str, int, float]] = []
    for path in sorted((OUT_DIR / "_all").glob("*.fleet")):
        root = ET.parse(path).getroot()
        faction = (root.findtext("FactionKey") or "").replace("Stock/", "")
        ships = len(root.findall("Ships/Ship"))
        points = float(root.findtext("TotalPoints") or 0)
        out.append((f"_all/{path.name}", faction, ships, points))
    return out


def load_picks() -> list[dict]:
    data = json.loads(TEMPLATES.read_text(encoding="utf-8"))
    picks: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for block in data.get("classes") or []:
        if not block.get("rec", True) or not block.get("samples"):
            continue
        cls = block["class"]
        median = block.get("cost_median") or 0.0
        ranked = sorted(block["samples"], key=lambda s: (s["rank"], abs(s["cost"] - median)))[:2]
        for n, s in enumerate(ranked, start=1):
            # 同一个存档文件常有两份（Steam 存档 + other info 导出），按内容去重
            key = (s["ship"], s["hull"], f"{s['cost']:.0f}", s["fleet"])
            if key in seen:
                continue
            seen.add(key)
            picks.append({"class": cls, "n": n, **s})
    return picks


def extract_ship(path: Path, name: str) -> ET.Element | None:
    tree = ET.parse(path)
    for ship in tree.getroot().iter("Ship"):
        node = ship.find("Name")
        if node is not None and (node.text or "").strip() == name:
            return ship
    return None


XSI = "http://www.w3.org/2001/XMLSchema-instance"
XSD = "http://www.w3.org/2001/XMLSchema"
ET.register_namespace("xsi", XSI)
ET.register_namespace("xsd", XSD)


def write_fleet(pick: dict, ship: ET.Element, out: Path) -> None:
    root = ET.Element("Fleet")
    ET.SubElement(root, "Name").text = f"{pick['class']} · {pick['ship']}"
    ET.SubElement(root, "Version").text = "3"
    ET.SubElement(root, "TotalPoints").text = f"{pick['cost']:.0f}"
    faction = ""
    src = Path(pick["path"])
    try:
        old = ET.parse(src).getroot().find("FactionKey")
        faction = (old.text or "").strip() if old is not None else ""
    except OSError:
        pass
    if faction:
        ET.SubElement(root, "FactionKey").text = faction
    ET.SubElement(root, "Description").text = (
        f"样板船：{pick['ship']}（{pick['fleet']}），舰体 {pick['hull']}，"
        f"原存档点数 {pick['cost']:.0f}。来自 {src.name}，未做任何改动。"
    )
    ships = ET.SubElement(root, "Ships")
    ships.append(ship)
    # 单船舰队里这艘船就是编队向导：`<InitialFormation><GuideKey>` 必须指向它自己，
    # 否则游戏报 `Fleet is missing guide with GUID …`，那艘船「start independently」。
    key_node = ship.find("Key")
    if key_node is not None:
        key_node.text = self_key = str(uuid.uuid4())
        guide = ship.find("InitialFormation/GuideKey")
        if guide is not None:
            guide.text = self_key
    # 导弹 / 舰载机模板库：发射器和机库按 `$MODMIS$/SGM-100 ARM`、`$CRAFT$/B-45 Sturgeon`
    # 这样的键去舰队根节点的库里取模板，不搬过去导弹和飞机就全是空的。
    pool = fleet_templates.gather([src])
    fleet_templates.emit(root, pool)
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    # 游戏存档的根节点声明了 xsd/xsi 两个命名空间前缀；ElementTree 只有在真正用到时才写，
    # 所以手工补进根标签（注意只能补一次，否则 XML 解析报 duplicate attribute）。
    body = body.replace(
        "<Fleet>", f'<Fleet xmlns:xsd="{XSD}" xmlns:xsi="{XSI}">', 1
    )
    out.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body, encoding="utf-8")


def main() -> int:
    picks = load_picks()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    used: dict[str, int] = {}
    rows: list[str] = []
    written = 0
    for pick in picks:
        src = Path(pick["path"])
        if not src.exists():
            rows.append(f"| {pick['class']} | {pick['ship']} | ⚠ 源文件不存在 | — | — | — |")
            continue
        ship = extract_ship(src, pick["ship"])
        if ship is None:
            rows.append(f"| {pick['class']} | {pick['ship']} | ⚠ 存档里找不到这艘船 | — | — | — |")
            continue
        stem = f"{safe(pick['class'])} - {safe(pick['ship'])}"
        if stem in used:
            # 不同舰队里有同名船：第二个起加来源后缀，避免互相覆盖
            used[stem] += 1
            stem = f"{stem}（{safe(pick['fleet'])}）"
        else:
            used[stem] = 1
        out = OUT_DIR / f"{stem}.fleet"
        write_fleet(pick, ship, out)
        written += 1
        # 船名里可能有 `|`（存档里真有这种名字），markdown 表格里换成全角竖线
        shown = pick["ship"].replace("|", "｜")
        shown_file = out.name.replace("|", "｜")
        rows.append(
            f"| {pick['class']} | {shown} | {pick['hull']} | {pick['cost']:.0f} | "
            f"{pick['fleet']} | `{shown_file}` |"
        )

    lines = [
        "# 样板船清单（每艘一个 `.fleet`）",
        "",
        f"共 **{written}** 艘，文件在 `sample fleets/`（与 `domain/kb/builds/<舰级>-sample-N.md` 一一对应："
        "同一艘船的表格页和 `.fleet` 是同一份数据）。",
        "",
        "用法：把 `.fleet` 拖进 `E:\\SteamLibrary\\steamapps\\common\\Nebulous\\Saves\\Fleets`，"
        "游戏里「舰队 → 载入」即可；也可以用 `repo\\.venv\\Scripts\\python.exe domain\\tools\\validate_fleet.py \"<文件>\"` 先校验。",
        "",
        "> `.fleet` 直接搬运原存档的 `<Ship>` 节点，弹药装载（`<ComponentData>`）、武器组、导弹模板都原样保留；"
        "只有舰队名、点数、描述被改成这艘船自己的。",
        "",
        "| 舰级 | 船名 | 舰体 | 点数 | 来源舰队 | 文件 |",
        "|---|---|---|---:|---|---|",
    ]
    lines += rows
    lines.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    # 同一份清单进知识库：模型被问「有哪些样板船 / 给我一艘 450 CH 的现成船」时能直接答
    kb = ROOT / "domain" / "kb" / "manual_zh" / "样板船清单.md"
    kb.parent.mkdir(parents=True, exist_ok=True)
    by_class: dict[str, list[str]] = {}
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 6 or not cells[5].startswith("`"):
            continue
        by_class.setdefault(cells[0], []).append(
            f"- `{cells[5].strip('`')}` —— {cells[1]}，{cells[3]} 点，舰体 {cells[2]}"
        )
    kb_lines = [
        "# 样板船清单（现成 `.fleet` 文件）",
        "",
        "Tags: kind=manual; topic=sample ships, 样板船, 现成配置, 照抄",
        "Keywords: 样板船, 现成配置, 照抄, sample, 模板船, fleet 文件, 抄船, 全套装配",
        f"Summary: 已导出 {written} 艘 good 样本船的独立 `.fleet` 文件（在项目根 `sample fleets/`），"
        "按舰级列出船名、点数、舰体；每艘还对应 `builds/<舰级>-sample-N.md` 的逐槽装配表。",
        "",
        "这些文件直接搬自真实存档，弹药装载、武器组、导弹模板都在里面，拖进 "
        "`Saves/Fleets` 就能在游戏里载入。用户问「有没有现成的 X 级船能抄」时先给这里的船名与文件。",
        "",
    ]
    for cls in sorted(by_class, key=str.lower):
        kb_lines += [f"## {cls}", ""] + by_class[cls] + [""]

    # 合并舰队：一个文件装下全部样板船（需要无船数上限 mod）
    merged = merge_all()
    if merged:
        kb_lines += [
            "## 全样板船合并舰队（需要无船数上限 mod）",
            "",
            "| 文件 | 阵营 | 船数 | 总点数 |",
            "|---|---|---:|---:|",
        ]
        for name, faction, ships, points in merged:
            kb_lines.append(f"| `{name}` | {faction} | {ships} | {points:.0f} |")
        kb_lines += [
            "",
            "按阵营拆成两个文件：`<FactionKey>` 是舰队级的，SA 与 OSP 的部件混进同一条舰队"
            "载入时会被游戏按舰队阵营判掉。",
            "",
        ]
    kb.write_text("\n".join(kb_lines), encoding="utf-8")
    print(f"kb list -> {kb}")
    print(f"wrote {written} fleets -> {OUT_DIR}")
    print(f"report -> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
