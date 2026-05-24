"""Tests for subtitle generation (Phase 3.6)."""

from pathlib import Path

from core.subtitle_generator import SubtitleGenerator, _format_srt_time, _format_vtt_time


SAMPLE_SCRIPT = {
    "title": "Test Video Title",
    "hook": "Welcome! This is a short hook.",
    "introduction": "Today we explore Afrobeats and Nigerian culture in depth.",
    "main_content": [
        "Afrobeats has grown from Lagos clubs to global charts.",
        "Artists blend Yoruba phrases with English for viral appeal.",
    ],
    "conclusion": "Thanks for watching this cultural breakdown.",
    "call_to_action": "Subscribe for more Nigerian vibes!",
}


def test_srt_time_format():
    assert _format_srt_time(0) == "00:00:00,000"
    assert _format_srt_time(61.5) == "00:01:01,500"


def test_vtt_time_uses_dot_separator():
    assert _format_vtt_time(1.25) == "00:00:01,250".replace(",", ".")


def test_generate_from_script_creates_files(tmp_path: Path):
    gen = SubtitleGenerator(output_dir=tmp_path)
    track = gen.generate_from_script(SAMPLE_SCRIPT)

    assert len(track.cues) >= 4
    assert track.total_duration > 0
    assert Path(track.srt_path).is_file()
    assert Path(track.vtt_path).is_file()

    srt_text = Path(track.srt_path).read_text(encoding="utf-8")
    vtt_text = Path(track.vtt_path).read_text(encoding="utf-8")

    assert "WEBVTT" in vtt_text
    assert "-->" in srt_text
    assert track.cues[0].text in srt_text


def test_cues_are_monotonic_in_time(tmp_path: Path):
    track = SubtitleGenerator(output_dir=tmp_path).generate_from_script(SAMPLE_SCRIPT)
    for i in range(1, len(track.cues)):
        assert track.cues[i].start >= track.cues[i - 1].end - 0.01


def test_empty_script_still_writes_files(tmp_path: Path):
    track = SubtitleGenerator(output_dir=tmp_path).generate_from_script({"title": "empty"})
    assert track.cues == []
    assert Path(track.srt_path).is_file()
    assert Path(track.vtt_path).is_file()
