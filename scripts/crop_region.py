# -*- coding: utf-8 -*-
"""Crop high-DPI horizontal bands out of PDF pages, for reading small print when
checking a suspect spot against the scan. Specs are 'page:y0:y1', y as a fraction
of page height (0=top, 1=bottom).

    python crop_region.py <pdf> 117:0.38:0.80 91:0.2:0.6 [--dpi 300]
"""
import argparse, os, fitz

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('specs', nargs='+', help='page:y0:y1')
    ap.add_argument('--dpi', type=int, default=300); ap.add_argument('--out', default='_pageimg')
    ap.add_argument('--pad', type=float, default=0.04, help='extra band above/below')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    doc = fitz.open(a.pdf)
    for spec in a.specs:
        p, y0, y1 = spec.split(':'); p = int(p); y0 = float(y0); y1 = float(y1)
        pg = doc[p - 1]; r = pg.rect
        clip = fitz.Rect(r.x0, r.y0 + r.height * max(0, y0 - a.pad),
                         r.x1, r.y0 + r.height * min(1, y1 + a.pad))
        pix = pg.get_pixmap(dpi=a.dpi, clip=clip)
        fn = os.path.join(a.out, f'crop_p{p:04d}_{int(y0*100)}-{int(y1*100)}.png')
        pix.save(fn); print(fn, pix.width, 'x', pix.height)
