#!/usr/bin/env python3
"""
songs_to_mp3.py - Read song names from a .txt file (one per line), search
YouTube for each, and save the best match as an MP3.

Setup (one time):
    pip install yt-dlp
    # and install ffmpeg:
    #   Windows:  winget install ffmpeg      (or https://ffmpeg.org/download.html)
    #   macOS:    brew install ffmpeg
    #   Linux:    sudo apt install ffmpeg

Usage:
    python songs_to_mp3.py songs.txt
    python songs_to_mp3.py songs.txt -o ~/Music/batch1 -q 320
    python songs_to_mp3.py songs.txt --suffix "official audio"

songs.txt example (blank lines and lines starting with # are ignored):
    Daft Punk - Get Lucky
    # this is a comment
    Fairuz - Li Beirut
    Amr Diab Tamally Maak
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    from yt_dlp import YoutubeDL
except ImportError:
    sys.exit("yt-dlp is not installed. Run:  pip install yt-dlp")


# Used when you double-click the script (no arguments given). Edit as you like.
DEFAULT_SONGS_FILE = Path(__file__).resolve().parent / "songs.txt"
DEFAULT_OUTPUT = Path(r"D:\R music")


def read_songs(path: Path) -> list[str]:
    """Return cleaned song names, skipping blanks, comments and duplicates."""
    songs, seen = [], set()
    # utf-8-sig strips the BOM that Windows Notepad sometimes adds
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        name = line.strip()
        if not name or name.startswith("#"):
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        songs.append(name)
    return songs


def build_options(out_dir: Path, quality: str, embed_meta: bool) -> dict:
    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }
    ]
    if embed_meta:
        postprocessors.append({"key": "FFmpegMetadata"})

    return {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "postprocessors": postprocessors,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": False,
        "windowsfilenames": True,   # strips characters Windows can't use
        "ignoreerrors": False,
        # Remembers finished downloads so re-running the script skips them
        "download_archive": str(out_dir / ".downloaded.txt"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a list of songs (from a .txt file) as MP3s via YouTube."
    )
    parser.add_argument("songs_file", type=Path, help="text file, one song per line")
    parser.add_argument("-o", "--output", type=Path, default=Path("downloads"),
                        help="output folder (default: ./downloads)")
    parser.add_argument("-q", "--quality", default="192",
                        choices=["128", "192", "256", "320"],
                        help="MP3 bitrate in kbps (default: 192)")
    parser.add_argument("--suffix", default="",
                        help='extra words added to every search, e.g. "official audio"')
    parser.add_argument("--no-metadata", action="store_true",
                        help="don't embed title/artist tags")
    args = parser.parse_args()

    if not args.songs_file.is_file():
        sys.exit(f"File not found: {args.songs_file}")
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg not found. Install it and make sure it's on your PATH "
                 "(see the setup notes at the top of this script).")

    songs = read_songs(args.songs_file)
    if not songs:
        sys.exit("No song names found in the file.")

    args.output.mkdir(parents=True, exist_ok=True)
    opts = build_options(args.output, args.quality, not args.no_metadata)

    ok, failed = [], []
    total = len(songs)
    print(f"Found {total} song(s). Saving MP3s to: {args.output.resolve()}\n")

    with YoutubeDL(opts) as ydl:
        for i, song in enumerate(songs, 1):
            query = f"{song} {args.suffix}".strip()
            print(f"[{i}/{total}] {song} ... ", end="", flush=True)
            try:
                # 'ytsearch1:' = take the top YouTube search result
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                entries = info.get("entries") or []
                title = entries[0].get("title") if entries else None
                if not title:
                    raise RuntimeError("no search results")
                print(f"done  ({title})")
                ok.append(song)
            except KeyboardInterrupt:
                print("\nStopped by user.")
                break
            except Exception as e:  # keep going if one song fails
                reason = str(e).splitlines()[0][:120]
                print(f"FAILED  ({reason})")
                failed.append(song)

    print(f"\nFinished: {len(ok)} succeeded, {len(failed)} failed.")
    if failed:
        failed_file = args.output / "failed.txt"
        failed_file.write_text("\n".join(failed) + "\n", encoding="utf-8")
        print(f"Failed songs saved to {failed_file} - you can re-run with that file.")


if __name__ == "__main__":
    main()
