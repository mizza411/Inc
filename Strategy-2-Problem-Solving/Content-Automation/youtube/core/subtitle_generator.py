"""
Automated subtitle generation (SRT + WebVTT) from video scripts.

Timing aligns with the video assembler speaking-rate model (~150 wpm).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class SubtitleCue:
    index: int
    start: float
    end: float
    text: str


@dataclass
class SubtitleTrack:
    title: str
    cues: List[SubtitleCue]
    total_duration: float
    srt_path: str
    vtt_path: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["cues"] = [asdict(c) for c in self.cues]
        return data


class SubtitleGenerator:
    """Generate timed captions from script sections."""

    WORDS_PER_MINUTE = 150
    MAX_CHARS_PER_CUE = 84
    MAX_CUE_SECONDS = 4.5

    SEGMENT_MULTIPLIERS = {
        "hook": 1.2,
        "introduction": 1.0,
        "main_content": 1.0,
        "conclusion": 0.8,
        "call_to_action": 0.9,
    }

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        base = Path(__file__).resolve().parent.parent
        self.output_dir = Path(output_dir or base / "exports" / "subtitles")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_from_script(self, script_data: Dict[str, Any]) -> SubtitleTrack:
        """Build subtitle cues from a script dictionary."""
        sections = self._script_sections(script_data)
        cues: List[SubtitleCue] = []
        cursor = 0.0
        cue_index = 1

        for section_type, text in sections:
            duration = self._segment_duration(text, section_type)
            chunks = self._split_text(text)
            if not chunks:
                continue
            chunk_duration = max(0.8, duration / len(chunks))
            chunk_duration = min(chunk_duration, self.MAX_CUE_SECONDS)

            for chunk in chunks:
                start = cursor
                end = cursor + chunk_duration
                cues.append(SubtitleCue(index=cue_index, start=start, end=end, text=chunk))
                cue_index += 1
                cursor = end

        title = script_data.get("title") or "video"
        srt_path, vtt_path = self._write_files(title, cues)

        return SubtitleTrack(
            title=title,
            cues=cues,
            total_duration=cursor,
            srt_path=srt_path,
            vtt_path=vtt_path,
        )

    def _script_sections(self, script_data: Dict[str, Any]) -> List[tuple[str, str]]:
        sections: List[tuple[str, str]] = []
        for key, section_type in (
            ("hook", "hook"),
            ("introduction", "introduction"),
            ("conclusion", "conclusion"),
            ("call_to_action", "call_to_action"),
        ):
            text = script_data.get(key)
            if text:
                sections.append((section_type, str(text).strip()))

        main = script_data.get("main_content", [])
        if isinstance(main, list):
            for item in main:
                if item:
                    sections.append(("main_content", str(item).strip()))
        elif main:
            sections.append(("main_content", str(main).strip()))

        return sections

    def _segment_duration(self, text: str, section_type: str) -> float:
        words = len(text.split())
        base = (words / self.WORDS_PER_MINUTE) * 60
        multiplier = self.SEGMENT_MULTIPLIERS.get(section_type, 1.0)
        return max(1.0, base * multiplier)

    def _split_text(self, text: str) -> List[str]:
        text = re.sub(r"\s+", " ", text.strip())
        if not text:
            return []

        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: List[str] = []
        current = ""

        for sentence in sentences:
            if len(sentence) <= self.MAX_CHARS_PER_CUE:
                candidate = f"{current} {sentence}".strip() if current else sentence
                if len(candidate) <= self.MAX_CHARS_PER_CUE:
                    current = candidate
                else:
                    if current:
                        chunks.append(current)
                    current = sentence
            else:
                if current:
                    chunks.append(current)
                    current = ""
                words = sentence.split()
                line = ""
                for word in words:
                    candidate = f"{line} {word}".strip() if line else word
                    if len(candidate) <= self.MAX_CHARS_PER_CUE:
                        line = candidate
                    else:
                        if line:
                            chunks.append(line)
                        line = word
                if line:
                    current = line

        if current:
            chunks.append(current)

        return chunks

    def _write_files(self, title: str, cues: List[SubtitleCue]) -> tuple[str, str]:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = re.sub(r"[^\w\-]+", "_", title.lower())[:40] or "video"
        srt_path = self.output_dir / f"{safe}_{stamp}.srt"
        vtt_path = self.output_dir / f"{safe}_{stamp}.vtt"

        srt_lines: List[str] = []
        for cue in cues:
            srt_lines.append(str(cue.index))
            srt_lines.append(f"{_format_srt_time(cue.start)} --> {_format_srt_time(cue.end)}")
            srt_lines.append(cue.text)
            srt_lines.append("")

        vtt_lines = ["WEBVTT", ""]
        for cue in cues:
            vtt_lines.append(f"{_format_vtt_time(cue.start)} --> {_format_vtt_time(cue.end)}")
            vtt_lines.append(cue.text)
            vtt_lines.append("")

        srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
        vtt_path.write_text("\n".join(vtt_lines), encoding="utf-8")
        return str(srt_path), str(vtt_path)


def _format_srt_time(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def _format_vtt_time(seconds: float) -> str:
    return _format_srt_time(seconds).replace(",", ".")
