# songs-to-mp3

A small Python command-line tool that reads a text file of song names, searches YouTube for each one, and saves the top result as an MP3. It's a thin wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [ffmpeg](https://ffmpeg.org/).

## Features

- Batch-download from a plain `.txt` list, one song per line
- Ignores blank lines, `#` comments, and duplicate entries
- Choose the MP3 bitrate (128, 192, 256 or 320 kbps)
- Embeds title/artist metadata (can be turned off)
- Keeps going if a song fails and saves the failures to `failed.txt` so you can retry
- Remembers what it has already downloaded, so re-running the same list skips finished songs

## Requirements

- Python 3.9 or newer
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) available on your PATH

## Installation

```
pip install yt-dlp
```

Then install ffmpeg:

| OS      | Command                  |
|---------|--------------------------|
| Windows | `winget install ffmpeg`  |
| macOS   | `brew install ffmpeg`    |
| Linux   | `sudo apt install ffmpeg`|

Close and reopen your terminal after installing ffmpeg, then check it with `ffmpeg -version`.

Download `songs_to_mp3.py` from this repo (or clone it):

```
git clone https://github.com/Eslam-Labib/songs-to-mp3.git
cd songs-to-mp3
```

## Getting your song list from Spotify, Apple Music, SoundCloud, YouTube Music and more

You don't have to type your songs by hand. [TuneMyMusic](https://www.tunemymusic.com) is a free third-party website that can read your playlists from streaming services (Spotify, Apple Music, SoundCloud, YouTube Music and many others) and export them as a **TXT** or CSV file.

1. Go to [www.tunemymusic.com](https://www.tunemymusic.com) and click **Let's start**.
2. Choose your **source** service (for example Spotify) and log in so it can read your library.
3. Select the playlists, liked songs, or albums you want.
4. For the destination, choose **Export to file** and pick the **TXT** format.
5. Download the file and save it next to `songs_to_mp3.py` (rename it to `songs.txt` if you like).

Then run the tool on that file:

```
python songs_to_mp3.py songs.txt
```

Notes:

- Open the exported file first and check that each line contains the artist and title. The tool searches YouTube with each line exactly as written.
- If the export has header lines or extra info you don't want, delete them or start those lines with `#` so the tool ignores them.
- TuneMyMusic is not affiliated with this project. Its options, limits and layout may change, so check the site for the current steps.

## Usage

1. Create a `songs.txt` file with one song per line (or export one with TuneMyMusic as described above):

```
Daft Punk - Get Lucky
Fairuz - Li Beirut
# lines starting with # are ignored
Amr Diab Tamally Maak
```

2. Run the script:

```
python songs_to_mp3.py songs.txt
```

On Windows, use `py` instead of `python` if `python` isn't recognized.

### Options

| Option            | Description                                              | Default      |
|-------------------|----------------------------------------------------------|--------------|
| `songs_file`      | Text file with one song name per line (required)         | -            |
| `-o`, `--output`  | Folder to save the MP3s in                               | `./downloads`|
| `-q`, `--quality` | MP3 bitrate in kbps: `128`, `192`, `256`, `320`          | `192`        |
| `--suffix`        | Extra words added to every search, e.g. `"official audio"` | none       |
| `--no-metadata`   | Don't embed title/artist tags                            | off          |

### Examples

Save to a specific folder at 320 kbps:

```
python songs_to_mp3.py songs.txt -o "D:\R music" -q 320
```

Add words to every search to avoid live versions and music videos with long intros:

```
python songs_to_mp3.py songs.txt --suffix "official audio"
```

## Get your playlists into a txt file

Don't want to type your song list by hand? You can export playlists from your streaming accounts (Spotify, Apple Music, YouTube Music and other supported services) to a text file with the free web tool [TuneMyMusic](https://www.tunemymusic.com).

1. Go to [tunemymusic.com](https://www.tunemymusic.com) and click **Let's Start**.
2. Choose your **source** service (for example Spotify, Apple Music or YouTube Music) and log in to it.
3. Pick the playlists (or your liked songs) you want to export.
4. For the destination, choose **Export to file**. No destination account is needed.
5. Choose **TXT** as the file type and download the file.
6. Rename it to `songs.txt` (or use its name directly) and put it next to `songs_to_mp3.py`.
7. Run the tool:

```
python songs_to_mp3.py songs.txt
```

Notes:

- Open the exported file before running the tool and make sure each line is a song name. The script searches YouTube with each line as the query, so extra info like album names is fine, but very messy lines may give wrong matches.
- If your export contains several playlists in one file, remove any heading lines you don't want searched. Lines starting with `#` are ignored.
- TuneMyMusic is a separate third-party service. This project is not affiliated with it, and its features, limits and supported platforms may change. Check their site for the current details.

## Tips

- Use the `Artist - Title` format for the most accurate matches. The script takes the **first** search result, so vague names can pick the wrong version.
- If some songs fail, re-run the tool with the generated `failed.txt` file.
- Keep `yt-dlp` up to date (`pip install -U yt-dlp`). YouTube changes often, and old versions stop working.

## Troubleshooting

| Problem                          | Fix                                                                 |
|----------------------------------|---------------------------------------------------------------------|
| `yt-dlp is not installed`        | Run `pip install yt-dlp`                                            |
| `ffmpeg not found`               | Install ffmpeg and reopen your terminal                             |
| Nothing happens when you run it  | Make sure the script file isn't empty and you're using the right `python`/`py` command |
| `File not found`                 | Run the command from the folder containing `songs.txt`, or give the full path |

## Legal notice

This tool is for downloading audio you have the right to download, such as your own uploads, Creative Commons or royalty-free music. Downloading from YouTube may violate its Terms of Service, and saving copyrighted music without permission may be illegal where you live. You are responsible for how you use this tool. The author is not affiliated with YouTube or Google.

## Credits

Built on [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [ffmpeg](https://ffmpeg.org/).

## License

MIT. See the `LICENSE` file.
