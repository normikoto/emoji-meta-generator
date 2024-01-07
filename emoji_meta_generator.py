#!/usr/bin/env python3
import json
import argparse
import datetime
import pathlib
import os
import glob

# TODO: maybe addd *.avif?
IMAGE_GLOBS = (
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.apng",
    "*.gif",
    "*.webp",
)

def generate_meta(files: list[str], category: str) -> dict:
    date = datetime.datetime.now()
    meta = {
        "metaVersion": 2,
        "host": "placeholder.localdomain",
        "exportedAt": date.isoformat(),
    }
    emojis = []

    for f in files:
        path = pathlib.PurePath(f)
        emojis.append({
            "downloaded": True,
            "fileName": path.name,
            "emoji": {
                "name": path.stem,
                "category": category,
                "aliases": []
            }
        })
    
    meta["emojis"] = emojis
    return meta

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emoji-path", "-p",
                    help="Location of emojis.", required=True)
    ap.add_argument("--category", "-c",
                    help="Category name.", required=True)
    args = ap.parse_args()
    
    os.chdir(args.emoji_path)
    files = []
    for img_glob in IMAGE_GLOBS:
        files.extend(glob.glob(img_glob))
    
    meta = generate_meta(files, args.category)
    with open(pathlib.Path(args.emoji_path) / "meta.json", "w") as f:
        json.dump(meta, f)

if __name__ == '__main__':
    main()