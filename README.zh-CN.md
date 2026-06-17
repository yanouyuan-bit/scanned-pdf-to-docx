[English](README.md) · **简体中文**

# scanned-pdf-to-docx

一套把**无文字层的扫描 PDF**（古籍、老排版的学术书）转成**干净、结构化 Word 文档**的工作流与工具集——用 [MinerU](https://github.com/opendatalab/MinerU) 做 OCR，配一套有纪律的**三档校对**保证质量。

它是在把一部四卷本扫描古籍转成可编辑、结构正确的 `.docx`（供翻译团队使用）的过程中沉淀出来的，这里打包成一个可复用的 [Claude](https://claude.com) **技能（skill）**（`SKILL.md`）外加独立脚本。

> **版权说明。** 本仓库**只**包含工作流和工具，**不**含任何源 PDF、OCR 文本或生成的 Word 文件——那些属于被处理的书，不进版本库（见 `.gitignore`）。请只在你有权处理的材料上使用本工具集。

## 为什么需要它

普通的"PDF 转 Word"工具在扫描书上会失败：没有文字可提取，OCR 弄乱古字，章标题消失，专业符号（这里指易经卦象）变成空白或错符。本工具集用一条可复用的流水线逐一解决这些问题，而不是临时打补丁。

## 流水线

```
切分  →  OCR(MinerU)  →  标题映射  →  生成(convert.py)  →  三档校对  →  交付
```

1. **切分**：把整本书切成章节大小的小份（控内存）。
2. **OCR**：每份用 MinerU（`ch_server` 模型）识别。
3. **标题映射**：写一个小小的 `toc_NN.py`，修复 OCR 丢失/弄乱的标题。
4. **生成**：用 `convert.py` 生成 `.docx`（纠错 + 符号修复 + 标题）。
5. **校对**（三档）：扫描错误标记 → 逐处对扫描原图核对 → 修正，把错误标记清零。
6. **交付**：每份 `.docx` 附一份"存疑清单"。

完整分步说明见 **[`SKILL.md`](SKILL.md)**，图文打印版见 **[`docs/workflow-guide.docx`](docs/workflow-guide.docx)**。

## 环境搭建

MinerU 需要 Python 3.10–3.12。首次 OCR 会一次性下载约 1 GB 模型。

```bash
pip install -U uv
uv venv .venv --python 3.12
uv pip install -r requirements.txt
```

## 脚本一览

| 脚本 | 作用 |
|---|---|
| `convert.py` | OCR markdown → 纠错、结构化的 `.docx`（引擎） |
| `corrections.py` | 有序 OCR 查找/替换表——示例，按自己的书增补 |
| `render_pages.py` / `crop_region.py` | 渲染 / 裁剪 PDF 页面以核对扫描原图 |
| `locate.py` | 借 MinerU 的 `content_list.json` 定位某片段所在页 |
| `check.py` | 扫描 `.docx` 的错误标记、标题、符号计数 |
| `symbols.py` | 导出每个特殊符号及上下文供核对 |

易经专用的部分（卦符修复、示例纠错表）都有清楚标注；核心——纠错、标题映射、docx 生成——是通用的。

## 作为 Claude 技能使用

把这个文件夹放进你的 Claude 技能目录（或让一个 agent 直接读 `SKILL.md`），它就会在新书上照此流程走：切分、OCR、映射标题、生成、校对。最实在的用法，正如一位同事评价那份指南时说的——**把它交给 AI 去跑工作流**，而不是自己去背。

## 许可证

MIT —— 见 [`LICENSE`](LICENSE)。
