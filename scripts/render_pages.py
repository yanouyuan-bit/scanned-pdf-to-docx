# -*- coding: utf-8 -*-
"""Render specific PDF pages to PNG (for eyeballing layout / picking crop bands).

    python render_pages.py <pdf> 1,3,5-8 [--dpi 200] [--out _pageimg]
"""
import argparse, os, fitz

def parse_pages(spec):
    out = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-'); out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('pages', help='1-based, e.g. 1,3,5-8')
    ap.add_argument('--dpi', type=int, default=200); ap.add_argument('--out', default='_pageimg')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    doc = fitz.open(a.pdf)
    for p in parse_pages(a.pages):
        pix = doc[p - 1].get_pixmap(dpi=a.dpi)
        fn = os.path.join(a.out, f'p{p:04d}.png'); pix.save(fn)
        print(fn, pix.width, 'x', pix.height)
