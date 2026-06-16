# -*- coding: utf-8 -*-
"""Find which PDF page a text snippet sits on, using MinerU's *_content_list.json
(each text block carries a page_idx and bbox). Use the page_idx to pick a crop band.

Queries are read from a FILE (one per line), NOT the command line, because passing
CJK on the Windows console mangles the encoding. Results are written to a UTF-8 file
(printing CJK to the console also mangles it). Read the output file with a real
editor / the Read tool.

    python locate.py <content_list.json> queries.txt [--out _loc_out.txt]
"""
import argparse, io, json

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('content_list'); ap.add_argument('queries')
    ap.add_argument('--out', default='_loc_out.txt')
    a = ap.parse_args()
    blocks = json.load(open(a.content_list, encoding='utf-8'))
    queries = [ln.rstrip('\n') for ln in io.open(a.queries, encoding='utf-8') if ln.strip()]
    o = io.open(a.out, 'w', encoding='utf-8')
    for q in queries:
        hit = next((b for b in blocks if q in b.get('text', '')), None)
        if hit:
            o.write(f'PDF p{hit["page_idx"] + 1}  bbox={hit.get("bbox")}  <<{q}>>\n')
        else:
            o.write(f'NOT FOUND: {q}\n')
    o.close(); print('wrote', a.out)
