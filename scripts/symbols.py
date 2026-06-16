# -*- coding: utf-8 -*-
"""Dump every Yijing symbol in a .docx with surrounding context, so you can verify
each one is correct. Trigram symbols (U+2630-2637) are flagged separately because a
leftover trigram usually means a missed conversion (e.g. "X卦象☰" needs a hexagram).

    python symbols.py <docx> [--out _sym_out.txt]
"""
import argparse, io
from docx import Document

def istg(c): return 0x2630 <= ord(c) <= 0x2637
def ishex(c): return 0x4DC0 <= ord(c) <= 0x4DFF

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('docx'); ap.add_argument('--out', default='_sym_out.txt')
    a = ap.parse_args()
    ps = [p.text for p in Document(a.docx).paragraphs]
    o = io.open(a.out, 'w', encoding='utf-8')
    for i, t in enumerate(ps):
        if any(istg(c) or ishex(c) for c in t):
            out = ''
            for j, c in enumerate(t):
                if istg(c) or ishex(c):
                    a0 = max(0, j - 8); b0 = min(len(t), j + 3)
                    out += ('[TRIGRAM]' if istg(c) else '[hex]') + f'...{t[a0:b0]}... '
            o.write(f'[{i}] {out}\n')
    o.close(); print('wrote', a.out)
