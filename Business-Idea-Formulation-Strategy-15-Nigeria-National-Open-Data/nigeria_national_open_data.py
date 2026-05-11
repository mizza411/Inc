#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 15: Nigeria National / Open Data (Data-First)

Phase 3.1 (implemented here):
- Manual input schema validation (no network calls)
- Generate a copy-paste payload for Prompt 1a from Nigeria official/open stats

Phase 3.2+ may add optional fetching/parsing helpers for specific sources.
"""

import argparse
import html
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import URLError
from urllib.request import Request, urlopen

# Repo root on sys.path for shared cursor_copy_helper (same pattern as Strategy 5)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from cursor_copy_helper import offer_cursor_copy_block, refresh_past_business_ideas_for_directory
except ImportError:
    offer_cursor_copy_block = None
    refresh_past_business_ideas_for_directory = None

from browser_links import collect_source_urls_from_raw_records, open_urls_in_browser
from output_normalizer import (
    merge_response_rows_into_phase4,
    parse_markdown_table,
    render_full_phase4_markdown,
    render_phase4_markdown_table,
)
from catalog_search_terms import get_search_terms_for_portal_url, offer_catalog_search_term_menu
from portal_menu import DEFAULT_PORTALS, run_portal_selection_interactive

# Instruction for Cursor block (data-first). use_config=False on offer_cursor_copy_block so
# repo-root cursor_copy_block_config.json (often Strategy 5) does not override these prompts.
def open_file_automatically(file_path: Path) -> None:
    """Open a file in the default app (Strategy 5 parity: Notepad/editor on Windows)."""
    try:
        if not file_path.exists():
            print(f"\n⚠ Preview file not found: {file_path}")
            return
        p = file_path.resolve()
        if sys.platform == "win32":
            os.startfile(str(p))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(p)], check=False)
        else:
            subprocess.run(["xdg-open", str(p)], check=False)
        print(f"\n✓ Opened preview file automatically: {file_path.name}")
    except Exception as exc:
        print(f"\n⚠ Could not open preview automatically ({exc}). Open manually: {file_path}")


def save_fetch_preview_txt(
    *,
    strategy_dir: Path,
    source_index: int,
    url: str,
    excerpt: str,
    max_chars: int,
) -> Path:
    """Write auto-fetched plain text to disk and return path (Strategy 5–style visibility)."""
    out_dir = strategy_dir / "fetched_previews"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"fetched_preview_{ts}_source{source_index}.txt"
    path = out_dir / name
    header = (
        "Strategy 15 — auto-fetch preview (plain text after HTML strip and --max-chars cap)\n"
        f"URL: {url}\n"
        f"Source slot: {source_index}\n"
        f"Max chars setting: {max_chars:,}\n"
        f"Excerpt length: {len(excerpt):,}\n"
        f"{'=' * 72}\n\n"
    )
    path.write_text(header + excerpt, encoding="utf-8")
    return path


STRATEGY_15_CURSOR_INSTRUCTION = (
    "Read the document at the path above (Strategy 15 payload: excerpts plus optional Local source file paths from portal downloads). "
    "When a path appears, open that file on disk when possible and use it together with the excerpt. "
    "Apply Prompt 1a, then Prompt 1b, then Prompt 1c in the same chat session. "
    "Full wording for each step is in chatgpt_prompt_1a.txt, chatgpt_prompt_1b.txt, and chatgpt_prompt_1c.txt next to this payload. "
    "Write markdown output to business_ideas_YYYYMMDD.md (today's date) in the same folder as the payload."
)

# Short refs for Cursor copy-block (Strategy 5–style: pointer lines; full text stays in chatgpt_prompt_*.txt).
STRATEGY_15_PROMPT_1A_REF = (
    "Nigeria official/open statistics only (not news). Ground ideas in the payload excerpt and any "
    "'Local source file' path—open the portal download when the path is available. "
    "Full instructions: chatgpt_prompt_1a.txt."
)
STRATEGY_15_PROMPT_1B_REF = (
    "Expand Prompt 1a hooks into one markdown section per idea (Business Idea + Digital Solution). "
    "Full structure: chatgpt_prompt_1b.txt."
)
STRATEGY_15_PROMPT_1C_REF = (
    "After 1b: add conditional Hardware Solution under each idea per chatgpt_prompt_1c.txt "
    "(use N/A when hardware is not central)."
)


def _supplementary_local_files_for_cursor_block(records: List[Dict[str, Any]]) -> str:
    """Duplicate portal-download paths into the Cursor copy block so they appear beside the payload path."""
    seen: List[str] = []
    for r in records:
        sf = r.get("source_file")
        if not sf:
            continue
        p = str(sf).strip()
        if p and p not in seen:
            seen.append(p)
    if not seen:
        return ""
    lines = [
        "Local source file(s) from portal download(s) — open on disk together with the payload:",
    ]
    for i, p in enumerate(seen, 1):
        lines.append(f"  {i}. {p}")
    lines.append("(Same paths appear inside the payload document.)")
    return "\n".join(lines)


# Numbered presets for Step 2 (like Strategy 5 source menu). Extend or edit this list anytime.
def print_interactive_run_overview(*, max_chars: int) -> None:
    """Explicit terminal instructions before Step 1 (default interactive mode)."""
    print("\n" + "-" * 60)
    print("INTERACTIVE RUN — INSTRUCTIONS (read this once per run)")
    print("-" * 60)
    print("You are in the default wizard (like Strategy 5: menu → collect → outputs).")
    print("")
    print("STEP 1 — Portal selection")
    print("  • Enter ONE OR MORE numbers from the list, separated by commas (example: 1,3).")
    print("  • Press Enter after typing your selection at the 'Selection:' prompt.")
    print("  • You will be asked whether to open those URLs in your browser (y/n).")
    print("")
    print("STEP 2 — Content collection (repeated for EACH portal you picked)")
    print("  • Catalog portals: you may get a numbered menu of search keywords → copied to clipboard")
    print("    for the site’s search box; then open results and paste the excerpt here (M).")
    print("  • M = Manual paste: excerpt/table row from the report or dataset page.")
    print("    Finish with a blank line (Enter twice). Default for catalog entry URLs.")
    print("  • F = Local file: path to a download (CSV/TXT/HTML/etc.) while this script runs.")
    print("    Paths can be absolute or relative to current folder or Strategy 15 folder.")
    print("    If the file has no extractable text (e.g. .xlsx), you will be prompted to paste a short summary.")
    print("  • A = Auto-fetch this URL only (~{:,} chars max); preview saved under fetched_previews/.".format(max_chars))
    print("    Often noisy on catalog home pages — prefer F or M after searching.")
    print("  • S = Skip this portal (no record saved).")
    print("")
    print("Provenance (indicator, period, source, gaps) is not prompted here — placeholders are")
    print("  written for you; refine them in Cursor or in the generated payload file.")
    print("")
    print("After Step 2: this script writes nigeria_inputs.json, payload + tables, then the Cursor copy block.")
    print("File-only mode (skip this wizard):  python ... --non-interactive --inputs nigeria_inputs.json")
    print("-" * 60)


def _load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_record(raw: Dict[str, Any], idx: int) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    errors: List[str] = []

    def req_str(key: str) -> str:
        val = raw.get(key, "")
        if val is None:
            val = ""
        s = str(val).strip()
        if not s:
            errors.append(f"Record {idx + 1}: missing/empty required field `{key}`.")
        return s

    indicator = req_str("indicator")
    period = req_str("period")
    source = req_str("source")

    if errors:
        return None, errors

    # Optional fields for honesty and gap handling.
    gaps = raw.get("gaps", "N/A")
    if gaps is None:
        gaps = "N/A"
    gaps_s = str(gaps).strip() or "N/A"

    statistical_content = raw.get("statistical_content", "")
    if statistical_content is None:
        statistical_content = ""
    content_s = str(statistical_content).strip()

    norm: Dict[str, Any] = {
        "indicator": indicator,
        "period": period,
        "source": source,
        "gaps": gaps_s,
        "statistical_content": content_s,
    }
    for key in ("source_url", "source_file", "catalog_search_term_used", "provenance_note"):
        v = raw.get(key)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            norm[key] = s
    fm = raw.get("file_matches_catalog_search", None)
    if fm is True or fm is False:
        norm["file_matches_catalog_search"] = fm

    return (norm, [])


def load_and_validate_inputs(inputs_path: Path) -> List[Dict[str, Any]]:
    if not inputs_path.exists():
        raise FileNotFoundError(str(inputs_path))

    data = _load_json(inputs_path)

    # Accept either a plain list OR {"records": [...]}
    if isinstance(data, list):
        records_raw = data
    elif isinstance(data, dict) and isinstance(data.get("records"), list):
        records_raw = data["records"]
    else:
        raise ValueError(
            f"Unsupported inputs JSON format in {inputs_path}. Expected a list of records or {{\"records\": [...]}}."
        )

    if not records_raw:
        raise ValueError(f"No records found in {inputs_path}.")

    return _validate_records_raw(records_raw)


def _validate_records_raw(records_raw: List[Any]) -> List[Dict[str, Any]]:
    validated: List[Dict[str, Any]] = []
    all_errors: List[str] = []

    for idx, raw in enumerate(records_raw):
        if not isinstance(raw, dict):
            all_errors.append(f"Record {idx + 1}: expected object/dict, got {type(raw).__name__}.")
            continue

        norm, errs = _normalize_record(raw, idx)
        if errs:
            all_errors.extend(errs)
        elif norm:
            validated.append(norm)

    if all_errors:
        raise ValueError("\n".join(all_errors))
    if not validated:
        raise ValueError("No valid records were collected.")

    return validated


def _extract_host_label(url: str) -> str:
    clean = (url or "").strip()
    if not clean:
        return "Selected source"
    no_proto = clean.replace("https://", "").replace("http://", "")
    return no_proto.split("/")[0] or clean


def _resolve_local_input_path(raw: str, strategy_dir: Path) -> Path:
    """Resolve a user path: existing file as-is, cwd-relative, then strategy-folder-relative."""
    text = (raw or "").strip().strip('"').strip("'")
    p = Path(text).expanduser()
    if p.is_file():
        return p.resolve()
    if not p.is_absolute():
        cand = (Path.cwd() / p).resolve()
        if cand.is_file():
            return cand
        cand = (strategy_dir / p).resolve()
        if cand.is_file():
            return cand
    return p.resolve()


def _read_local_file_excerpt(path: Path, *, max_chars: int) -> str:
    """Load text from a local file; strip HTML-like content; cap length."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        print(
            "  Note: Plain read of .pdf often yields little usable text—prefer CSV/XLSX export "
            "or use M to paste table rows from the PDF viewer."
        )
    raw_text = _read_text_from_file(path)
    low = raw_text[:8000].lower()
    if "<html" in low or "<body" in low or "<table" in low:
        raw_text = _strip_html_to_text(raw_text)
    return _extract_by_keywords(raw_text, [], max_chars=max_chars)


