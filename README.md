<!-- Language: **English** · [中文](README.zh-CN.md) -->

# scanned-pdf-to-docx

A practical workflow + toolkit for turning **scanned PDFs with no text layer**
(classical-Chinese works, old typeset academic books) into **clean, well-structured
Word documents** — using [MinerU](https://github.com/opendatalab/MinerU) for OCR and
a disciplined three-tier proofreading pass for quality.

It was built converting a four-volume scanned classical-Chinese book into editable,
correctly-structured `.docx` for a translation team, and is packaged here as a
reusable [Claude](https://claude.com) **skill** (`SKILL.md`) plus standalone scripts.

> **Copyright.** This repository contains only the workflow and tools. It contains
> **no** source PDFs, OCR text, or generated Word files — those belong to the books
> being processed and stay out of version control (see `.gitignore`). Use the
> toolkit only on material you have the right to process.

## Why it exists

Plain "PDF → Word" converters fail on scanned books: there is no text to extract,
OCR garbles classical characters, chapter titles vanish, and domain symbols (here,
Yijing hexagrams) come out blank or wrong. This toolkit addresses each of those with
a repeatable pipeline rather than one-off fixes.

## The pipeline

```
split  →  OCR (MinerU)  →  title map  →  generate (convert.py)  →  three-tier proofread  →  deliver
```

1. **Split** the book into chapter-sized parts (memory).
2. **OCR** each part with MinerU (`ch_server` model).
3. **Title map** — a tiny `toc_NN.py` repairing the headings OCR dropped/garbled.
4. **Generate** the `.docx` with `convert.py` (corrections + symbol repair + titles).
5. **Proofread** in three tiers: scan for error markers → check each against the
   scanned image → fix, and drive the markers to zero.
6. **Deliver** each `.docx` with an "open questions" note.

Full step-by-step instructions are in **[`SKILL.md`](SKILL.md)**, with a printable
illustrated version in **[`docs/workflow-guide.docx`](docs/workflow-guide.docx)**.

## Setup

MinerU needs Python 3.10–3.12. The first OCR run downloads ~1 GB of models once.

```bash
pip install -U uv
uv venv .venv --python 3.12
uv pip install -r requirements.txt
```

## Scripts

| script | what it does |
|---|---|
| `convert.py` | OCR-markdown → corrected, structured `.docx` (the engine) |
| `corrections.py` | ordered OCR find/replace table — an example; grow your own |
| `render_pages.py` / `crop_region.py` | render / crop PDF pages to read the scan |
| `locate.py` | find a snippet's page via MinerU's `content_list.json` |
| `check.py` | scan a `.docx` for error markers, headings, symbol counts |
| `symbols.py` | dump every special symbol with context to verify it |

The Yijing-specific parts (hexagram repair, the example corrections) are clearly
marked; the core — corrections, title mapping, docx writing — is general.

## Using it as a Claude skill

Drop this folder into your Claude skills directory (or point an agent at `SKILL.md`)
and it will follow the workflow on a new book: split, OCR, map titles, generate,
proofread. The honest use is exactly what one colleague suggested about the guide —
*hand it to an AI to run the workflow*, rather than memorise it yourself.

## License

MIT — see [`LICENSE`](LICENSE).
