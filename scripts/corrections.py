# -*- coding: utf-8 -*-
"""
Ordered OCR find/replace table, applied to every line before the .docx is built.

This is the table grown for one specific book; treat it as an EXAMPLE. Build your
own by collecting the recurring OCR mistakes you spot during proofreading.

Two techniques worth copying:
  * Order matters - pairs run top to bottom.
  * "Protect -> replace -> restore": when a wrong form is almost always an error
    but is legitimate inside one particular phrase, swap that phrase to a sentinel
    first, run the blanket replace, then swap it back (see the Chen-Tuan block).
"""

_S = ''   # sentinel: Unicode private-use char, never occurs in real text

PAIRS = [
    # --- divination terms commonly mis-OCR'd by lookalike radicals ---
    ('占笼', '占筮'), ('占箍', '占筮'), ('占笨', '占筮'), ('占笠', '占筮'), ('占签', '占筮'),
    ('笼法', '筮法'), ('笨法', '筮法'), ('箍法', '筮法'), ('签法', '筮法'),
    ('笼辞', '筮辞'), ('箍辞', '筮辞'), ('签辞', '筮辞'), ('笨辞', '筮辞'),
    ('卜笼', '卜筮'), ('龟笼', '龟筮'), ('八笼', '八筮'), ('卜签', '卜筮'),
    ('著草', '蓍草'), ('警草', '蓍草'), ('菁草', '蓍草'),
    ('根著', '根蓍'), ('操著', '揲蓍'), ('揲著', '揲蓍'), ('探著', '揲蓍'),
    ('撲著', '揲蓍'), ('楪蓍', '揲蓍'), ('分探其著', '分揲其蓍'),
    ('以警求卦', '以蓍求卦'), ('以著求卦', '以蓍求卦'), ('著数', '蓍数'),
    ('誓圆', '蓍圆'), ('著圆', '蓍圆'), ('著德圆', '蓍德圆'),
    ('言生著', '言生蓍'), ('而生著', '而生蓍'), ('此著何由', '此蓍何由'),
    ('生著之法', '生蓍之法'), ('生著起数', '生蓍起数'),
    # --- proper names ---
    ('何塘', '何瑭'), ('李塔', '李塨'), ('训话', '训诂'),
    ('顾颜刚', '顾颉刚'), ('张政娘', '张政烺'), ('朱伯昆', '朱伯崑'),
    # Chen-Tuan (OCR usually writes the 2nd char wrong). In one fixed verb phrase the
    # "wrong" char is actually correct -> protect that phrase first, restore it last.
    ('陈传之于挺之', _S),
    ('陈转', '陈抟'), ('陈传', '陈抟'),
    (_S, '陈传之于挺之'),
    # --- turtle-shell divination, mis-OCR'd as 下 ---
    ('龟下', '龟卜'), ('下辞', '卜辞'), ('下问', '卜问'), ('下兆', '卜兆'), ('占下', '占卜'),
    ('下笼', '卜筮'), ('下筮', '卜筮'),
    # --- hexagram "line" 爻, frequently OCR'd as the lookalike 交 (context-scoped) ---
    ('交辞', '爻辞'), ('交象', '爻象'), ('交位', '爻位'), ('六交', '六爻'), ('卦交', '卦爻'),
    ('交之象', '爻之象'), ('三百八十四交', '三百八十四爻'), ('一交', '一爻'), ('各交', '各爻'),
    ('上九交', '上九爻'), ('初九交', '初九爻'), ('初六交', '初六爻'), ('刚柔两交', '刚柔两爻'),
    # --- misc word-form errors ---
    ('窠白', '窠臼'),
    ('翼卦', '巽卦'), ('良卦', '艮卦'), ('良其趾', '艮其趾'), ('敦良', '敦艮'),
]


def fix(t):
    for a, b in PAIRS:
        t = t.replace(a, b)
    return t