def _read_multiline_paste(*intro_lines: str) -> str:
    """Read lines until blank line twice; leading blank-only submit returns empty."""
    for s in intro_lines:
        print(s)
    lines: List[str] = []
    while True:
        line = input()
        if not line and not lines:
            break
        if not line and lines:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run_source_collection_interactive(selected_urls: List[str], *, max_chars: int) -> List[Dict[str, Any]]:
    """
    Mandatory Step 2 flow (Strategy 5 style):
    For each selected source, collect statistical excerpt via auto-fetch or manual paste,
    then apply default provenance placeholders (refine in Cursor / payload).
    """
    print("\n" + "=" * 60)
    print("STEP 2: Collect Source Content")
    print("=" * 60)
    print("\nINSTRUCTIONS:")
    print("  For each URL: optional catalog search-term menu (clipboard) → then M/F/A/S.")
    print("  • M — Paste excerpt from the report/dataset page (recommended for catalogs).")
    print("  • F — Path to a local downloaded file (CSV, TXT, HTML…); content capped by --max-chars.")
    print("    If nothing readable is extracted (e.g. binary .xlsx), you will be asked to paste a short summary.")
    print("  • A — Auto-fetch this URL’s HTML as plain text (preview opens; often poor on home pages).")
    print("  • S — Skip this URL (no row saved).")
    print("  After text is captured: provenance uses TBD placeholders (no interactive prompts).")

    if not selected_urls:
        print("\nNo portals selected in Step 1. Please re-run and select at least one portal.")
        return []

    strategy_dir = Path(__file__).resolve().parent
    records: List[Dict[str, Any]] = []
    for idx, url in enumerate(selected_urls, 1):
        print(f"\n--- Source {idx}/{len(selected_urls)} ---")
        print(f"URL: {url}")

        catalog_terms = get_search_terms_for_portal_url(url)
        has_catalog = bool(catalog_terms)
        catalog_term_chosen: Optional[str] = None
        if catalog_terms:
            catalog_term_chosen = offer_catalog_search_term_menu(catalog_terms)

        print("\nHow to collect text for THIS source?")
        print("  M = Manual paste   F = Local file path   A = Auto-fetch URL   S = Skip")
        default_letter = "m" if has_catalog else "a"
        hint = "M" if has_catalog else "A"
        raw_mode = input(f"Type M, F, A, or S (default={hint}): ").strip().lower()
        if raw_mode == "":
            mode = default_letter
        elif raw_mode in ("m", "f", "a", "s"):
            mode = raw_mode
        else:
            mode = default_letter

        if mode == "s":
            print("Skipped.")
            continue

        excerpt = ""
        source_file_saved: Optional[str] = None
        file_matches_catalog_search: Optional[bool] = None
        provenance_note_extra = ""

        if mode == "f":
            print("  Enter full path to your downloaded file (quotes OK on Windows).")
            print(f"  Tip: cwd={Path.cwd()} ; strategy folder={strategy_dir}")
            path_raw = input("  File path: ").strip()
            file_path = _resolve_local_input_path(path_raw, strategy_dir)
            if not file_path.is_file():
                print(f"  ⚠ Not found or not a file: {file_path}")
                print("  You can paste manually below, or re-run this source.")
            else:
                try:
                    excerpt = _read_local_file_excerpt(file_path, max_chars=max_chars)
                    source_file_saved = str(file_path.resolve())
                    print(f"  ✓ Read {len(excerpt):,} characters from file (capped by --max-chars).")
                    if catalog_term_chosen:
                        ans = input(
                            "  Does this file correspond to that catalog search term "
                            f"({catalog_term_chosen!r})? (y/n/skip): "
                        ).strip().lower()
                        if ans in ("y", "yes"):
                            file_matches_catalog_search = True
                        elif ans in ("n", "no"):
                            file_matches_catalog_search = False
                    note_in = input(
                        "  Optional audit note (e.g. file from a different search); Enter to skip: "
                    ).strip()
                    if note_in:
                        provenance_note_extra = note_in
                except OSError as exc:
                    print(f"  ⚠ Could not read file: {exc}")

        if mode == "f" and source_file_saved and not excerpt.strip():
            excerpt = _read_multiline_paste(
                "\nNo readable text was extracted from the file (common for .xlsx / other binary formats).",
                "Paste a short human summary for Prompt 1a — e.g. sheet name, table title, TOTAL row, or key figures.",
                "Paste below, then press Enter on an empty line twice to finish (or twice immediately to skip).",
            )

        if mode == "a":
            print(f"  Attempting auto-fetch (max excerpt length: {max_chars:,} characters)...")
            try:
                text = _fetch_text_from_url(url)
                if "<html" in text.lower() or "<body" in text.lower() or "<table" in text.lower() or "<p" in text.lower():
                    text = _strip_html_to_text(text)
                excerpt = _extract_by_keywords(text, [], max_chars=max_chars)
                print(f"  ✓ Auto-collected {len(excerpt)} characters (capped by --max-chars).")
                preview_path = save_fetch_preview_txt(
                    strategy_dir=strategy_dir,
                    source_index=idx,
                    url=url,
                    excerpt=excerpt,
                    max_chars=max_chars,
                )
                print(f"  ✓ Saved scrape preview: {preview_path.relative_to(strategy_dir)}")
                open_file_automatically(preview_path)
                print("  If this text is not the right table or figure, you can still complete this source,")
                print("  or choose S to skip and re-run later; next time pick M to paste only what you need.")
            except Exception as exc:
                print(f"  ⚠ Auto collection failed: {exc}")
                print("  You will be asked to paste manually below.")

        need_generic_paste = mode == "m" or (
            not excerpt.strip() and not (mode == "f" and source_file_saved)
        )
        if need_generic_paste:
            excerpt = _read_multiline_paste(
                "\nMANUAL PASTE:",
                "  Copy the relevant table row, figure, or short paragraph from the official source.",
                "  Paste here, then press Enter on an empty line twice to finish.",
            )

        print("\nDefault provenance placeholders (refine in Cursor or in strategy15_prompt_1a_payload.txt).")
        host = _extract_host_label(url)
        indicator = "TBD — refine from official excerpt or file"
        period = "TBD — confirm from publisher release"
        source = host
        if source_file_saved:
            source = f"{host}; local file: {Path(source_file_saved).name}"
        gaps = "Placeholder — verify indicator, period, and series against the official source."

        rec: Dict[str, Any] = {
            "indicator": indicator,
            "period": period,
            "source": source,
            "gaps": gaps,
            "statistical_content": excerpt,
            "source_url": url,
        }
        if source_file_saved:
            rec["source_file"] = source_file_saved
        if catalog_term_chosen:
            rec["catalog_search_term_used"] = catalog_term_chosen
        if file_matches_catalog_search is not None:
            rec["file_matches_catalog_search"] = file_matches_catalog_search
        if provenance_note_extra:
            rec["provenance_note"] = provenance_note_extra
        records.append(rec)

    print(f"\n✓ Collected {len(records)} record(s) from selected source(s).")
    return records


