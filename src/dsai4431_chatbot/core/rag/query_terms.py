"""中文提问 → 英文检索词补充（知识库正文保持英文原文，不在文档里做翻译）。

背景：`asset/RAG` 里全部是官方 wiki 的英文原文（部件名、字段名、机制说明）。
中文提问（"有哪些舱室"）与英文文档之间的语义距离太大，实测会被
"decoy container" 这类词抢走。这里在**检索时**把中文术语映射成英文，
与原文一起做向量平均——文档一个字都不改，只在查询侧对齐。
"""

from __future__ import annotations

import re

CJK = re.compile(r"[\u4e00-\u9fff]")

# 中文说法 → 官方 wiki 里的英文词（按 wiki 的用词写，不是直译）
TERMS: list[tuple[str, str]] = [
    # 部件大类
    ("舱室", "compartment"),
    ("指挥舱", "command compartment"),
    ("损管舱", "damage control compartment"),
    ("机库", "hangar"),
    ("模块", "module"),
    ("挂载", "mount"),
    ("武器位", "mount"),
    ("内置部件", "integrated component"),
    ("导弹发射器", "missile launcher"),
    ("发射器", "launcher"),
    ("垂直发射", "vertical launch"),
    ("近防", "point defense"),
    ("点防御", "point defense"),
    ("轴炮", "spinal weapon"),
    ("雷达", "radar"),
    ("传感器", "sensor"),
    ("电子战", "electronic warfare"),
    ("干扰", "jamming"),
    ("诱饵", "decoy"),
    ("反应堆", "reactor"),
    ("动力装置", "powerplant"),
    ("发动机", "drive"),
    ("推进器", "propulsion"),
    ("装甲", "armor"),
    ("穿深", "penetration"),
    ("穿透", "penetration"),
    # 舰船
    ("船体", "hull"),
    ("巡洋舰", "cruiser"),
    ("驱逐舰", "destroyer"),
    ("护卫舰", "frigate"),
    ("战列舰", "battleship"),
    ("航母", "carrier"),
    ("航空母舰", "carrier"),
    ("补给舰", "logistics ship"),
    ("布雷舰", "minelayer"),
    ("舰载机", "spacecraft craft"),
    ("战机", "craft fighter"),
    ("无人机", "drone"),
    # 弹药
    ("弹药", "munition ammunition"),
    ("导弹", "missile"),
    ("炮弹", "shell"),
    ("穿甲弹", "AP shell"),
    ("高爆弹", "HE shell"),
    ("破片", "flechette"),
    ("引信", "fuze"),
    ("导引头", "seeker"),
    ("战斗部", "payload"),
    ("弹体", "missile body"),
    ("水雷", "mine"),
    ("炸弹", "bomb"),
    ("火箭", "rocket"),
    # 武器细分与机制（玩家口语 → 官方用词）
    ("点防炮塔", "point defense turret"),
    ("炮塔", "turret"),
    ("磁轨", "mass driver"),
    ("粒子束", "particle beam"),
    ("等离子", "plasma"),
    ("箔条", "chaff"),
    ("热焰弹", "flare"),
    ("编程通道", "programming channel"),
    ("扬弹机", "ammunition elevator elevator"),
    ("炮术指挥中心", "gun plot center"),
    ("情报中心", "intel compartment"),
    ("战斗情报中心", "combat information center"),
    ("雷达接收机", "radar receiver"),
    ("粒子加速器", "particle accelerator"),
    # 战术与术语（缩写表 / 指挥术语）
    ("软杀", "soft kill"),
    ("硬杀", "hard kill"),
    ("主引导头", "primary seeker"),
    ("副引导头", "secondary seeker"),
    ("验证头", "verification seeker"),
    ("烧穿", "burnthrough sweep"),
    ("航迹", "track"),
    ("锁定", "lock on"),
    ("交战距离", "engagement range"),
    ("集火", "focus fire"),
    ("抢点", "capture point"),
    ("绕侧", "flank"),
    ("抗线", "hold the line"),
    ("拖船", "tugboat"),
    ("箱船", "container liner"),
    ("集装箱船", "container liner"),
    ("长船", "line ship"),
    ("指挥巡洋舰", "command cruiser"),
    ("导弹船", "missile line ship"),
    ("缩写", "abbreviation glossary"),
    ("MMT", "multi mission tug"),
    ("拦截机", "interceptor craft"),
    ("轰炸机", "bomber craft"),
    ("轴炮", "spinal weapon spinal mount"),
    ("地图", "map maps"),
    ("这张图", "map"),
    ("多大", "map size"),
    # 命名差异（wiki 名称 vs 游戏内字符串）
    ("名字", "naming differences wiki in-game name"),
    ("名称", "naming differences wiki in-game name"),
    ("叫法", "naming differences in-game name"),
    ("改名", "renamed naming differences"),
    ("对不上", "naming differences"),
    ("不一致", "naming differences"),
    ("冲突", "naming differences"),
    ("差异", "naming differences"),
    ("换过名", "renamed"),
    # 阵营（wiki 用阵营徽记标记专属部件）
    ("部件", "part"),
    ("组件", "part"),
    ("阵营", "faction"),
    ("势力", "faction"),
    ("哪边", "faction"),
    ("专属", "exclusive only"),
    ("特有", "exclusive only"),
    ("独有", "exclusive only"),
    ("只有", "exclusive only"),
    ("通用", "both factions unrestricted"),
    ("共用", "both factions unrestricted"),
    ("民用", "civilian"),
    ("军用", "military"),
    # 部件分类（"X 模块/挂载/舱室"这种组合口语）
    ("雷达模块", "radar module"),
    ("动力模块", "powerplant module"),
    ("推进模块", "propulsion module"),
    ("武器支援模块", "weapon support module"),
    ("发动机模块", "propulsion drive module"),
    ("损管模块", "damage control module"),
    ("导弹发射器", "missile launcher vertical launch system"),
    ("有哪几种", "list of all entries"),
    ("有哪些", "list of all entries"),
    # 数值字段
    ("点数", "point cost cost"),
    ("质量", "mass tonnes"),
    ("结构值", "hitpoints"),
    ("伤害阈值", "damage threshold"),
    ("射程", "range"),
    ("射速", "rate of fire"),
    ("供电", "power"),
    ("耗电", "required power"),
    ("功率", "power kW"),
    ("信号", "radar signature"),
    ("信号半径", "signature radius"),
    ("乘员", "crew"),
    ("损管", "damage control"),
    ("维修", "repair"),
    ("维修上限", "max repair"),
    ("载弹", "magazine capacity"),
    ("弹舱", "magazine"),
]


def variants(query: str) -> list[tuple[str, float]]:
    """返回要一起编码的查询变体与权重：原文（恒有），以及中文命中术语时的英文补充。

    英文补充里**不带中文原文**——中文句子对英文文档贡献很小，带上反而稀释。
    但提问里已经含有英文实体名（"Ocello 多少点"）时，原文那一份要保住权重，
    否则英文补充词会把实体名压掉。
    """
    text = (query or "").strip()
    if not text:
        return []
    if not CJK.search(text):
        return [(text, 1.0)]

    extra: list[str] = []
    for zh, en in TERMS:
        if zh in text and en not in extra:
            extra.append(en)
    if not extra:
        return [(text, 1.0)]
    latin = re.search(r"[A-Za-z]{2,}", text)
    orig_weight = 0.5 if latin else 0.35
    return [(text, orig_weight), (" ".join(extra), 1.0 - orig_weight)]
