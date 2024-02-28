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

class MetaEmoji(TypedDict):
    downloaded: bool
    fileName: str
    emoji: TypedDict('emoji', {"name": str, "category": str, "aliases": list})

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
    Return a dictionary that contains a mapping from emoji name to the emoji filename.
    """
    return {f.stem: f.name for f in files}

def generate_meta(files: list[pathlib.Path], category: str) -> Meta:
    date = datetime.datetime.now()
    meta = {
        "metaVersion": 2,
        "host": "placeholder.localdomain",
        "exportedAt": date.isoformat(),
    }
    emojis = []

    files_dict = generate_name_to_file_dict(files)
    for emoji_name, file_name in files_dict.items():
        emojis.append({
            "downloaded": True,
            "fileName": file_name,
            "emoji": {
                "name": emoji_name,
                "category": category,
                "aliases": []
            }
        })
    
    meta["emojis"] = emojis
    return meta

def generate_pack(files: list[pathlib.Path]) -> Pack:
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
    args = ap.parse_args()
    emoji_path = pathlib.Path(args.emoji_path)
    category = args.category if args.category is not None else emoji_path.name
    zip_path = pathlib.Path(args.zip_path) if args.zip_path else emoji_path

    files: list[pathlib.Path] = []
    for img_glob in IMAGE_GLOBS:
        files.extend(emoji_path.glob(img_glob))

    meta = generate_meta(files, category)
    meta_path = emoji_path / "meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f)

    pack = generate_pack(files)
    pack_path = emoji_path / "pack.json"
    with open(pack_path, "w") as f:
        json.dump(pack, f)

    files.append(meta_path)
    files.append(pack_path)

    if args.create_zip:
        zip_file = zip_path / f"{category}.zip"
        make_zipfile(files, zip_path)

def make_zipfile(files: list[pathlib.Path], zip_path: pathlib.Path) -> None:
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for file_path in files:
            zipf.write(file_path, arcname=file_path.name)
    print(f"Created ZIP file at {zip_path}")

if __name__ == '__main__':
    main()
