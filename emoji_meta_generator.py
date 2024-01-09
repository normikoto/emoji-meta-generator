#!/usr/bin/env python3
import json
import argparse
import datetime
import pathlib
import os
import glob
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

def generate_name_to_file_dict(files: list[str]) -> dict[str, str]:
    """
    Return a dictionary that contains a mapping from emoji name to the emoji filename.
    """
    result = {}
    for f in files:
        path = pathlib.PurePath(f)
        result[path.stem] = path.name
    return result

def generate_meta(files: list[str], category: str) -> Meta:
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

def generate_pack(files: list[str]) -> Pack:
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
    args = ap.parse_args()
    emoji_path = pathlib.Path(args.emoji_path)
    category = args.category if args.category is not None else emoji_path.name
    
    os.chdir(emoji_path)
    files = []
    for img_glob in IMAGE_GLOBS:
        files.extend(glob.glob(img_glob))
    
    meta = generate_meta(files, category)
    with open(emoji_path / "meta.json", "w") as f:
        json.dump(meta, f)
    
    pack = generate_pack(files)
    with open(emoji_path / "pack.json", "w") as f:
        json.dump(pack, f)

if __name__ == '__main__':
    main()