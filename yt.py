import ffmpeg
from pathlib import Path
from imageio_ffmpeg import get_ffmpeg_exe
from yt_dlp import YoutubeDL
import requests
from urllib.parse import urlparse, parse_qs


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def convert_stepmania_safe(tmp, dest):
    (
        ffmpeg.input(tmp)
        .output(
            dest,
            vcodec="libx264",
            pix_fmt="yuv420p",
            profile="baseline",
            level="3.0",
            vf="scale=1280:720,fps=30",
            preset="veryfast",
            crf=23,
            an=None,
            movflags="+faststart",
        )
        .overwrite_output()
        .run()
    )


def download_mp4(
    url: str,
    min_height: int = 720,
) -> None:
    base_dir = Path("work").resolve()
    mp4_path = base_dir / "file.mp4"
    mp4_tmp = base_dir / "tmp.mp4"
    ffmpeg_path = get_ffmpeg_exe()

    ensure_parent(mp4_tmp)
    format_selector = (
        "bestvideo[ext=mp4][height>={min_height}]+bestaudio[ext=m4a]/"
        "best[ext=mp4]/best"
    ).format(min_height=min_height)
    ydl_opts = {
        "format": format_selector,
        "outtmpl": str(mp4_tmp),
        "merge_output_format": "mp4",
        "ffmpeg_location": ffmpeg_path,
        "noplaylist": True,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    convert_stepmania_safe(str(mp4_tmp), str(mp4_path))
    mp4_tmp.unlink()


def download_ogg(
    url: str,
    quality: int = 10,
) -> None:
    base_dir = Path("work").resolve()
    ogg_path = base_dir / "file.ogg"
    ffmpeg_path = get_ffmpeg_exe()

    ensure_parent(ogg_path)
    outtmpl = str(ogg_path.with_suffix("")) + ".%(ext)s"
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


def get_video_id(url):
    # youtu.be/ID
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]

    # youtube.com/watch?v=ID
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]

    raise ValueError("URL inválida do YouTube")


def download_thumb(url):
    base_dir = Path("work").resolve()
    thumb_path = base_dir / "file.jpg"
    video_id = get_video_id(url)

    urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
    ]

    for url in urls:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            with open(thumb_path, "wb") as f:
                f.write(resposta.content)
            print("Thumbnail saved on:", thumb_path)
            return

    print("Não foi possível baixar a thumbnail.")




