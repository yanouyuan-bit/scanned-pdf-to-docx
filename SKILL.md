---
name: scanned-pdf-to-docx
description: >-
  Convert scanned PDFs that have no text layer (classical-Chinese works, old
  typeset academic books) into clean, well-structured Word (.docx) using MinerU
  OCR plus a three-tier proofreading workflow. Use when turning scanned book
  pages into editable Word, OCR-ing a PDF into .docx, or rebuilding a typeset
  book's chapters / sections / special symbols. Not for PDFs that already have a
  good text layer (extract those directly).
---

# Scanned PDF → clean Word

Pipeline: **split → OCR (MinerU) → title map → generate (convert.py) → three-tier
proofread → deliver.** Scripts live in `scripts/`; a worked example is in
`examples/yixue/`; a printable human guide is `docs/workflow-guide.docx`.

> **Copyright:** the workflow and tools are open; the *book* is not. Never commit
> or redistribute source PDFs, OCR text, or generated Word files.

## 0. When to use
Use for scanned/image PDFs (no selectable text). If the PDF already has a clean
text layer, skip OCR and extract directly — this skill is overkill.

## 1. Environment (once)
MinerU needs Python 3.10–3.12 (not 3.13). Use an isolated env; first OCR run
auto-downloads ~1 GB of models from HuggingFace (one time).
```
pip install -U uv
uv venv C:\mineru-env --python 3.12
uv pip install --python C:\mineru-env\Scripts\python.exe -U "mineru[core]" python-docx pymupdf rapidocr-onnxruntime
C:\mineru-env\Scripts\mineru.exe --version
```
Run every python command with that env's interpreter. `C:\mineru-env` is local
(does not sync to OneDrive); a new machine needs a reinstall.

## 2. Split the PDF
A whole book at once thrashes memory for hours; split into 50–400-page chapter
parts and do one at a time (`fitz.open` → `insert_pdf(from_page, to_page)` →
`save`). Render a couple of pages first (`render_pages.py`) and record the
**printed-page → PDF-page offset** — you reuse it through the whole proofread.

## 3. OCR with MinerU
```
$env:MINERU_MODEL_SOURCE="huggingface"
C:\mineru-env\Scripts\mineru.exe -p "part.pdf" -o "_ocr_out\part" -b pipeline -m ocr -l ch_server -f false -t false
```
- `-b pipeline` (CPU-only machines); `-m ocr` (scanned); `-l ch_server` (the
  large Chinese model — noticeably more accurate than `ch`, same speed); `-f/-t
  false` (skip formula/table to save memory).
- **Long-run survival:** disable sleep (`powercfg /change standby-timeout-ac 0`)
  — sleep kills the job and MinerU has no resume; **split anything over ~350
  pages in half** and concatenate the two `.md` files; judge liveness by the log
  file's mtime, not by hope.
- Output: `_ocr_out/part/.../ocr/part.md` plus `*_content_list.json`
  (per-block `page_idx`+`bbox` — your proofread index) and `images/`. Keep them.

## 4. Title map `toc_NN.py`
OCR drops chapter titles (chapter front pages look like images) and garbles
section titles. Write a small module (see `examples/yixue/toc_example.py`) with
`CHAPTERS` / `SEC` / `SUB`. Two rules:
1. Grep the `.md` for `##` lines and write keys **as OCR actually output them,
   typos included** (list variants). Not as the book reads.
2. When OCR and your hand-typed canonical TOC disagree, **trust the scan** — the
   hand copy is the likelier error.

## 5. Generate
```
C:\mineru-env\Scripts\python.exe scripts\convert.py "part.pdf" -o "out\NN.docx" --toc toc_NN.py --md "_ocr_out\part\...\ocr\part.md"
```
`--md` reuses existing OCR (re-runs take seconds). `convert.py` applies
`corrections.py`, restores symbols, maps titles, writes the docx (body SongTi
10.5pt + first-line indent; special symbols get Segoe UI Symbol or they show
blank). Plain front-matter/contents files don't need `--toc`. Check the printed
`headings` count.

## 6. Three-tier proofread (the quality step)
1. **Scan markers:** `python scripts\check.py out\NN.docx`. Hunt empty `“”`
   (usually a dropped 一), empty `《》` (a dropped book title), dash-in-quotes
   (also 一), lookalikes (交→爻, 著→蓍, 签→筮, 下→卜), and the **"重"/☰ form of a
   hexagram symbol**. Context matters — `著作`, `上下交错`, `重叠` are legitimate.
2. **Check against the scan:** search the snippet in `*_content_list.json` for its
   `page_idx`; crop a band with `crop_region.py "page:0.3:0.7"`; read the image.
   Resolve to: real OCR error → fix; OCR matches the book (classical variants
   often look wrong) → leave; unsure → log it.
3. **Fix and re-check:** recurring errors → add to `corrections.py` (then
   **regenerate any already-delivered file that had the error**); one-offs → edit
   the `.md` (use long context strings; each replace must hit exactly once).
   Regenerate with `--md`, rerun `check.py` until markers are zero. Ship a
   per-file "open questions" note alongside each `.docx`.

## Special problems (see `docs/workflow-guide.docx` §8 for detail)
- **Symbols Word shows blank** → must use Segoe UI Symbol; `convert.py` does this.
- **A genuine trigram (☰☱☲…)** in an "interlocking trigrams" sentence must NOT be
  auto-upgraded to a hexagram — wrap it in parentheses, e.g. `兑（☱）`.
- **Index / dense tables produce no text** under `-t false` (the block is stored
  only as an image): re-OCR those block images with `rapidocr-onnxruntime` and
  rebuild from `content_list.json` ordering.
- **Full-page diagrams** become garbage fragments → replace with a placeholder
  note pointing at the scan; don't try to rebuild them from text.
- **PowerShell + Chinese:** never pass CJK as a command-line argument (it mangles)
  — read queries from a file; write results to a UTF-8 file and open that.

## Scripts
`convert.py` (engine) · `corrections.py` (error table — yours to grow) ·
`render_pages.py` · `crop_region.py` · `locate.py` · `check.py` · `symbols.py`.
The hexagram logic in `convert.py`/`corrections.py` is the Yijing example; the
core (corrections + title mapping + docx writing) is general.
