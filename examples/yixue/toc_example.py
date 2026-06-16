# -*- coding: utf-8 -*-
"""
Example title-mapping module passed to convert.py via --toc.

You write one of these per document. Its whole job is to turn the messy ## heading
lines that OCR produced back into correct, properly-levelled titles.

How convert.py uses it:
  * keys are matched after normalisation (punctuation / digits / ordinal numerals
    are stripped) -- so write the key the way OCR ACTUALLY output the heading,
    including its typos; you may list several key variants for one title.
  * CHAPTERS injects a chapter title in front of its first section -- OCR almost
    always drops chapter titles because the chapter front page is treated as an image.
  * SEC -> section heading (h2);  SUB -> sub-section heading (h3).
  * the value carries the CORRECT text; use a full-width space (　) between the
    ordinal and the title.

The entries below are a short, illustrative slice -- not a complete document.
"""

# (first-section title as it will be displayed, chapter title to inject before it)
CHAPTERS = [
    ('第一节　孔颖达《周易正义》', '第五章　唐代易学哲学的发展'),
]

# key = how OCR rendered the section heading (after normalisation); list typo variants too
SEC = {
    '第一节孔颖达《周易正义》': ('h2', '第一节　孔颖达《周易正义》'),
    '孔颖达《周易正义》':       ('h2', '第一节　孔颖达《周易正义》'),
    '崔憬和李鼎祚的易说':       ('h2', '第二节　崔憬和李鼎祚的易说'),   # OCR dropped the "第二节" prefix
}

SUB = {
    '一论《周易》体例': '一　论《周易》体例', '论《周易》体例': '一　论《周易》体例',
    '二论《周易》的原理': '二　论《周易》的原理', '论《周易》的原理': '二　论《周易》的原理',
    '崔憬《易探玄》': '一　崔憬《易探玄》',
    '二李鼎祚的易学观': '二　李鼎祚的易学观', '李鼎祚的易学观': '二　李鼎祚的易学观',
}
