import re
import zipfile
from pathlib import Path


def extract_metadata(sm_text):
    parts = sm_text.split("#NOTES:")
    return parts[0].strip()


def extract_notes(sm_text):
    pattern = r"#NOTES:[\s\S]*?;"
    return re.findall(pattern, sm_text)


def get_difficulty(notes_block):
    lines = notes_block.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "dance-single:":
            return lines[i + 2].strip()
    return "Unknown"


def remove_zips():
    folder = Path("work")

    for file in folder.glob("*.zip"):
        file.unlink()


def merger(has_video):
    input_dir = Path("work")

    if not input_dir.exists():
        print("❌ Pasta não encontrada")
        return

    zip_files = list(input_dir.rglob("*.zip"))

    if not zip_files:
        print("❌ Nenhum arquivo .zip encontrado")
        return

    merged_notes = []
    used_difficulties = set()
    metadata_written = False
    final_text = ""

    sm_texts = []
    for zip_path in zip_files:
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                for name in zip_file.namelist():
                    lower_name = name.lower()
                    if lower_name.endswith(".sm"):
                        with zip_file.open(name, "r") as sm_file:
                            sm_texts.append(sm_file.read().decode("utf-8"))
        except zipfile.BadZipFile:
            print(f"⚠️ Zip inválido ignorado: {zip_path}")

    if not sm_texts:
        print("❌ Nenhum arquivo .sm encontrado dentro dos zips")
        return

    for text in sm_texts:

        if not metadata_written:
            final_text += extract_metadata(text) + "\n\n"
            metadata_written = True

        for notes in extract_notes(text):
            diff = get_difficulty(notes)

            if diff not in used_difficulties:
                merged_notes.append(notes.strip())
                used_difficulties.add(diff)

    for block in merged_notes:
        final_text += block + "\n\n"

    output_format = "mp4" if has_video else "jpg"
    final_text = f"#BACKGROUND:file.{output_format};\n#BANNER:file.jpg;\n" + final_text
    final_text = re.sub(
        r"#MUSIC:.*?;", "#MUSIC:file.ogg;", final_text, flags=re.IGNORECASE
    )
    output_file = input_dir / "merged.sm"
    output_file.write_text(final_text, encoding="utf-8")
    remove_zips()

    print(f"Arquivo criado: {output_file}")
