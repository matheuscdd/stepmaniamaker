from ddc import ddc
import shutil
from yt import download_mp4, download_ogg, download_thumb
from merger import merger
import argparse
import os
from pathlib import Path
from time import time
from concurrent.futures import ThreadPoolExecutor
import platform


def main():
    start = time()
    if platform.system() == "Windows":
        appdata = os.getenv("APPDATA") 
        stepmania_cache = os.path.join(appdata, "StepMania 5", "Cache")
        if os.path.exists(stepmania_cache):
            shutil.rmtree(stepmania_cache)
            print("🧹 Limpando cache")
    
    parser = argparse.ArgumentParser(
        description="Baixa um vídeo do youtube e converte para stepmania"
    )
    parser.add_argument("--song", help="Nome da música")
    parser.add_argument("--artist", help="Nome do artista")
    parser.add_argument("--url", help="URL do YouTube")
    parser.add_argument("--output", help="Diretório de destino")
    parser.add_argument("--has-video", default='1', help="Tem vídeo")
    args = parser.parse_args()
    args.has_video = bool(int(args.has_video))
    print(args)

    destination = os.path.join(args.output, args.song)
    if (os.path.exists(destination)):
        return print("❌ Name already exists")

    work = Path("work")
    if work.exists():
        shutil.rmtree("work")
    work.mkdir(exist_ok=True)

    print("🎶 Process starting")
    download_ogg(args.url)

    with ThreadPoolExecutor() as executor:
        futures = []
        if args.has_video:
            futures.append(executor.submit(download_mp4, args.url))
        futures.append(executor.submit(download_thumb, args.url))
        futures.append(executor.submit(ddc, args.song, args.artist))
        [future.result() for future in futures]

    merger(args.has_video)

    shutil.move("work", destination)
    print(f"✅ Finished song {args.song} with {round(time() - start)} seconds")


if __name__ == "__main__":
    main()