def render_prompt_1a_payload(records: List[Dict[str, Any]], out_path: Path) -> None:
    # This payload is meant to be copied into Prompt 1a together with chatgpt_prompt_1a.txt.
    lines: List[str] = []
    lines.append("Nigeria official/open statistical inputs (for Strategy 15).")
    lines.append("Use together with chatgpt_prompt_1a.txt, then chatgpt_prompt_1b.txt, then chatgpt_prompt_1c.txt.")
    lines.append("")
    lines.append(
        "This bundle may include a text excerpt below and/or a Local source file path "
        "(portal download from Step 2 — F). When both exist, prefer the file on disk for tables, units, "
        "and footnotes when you can open it; use the excerpt as in-chat context."
    )
    lines.append("")

    for i, r in enumerate(records):
        lines.append(f"--- Record {i + 1} ---")
        lines.append(f"Statistical indicator (indicator): {r['indicator']}")
        lines.append(f"Period (as published): {r['period']}")
        lines.append(f"Source (org + URL or file name): {r['source']}")
        lines.append(f"Gaps / limitations: {r['gaps']}")
        if r.get("catalog_search_term_used"):
            lines.append(f"Catalog search term used (Step 2 menu): {r['catalog_search_term_used']}")
        if r.get("source_file"):
            lines.append(f"Local source file: {r['source_file']}")
        fm = r.get("file_matches_catalog_search")
        if fm is True or fm is False:
            lines.append(f"File matches catalog search term: {'yes' if fm else 'no'}")
        if r.get("provenance_note"):
            lines.append(f"Provenance note: {r['provenance_note']}")
        if r["statistical_content"]:
            lines.append("Statistical content excerpt:")
            lines.append(r["statistical_content"])
        else:
            lines.append("Statistical content excerpt: [add a short excerpt/row from the official source]")
        lines.append("")

    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def _strip_html_to_text(s: str) -> str:
    """
    Minimal HTML-to-text extractor (stdlib-only).
    Keeps readability without extra dependencies.
    """
    # Unescape HTML entities first.
    s2 = html.unescape(s)
    # Replace common separators with newlines before stripping tags.
    for tag in ("</p>", "</div>", "</br>", "<br>", "<br/>", "<br />", "</li>"):
        s2 = s2.replace(tag, "\n")
    # Remove remaining tags.
    out: List[str] = []
    in_tag = False
    buf: List[str] = []
    for ch in s2:
        if ch == "<":
            in_tag = True
            continue
        if ch == ">":
            in_tag = False
            out.append("".join(buf))
            buf = []
            continue
        if in_tag:
            buf.append(ch)
        else:
            # We are outside a tag.
            out.append(ch)

    text = "".join(out)
    # Collapse excessive whitespace.
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def _extract_by_keywords(text: str, keywords: List[str], max_chars: int) -> str:
    if not keywords:
        return text[:max_chars]

    lower = text.lower()
    hits: List[str] = []
    for kw in keywords:
        k = (kw or "").strip().lower()
        if not k:
            continue
        if k in lower:
            # Keep it simple: take a window around the first occurrence.
            pos = lower.find(k)
            start = max(0, pos - 400)
            end = min(len(text), pos + 1600)
            snippet = text[start:end].strip()
            hits.append(snippet)

    if hits:
        joined = "\n\n---\n\n".join(hits)
        return joined[:max_chars]

    return text[:max_chars]


