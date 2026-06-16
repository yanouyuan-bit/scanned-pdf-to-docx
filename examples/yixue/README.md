# Example: 易学哲学史 (History of Yijing Philosophy)

This toolkit was built to convert a four-volume scanned classical-Chinese work
(朱伯崑《易学哲学史》) into clean, structured Word files.

What that domain needed, and how the toolkit handles it:

- **Hexagram / trigram symbols** the OCR cannot read. `convert.py` rebuilds them:
  structured blocks (the eight-trigram table, the King-Wen 64-hexagram sequence
  line) are matched by signature and regenerated; inline `name + ☰` patterns are
  converted to the correct hexagram character; and every symbol gets the
  *Segoe UI Symbol* font, because SongTi renders these code points blank.
- **A book-specific error table** (`scripts/corrections.py`) for the recurring
  lookalike mistakes of this text (爻/交, 蓍/著, names, …).
- **Per-document title maps** like `toc_example.py` here, because OCR drops chapter
  titles and garbles section titles.

`toc_example.py` is a short, illustrative slice (the Tang-dynasty chapter), included
only to show the file format — not the book's content.

> The source book is under copyright; none of its text, OCR output, or generated
> Word files are included in this repository. Only the tooling and workflow are.
