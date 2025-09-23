#!/usr/bin/env python3
import json
import argparse
import datetime
import pathlib
import zipfile
from typing import Literal, TypedDict

# TODO: maybe addd *.avif?
IMAGE_GLOBS = (
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.apng",
    "*.gif",
    "*.webp",
)

class MetaEmojiInfo(TypedDict):
    name: str
    category: str
    aliases: list[str]

class MetaEmoji(TypedDict):
    downloaded: bool
    fileName: str
    emoji: MetaEmojiInfo

class Meta(TypedDict):
    metaVersion: Literal[2]
    host: str
    exportedAt: str
    emojis: list[MetaEmoji]

class Pack(TypedDict):
    files: dict[str, str]
    pack: dict
    count: int

def generate_name_to_file_dict(files: list[pathlib.Path]) -> dict[str, str]:
    """
    Return a dictionary that contains a mapping from emoji name to the emoji
    filename.

    :param files: A list of files
    :returns: A dict mapping the emoji name to the emoji filepath
    """
    return {f.stem: f.name for f in files}

def generate_meta(files: list[pathlib.Path], category: str) -> Meta:
    """
    Generate a dict that complies with the Misskey meta.json format.

    :param files: A list of files to include
    :param category: Name of the emoji category
    :returns: A dictionary in the Misskey meta.json format
    """
    date = datetime.datetime.now()
    meta: Meta = {
        "metaVersion": 2,
        "host": "placeholder.localdomain",
        "exportedAt": date.isoformat(),
        "emojis": []
    }

    files_dict = generate_name_to_file_dict(files)
    for emoji_name, file_name in files_dict.items():
        meta["emojis"].append({
            "downloaded": True,
            "fileName": file_name,
            "emoji": {
                "name": emoji_name,
                "category": category,
                "aliases": []
            }
        })

    return meta

def generate_pack(files: list[pathlib.Path]) -> Pack:
    """
    Generate a dict that complies with the Pleroma/Akkoma pack.json format.

    :param files: A list of files to include
    :returns: A dictionary in the Pleroma/Akkoma pack.json format
    """
    return {
        "files": generate_name_to_file_dict(files),
        "pack": {},
        "count": len(files),
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emoji-path", "-p",
                    help="Location of emojis.", required=True)
    ap.add_argument("--category", "-c",
                    help="Category name.")
    ap.add_argument("--create-zip", "-z", action="store_true",
                    help="Create a zip archive with the emojis")
    ap.add_argument("--zip-path", "-Z",
                    help="Location to save zip file. Defaults to emoji path. Has no effect if --create-zip/-z is not selected")
    ap.add_argument("--format", action="append", choices=["akkoma", "misskey"],
                    help="Emoji pack format to use. Defaults to creating both 'akkoma' (pack.json) and 'misskey' (meta.json) formats")
    args = ap.parse_args()
    emoji_path = pathlib.Path(args.emoji_path)
    category = args.category if args.category is not None else emoji_path.name
    formats = args.format if args.format else ["misskey", "akkoma"]

    files: list[pathlib.Path] = []
    for img_glob in IMAGE_GLOBS:
        files.extend(emoji_path.glob(img_glob))

    zip_files = files[:]
    if "misskey" in formats:
        meta = generate_meta(files, category)
        meta_path = emoji_path / "meta.json"
        with open(meta_path, "w") as f:
            json.dump(meta, f)
        zip_files.append(meta_path)

    if "akkoma" in formats:
        pack = generate_pack(files)
        pack_path = emoji_path / "pack.json"
        with open(pack_path, "w") as f:
            json.dump(pack, f)
        zip_files.append(pack_path)

    if args.create_zip:
        zip_file = pathlib.Path(args.zip_path) if args.zip_path else emoji_path / f"{category}.zip"
        make_zipfile(zip_files, zip_file)

def make_zipfile(files: list[pathlib.Path], zip_file: pathlib.Path) -> None:
    with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for file_path in files:
            zipf.write(file_path, arcname=file_path.name)
    print(f"Created ZIP file at {zip_file}")

if __name__ == '__main__':
    main()