def _resolve_path_maybe_relative(base_dir: Path, maybe_path: str) -> Path:
    p = Path(maybe_path).expanduser()
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


def _fetch_text_from_url(url: str, timeout_s: int = 30) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Strategy15Bot/1.0)"})
    with urlopen(req, timeout=timeout_s) as resp:
        data = resp.read()

    # Attempt best-effort decoding.
    for enc in ("utf-8", "utf-16", "latin-1"):
        try:
            return data.decode(enc, errors="ignore")
        except Exception:
            continue

    # Fallback: latin-1.
    return data.decode("latin-1", errors="ignore")


def _read_text_from_file(path: Path) -> str:
    # Try utf-8 first; fall back.
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return path.read_text(encoding="latin-1", errors="ignore")


def try_populate_statistical_content(
    raw_records: List[Dict[str, Any]],
    validated_records: List[Dict[str, Any]],
    base_dir: Path,
    *,
    fetch: bool,
    overwrite: bool,
    max_chars: int,
    save_fetched: bool,
    fetched_dir: Path,
) -> None:
    """
    Phase 3.2 (opt-in):
    If --fetch is enabled, download/read text only for records that
    have statistical_content empty (unless --overwrite).

    Supported optional input keys per record:
    - source_url: URL to an official/open dataset page (HTML) or text endpoint
    - source_file: local file path (txt/csv/html) to read
    - extract_keywords: list or comma-separated string of keywords for snippet extraction
    """
    if not fetch:
        return

    # Ensure fetched_dir exists only if we actually fetch.
    if save_fetched:
        fetched_dir.mkdir(parents=True, exist_ok=True)

    for i, raw in enumerate(raw_records):
        if i >= len(validated_records):
            break

        validated = validated_records[i]
        needs = overwrite or not validated.get("statistical_content", "").strip()
        if not needs:
            continue

        source_url = raw.get("source_url", "") or ""
        source_file = raw.get("source_file", "") or ""
        keywords_raw = raw.get("extract_keywords", None)

        keywords: List[str] = []
        if isinstance(keywords_raw, list):
            keywords = [str(x) for x in keywords_raw]
        elif isinstance(keywords_raw, str):
            # allow comma or semicolon separated
            parts = [p.strip() for p in keywords_raw.replace(";", ",").split(",")]
            keywords = [p for p in parts if p]

        fetched_text: Optional[str] = None
        fetch_err: Optional[str] = None

        try:
            if str(source_url).strip():
                fetched_text = _fetch_text_from_url(str(source_url).strip())
            elif str(source_file).strip():
                file_path = _resolve_path_maybe_relative(base_dir, str(source_file).strip())
                fetched_text = _read_text_from_file(file_path)
            else:
                fetch_err = "No source_url or source_file provided for this record."
        except URLError as e:
            fetch_err = f"Network/URL error: {e}"
        except Exception as e:
            fetch_err = f"Fetch/read error: {e}"

        if fetch_err:
            # Keep it auditable: do not hallucinate content.
            prev_gaps = validated.get("gaps", "N/A")
            validated["gaps"] = (prev_gaps + " | " + fetch_err).strip(" |")
            validated["statistical_content"] = ""
            continue

        if fetched_text is None:
            continue

        # If it looks like HTML, strip to plain text.
        text = fetched_text
        if "<html" in text.lower() or "<body" in text.lower() or "<table" in text.lower() or "<p" in text.lower():
            text = _strip_html_to_text(text)

        excerpt = _extract_by_keywords(text, keywords, max_chars=max_chars)
        validated["statistical_content"] = excerpt

        if save_fetched:
            (fetched_dir / f"record_{i+1}_raw_excerpt.txt").write_text(
                excerpt, encoding="utf-8"
            )


