import argparse
from pathlib import Path

from imageio_ffmpeg import get_ffmpeg_exe
from yt_dlp import YoutubeDL


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def download_mp4(
    url: str,
    output_path: Path,
    ffmpeg_path: str,
    min_height: int,
) -> None:
    ensure_parent(output_path)
    format_selector = (
        "bestvideo[ext=mp4][height>={min_height}]+bestaudio[ext=m4a]/"
        "best[ext=mp4]/best"
    ).format(min_height=min_height)
    ydl_opts = {
        "format": format_selector,
        "outtmpl": str(output_path),
        "merge_output_format": "mp4",
        "ffmpeg_location": ffmpeg_path,
        "noplaylist": True,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_ogg_audio(
    url: str,
    output_path: Path,
    ffmpeg_path: str,
    quality: int,
) -> None:
    ensure_parent(output_path)
    outtmpl = str(output_path.with_suffix("")) + ".%(ext)s"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "ffmpeg_location": ffmpeg_path,
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "vorbis",
                "preferredquality": str(quality),
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Baixa um video do YouTube em MP4 e cria uma versao OGG."
    )
    parser.add_argument("url", help="URL do YouTube")
    parser.add_argument(
        "--audio-quality",
        type=int,
        default=5,
        help="Qualidade do audio OGG (0-10, menor=melhor).",
    )
    parser.add_argument(
        "--min-height",
        type=int,
        default=720,
        help="Altura minima do video em pixels (padrao: 720).",
    )
    args = parser.parse_args()

    base_dir = Path("work").resolve()
    mp4_path = base_dir / "video.mp4"
    ogg_path = base_dir / "video.ogg"
    ffmpeg_path = get_ffmpeg_exe()

    download_mp4(args.url, mp4_path, ffmpeg_path, args.min_height)
    download_ogg_audio(args.url, ogg_path, ffmpeg_path, args.audio_quality)


if __name__ == "__main__":
    main()
