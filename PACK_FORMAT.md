# `pack.json` format
This is an *unofficial* document sepficying the format of a `pack.json` file as used in Pleroma and derivatives such as Akkoma.

This is a work in progress as I learn more about the format.

## Example
```json
{
  "files": {
    "anubis_approve": "anubis_approve.webp",
    "anubis_check": "anubis_check.webp",
    "anubis_reject": "anubis_reject.webp"
  },
  "pack": {
    "description": "Icons containing the Anubis mascot",
    "fallback-src": "https://example.com/pack.zip",
    "fallback-src-sha256": "INSERT_HASH_HERE",
    "homepage": "https://example.com/emoji-packs",
    "license": "Some-License",
    "share-files": true
  },
  "files_count": 3
}
```

## `files` field
The `files` field contains a JSON object with entries in the format of `"emoji name": "emoji file.ext"`. Required.

## `pack` field
A JSON object containing metadata of the emoji pack. This field is required, but all entries are optional.

### `description`
A brief description of the pack's contents.

### `fallback-src`
Download URL of the emoji pack.

### `fallback-src-sha256`
A SHA-256 hash of the file at the download URL.

### `homepage`
URL of the emoji pack's project homepage if applicable.

### `license`
The license the pack is released under.

### `share-files`
Boolean (`true`/`false`) value determining whether the pack can be downloaded by other servers.

## `files_count` field
Number of files in the pack as determined by the `files` field. Required.