def _as_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    return s in {"1", "true", "yes", "y"}


def _append_gap_note(existing: str, note: str) -> str:
    base = (existing or "").strip()
    if not base or base == "N/A":
        return note
    if note in base:
        return base
    return f"{base} | {note}"


def apply_data_honesty_policy(
    raw_records: List[Dict[str, Any]],
    validated_records: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Phase 3.3:
    Centralized, deterministic policy for gap/revision/lag/PDF honesty notes.

    Supported optional input keys per record:
    - missing_periods: string/list, e.g. "2020-2021 missing" or ["2020", "2021"]
    - pdf_extract: bool/string (true if extracted from PDF/manual table copy)
    - revised_series: bool/string (true if source series was revised)
    - release_lag_note: string, e.g. "Released 4 months after period end"
    - release_lag_days: int-like, e.g. 120
    - quality_note: string for extra caveats
    """
    enriched: List[Dict[str, Any]] = []

    for i, rec in enumerate(validated_records):
        out = dict(rec)
        raw = raw_records[i] if i < len(raw_records) and isinstance(raw_records[i], dict) else {}

        gaps = out.get("gaps", "N/A")

        missing_periods = raw.get("missing_periods", "")
        if isinstance(missing_periods, list):
            missing_periods = ", ".join(str(x).strip() for x in missing_periods if str(x).strip())
        missing_periods_s = str(missing_periods).strip()
        if missing_periods_s:
            gaps = _append_gap_note(gaps, f"Missing periods: {missing_periods_s}")

        if _as_bool(raw.get("pdf_extract", False)):
            gaps = _append_gap_note(gaps, "PDF/manual extraction used; verify table/page citation.")

        if _as_bool(raw.get("revised_series", False)):
            gaps = _append_gap_note(gaps, "Series may include revisions; prefer latest official release.")

        release_lag_note = str(raw.get("release_lag_note", "")).strip()
        if release_lag_note:
            gaps = _append_gap_note(gaps, f"Release lag: {release_lag_note}")

        lag_days_raw = raw.get("release_lag_days", None)
        if lag_days_raw not in (None, ""):
            try:
                lag_days = int(str(lag_days_raw).strip())
                if lag_days > 0:
                    gaps = _append_gap_note(gaps, f"Release lag days: {lag_days}")
            except ValueError:
                gaps = _append_gap_note(gaps, f"Release lag days (unparsed): {lag_days_raw}")

        quality_note = str(raw.get("quality_note", "")).strip()
        if quality_note:
            gaps = _append_gap_note(gaps, f"Quality note: {quality_note}")

        # If no statistical content after validation/fetch, enforce explicit note.
        if not out.get("statistical_content", "").strip():
            gaps = _append_gap_note(gaps, "No excerpt captured; add short source excerpt before final ideation.")

        out["gaps"] = gaps if gaps.strip() else "N/A"
        enriched.append(out)

    return enriched


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Strategy 15 helper: validate Nigeria data-first inputs and generate a Prompt 1a payload."
    )
    parser.add_argument(
        "--inputs",
        type=str,
        default=None,
        help="Path to inputs JSON. If omitted, defaults to ./nigeria_inputs.json inside the strategy folder.",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Opt-in: download/read text from source_url/source_file to populate statistical_content when empty.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, overwrite statistical_content even when it is already present.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=8000,
        help="Max characters for extracted excerpts (Phase 3.2).",
    )
    parser.add_argument(
        "--save-fetched",
        action="store_true",
        help="If set with --fetch, write extracted excerpts to fetched_content/ for auditability.",
    )
    parser.add_argument(
        "--fetched-dir",
        type=str,
        default="fetched_content",
        help="Directory name for saving fetched excerpts (only with --fetch --save-fetched).",
    )
    parser.add_argument(
        "--prompt1b-response",
        type=str,
        default=None,
        help="Optional path to a markdown table exported from Prompt 1b for auto-merge into normalized output.",
    )
    parser.add_argument(
        "--open-links",
        action="store_true",
        help="Opt-in: open http(s) source_url values from inputs JSON in the browser (deduped).",
    )
    parser.add_argument(
        "--portal-menu",
        action="store_true",
        help="Interactive: pick Nigeria official/open data portals (Strategy 5–style), then optionally open in browser.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Use file-driven mode only (legacy behavior): read inputs JSON directly without mandatory source wizard.",
    )
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    playbook = here / "business-idea-formulation-strategy-15-nigeria-national-open-data.md"
    p1a = here / "chatgpt_prompt_1a.txt"
    p1b = here / "chatgpt_prompt_1b.txt"
    p1c = here / "chatgpt_prompt_1c.txt"

    print("=" * 60)
    print("Strategy 15: Nigeria National / Open Data (Data-First)")
    print("=" * 60)

    print("\nFiles:")
    for p in (playbook, p1a, p1b, p1c):
        status = "ok" if p.exists() else "MISSING"
        print(f"  [{status}] {p.name}")

    # Phase 3.1: default run is Strategy 5-like mandatory interactive source flow.
    default_inputs = here / "nigeria_inputs.json"
    inputs_path = Path(args.inputs).expanduser().resolve() if args.inputs else default_inputs
    raw_records: List[Dict[str, Any]]

    if args.non_interactive:
        print("\n" + "-" * 60)
        print("NON-INTERACTIVE MODE (--non-interactive)")
        print("-" * 60)
        print("Skipping Step 1/2 wizard. Reading records from your --inputs JSON file only.")
        print("-" * 60)
        if not inputs_path.exists():
            print("\nNo inputs file found for non-interactive mode.")
            print("Create a valid JSON file (no // comments). Example:")
            print("  [")
            print("    {")
            print('      "indicator": "Inflation rate (headline, %)",')
            print('      "period": "Q1 2024",')
            print('      "source": "NBS — CPI report (title or file name)",')
            print('      "gaps": "N/A",')
            print('      "statistical_content": "Short excerpt from the official source",')
            print('      "source_url": "https://www.nigerianstat.gov.ng/"')
            print("    }")
            print("  ]")
            print("Optional keys: source_url (http/https for --open-links), source_file, extract_keywords, etc.")
            print(f"\nThen re-run with:")
            print(f"  python {Path(__file__).name} --non-interactive --inputs \"{inputs_path}\"")
            return

        try:
            data = _load_json(inputs_path)
            if isinstance(data, list):
                raw_records = data
            elif isinstance(data, dict) and isinstance(data.get("records"), list):
                raw_records = data["records"]
            else:
                raw_records = []
            validated = load_and_validate_inputs(inputs_path)
        except Exception as e:
            print(f"\n⚠ Inputs validation failed: {e}")
            print("Fix the JSON schema and try again.")
            sys.exit(1)
    else:
        print_interactive_run_overview(max_chars=int(args.max_chars))
        # Step 1: mandatory source selection menu (Strategy 5-style).
        selected_urls = run_portal_selection_interactive(DEFAULT_PORTALS)
        # Step 2: mandatory content collection from selected sources.
        raw_records = run_source_collection_interactive(
            selected_urls, max_chars=int(args.max_chars)
        )
        if not raw_records:
            print("\n⚠ No records collected. Re-run and select at least one source with content.")
            sys.exit(1)
        # Persist latest interactive run as the default inputs file for audit/reuse.
        inputs_path = default_inputs
        inputs_path.write_text(json.dumps(raw_records, indent=2), encoding="utf-8")
        try:
            validated = _validate_records_raw(raw_records)
        except Exception as e:
            print(f"\n⚠ Collected records failed validation: {e}")
            sys.exit(1)

    # Optional secondary open-links pass (works in both modes).
    if args.open_links:
        link_urls = collect_source_urls_from_raw_records(raw_records)
        if link_urls:
            print("\nOpening source_url link(s) in browser...")
            open_urls_in_browser(link_urls)
        else:
            print("\n--open-links: no http(s) source_url fields found in inputs.")

    # Phase 3.2: optional fetch/populate (never runs unless --fetch is explicitly set).
    fetched_dir = here / str(args.fetched_dir)
    try_populate_statistical_content(
        raw_records=raw_records,
        validated_records=validated,
        base_dir=inputs_path.parent,
        fetch=bool(args.fetch),
        overwrite=bool(args.overwrite),
        max_chars=int(args.max_chars),
        save_fetched=bool(args.save_fetched),
        fetched_dir=fetched_dir,
    )

    # Phase 3.3: centralized honesty policy for gaps/revisions/lag/PDF extraction.
    validated = apply_data_honesty_policy(raw_records=raw_records, validated_records=validated)

    validated_out = here / "nigeria_inputs_validated.json"
    validated_out.write_text(json.dumps(validated, indent=2), encoding="utf-8")

    payload_out = here / "strategy15_prompt_1a_payload.txt"
    render_prompt_1a_payload(validated, payload_out)
    phase4_out = here / "strategy15_prompt_1b_normalized_table.md"
    render_phase4_markdown_table(validated, phase4_out)
    phase4_filled_out = here / "strategy15_prompt_1b_normalized_table_filled.md"

    if args.prompt1b_response:
        resp_path = Path(args.prompt1b_response).expanduser().resolve()
        if not resp_path.exists():
            print(f"\n⚠ Prompt 1b response file not found: {resp_path}")
            print("Skipping Phase 4.2 merge.")
        else:
            resp_headers, resp_rows = parse_markdown_table(resp_path)
            merged_rows = merge_response_rows_into_phase4(
                base_records=validated,
                response_headers=resp_headers,
                response_rows=resp_rows,
            )
            render_full_phase4_markdown(merged_rows, phase4_filled_out)
            print(f"✓ Wrote: {phase4_filled_out.name}")

    print(f"\n✓ Validated {len(validated)} record(s).")
    print(f"✓ Wrote: {validated_out.name}")
    print(f"✓ Wrote: {payload_out.name}")
    print(f"✓ Wrote: {phase4_out.name}")
    print("\nNext:")
    print(f"1) Run Prompt 1a ({p1a.name}) with the payload content in ChatGPT or Cursor.")
    print(f"2) Then Prompt 1b ({p1b.name}), then Prompt 1c ({p1c.name}).")

    # Cursor copy-block (short refs like Strategy 5; full prompts stay in chatgpt_prompt_*.txt)
    if offer_cursor_copy_block is not None and payload_out.exists():
        if refresh_past_business_ideas_for_directory is not None:
            past = refresh_past_business_ideas_for_directory(str(here))
            if past is not None:
                print(f"\n  ✓ Past ideas aggregate updated: {past.name}")
        offer_cursor_copy_block(
            document_path=payload_out,
            prompt_1a_ref=STRATEGY_15_PROMPT_1A_REF,
            prompt_1b_ref=STRATEGY_15_PROMPT_1B_REF,
            prompt_1c_ref=STRATEGY_15_PROMPT_1C_REF,
            instruction=STRATEGY_15_CURSOR_INSTRUCTION,
            use_config=False,
            supplementary_block=_supplementary_local_files_for_cursor_block(validated),
        )
        print("\nNext (after copy block): Review ideas; use normalized table outputs as needed.")
    elif offer_cursor_copy_block is None:
        print("\nNote: cursor_copy_helper not available (import failed). Copy prompts manually from this folder.")


if __name__ == "__main__":
    main()
    sys.exit(0)
