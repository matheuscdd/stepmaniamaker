from ddc import ddc
import shutil
from yt import download_mp4, download_ogg, download_thumb
from merger import merger
import argparse
import os
from pathlib import Path
from time import time
from concurrent.futures import ThreadPoolExecutor


def main():
    start = time()
    parser = argparse.ArgumentParser(
        description="Baixa um vídeo do youtube e converte para stepmania"
    )
    parser.add_argument("--song", help="Nome da música")
    parser.add_argument("--artist", help="Nome do artista")
    parser.add_argument("--url", help="URL do YouTube")
    parser.add_argument("--output", help="Diretório de destino")
    args = parser.parse_args()
    print(args)

    destination = os.path.join(args.output, args.song)
    if (os.path.exists(destination)):
        return print("❌ Name already exists")

    if Path("work").exists():
        shutil.rmtree("work")
    Path("work").mkdir(exist_ok=True)

    download_ogg(args.url)

    with ThreadPoolExecutor() as executor:
        futures = []
        futures.append(executor.submit(download_mp4, args.url))
        futures.append(executor.submit(download_thumb, args.url))
        futures.append(executor.submit(ddc, args.song, args.artist))
        [future.result() for future in futures]

    merger()

    shutil.copytree("work", destination)
    print(f"✅ Finished song on [{round(time() - start)}s]: {destination}")


if __name__ == "__main__":
    main()
