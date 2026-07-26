#!/usr/bin/env python3
"""ウィキメディア・コモンズのファイル名から実写真の配信URLを組み立てる。

コモンズの画像は upload.wikimedia.org 上で
  /wikipedia/commons/<h[0]>/<h[0:2]>/<ファイル名>
というパスに置かれる（h = ファイル名のMD5）。サムネイルは
  /wikipedia/commons/thumb/<h[0]>/<h[0:2]>/<ファイル名>/<幅>px-<ファイル名>
になる。この規則は決まっているので、ファイル名さえ正しければURLを計算できる。

AI生成画像は一切使っていない。すべて実際に撮影された写真。
"""

import hashlib
import urllib.parse

# コモンズのパスはこれらの記号をエスケープしない
_SAFE = "()',!*-._~"


def _encode(name: str) -> str:
    return urllib.parse.quote(name.replace(" ", "_"), safe=_SAFE)


def thumb(filename: str, width: int = 1600) -> str:
    """サムネイル（幅指定）のURLを返す。"""
    name = filename.replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    enc = _encode(name)
    # .JPG などの拡張子はサムネイル名でもそのまま維持される
    return (
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/"
        f"{h[0]}/{h[0:2]}/{enc}/{width}px-{enc}"
    )


def original(filename: str) -> str:
    """原寸画像のURLを返す。"""
    name = filename.replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    return (
        f"https://upload.wikimedia.org/wikipedia/commons/"
        f"{h[0]}/{h[0:2]}/{_encode(name)}"
    )


def page(filename: str) -> str:
    """コモンズの解説ページ（撮影者・ライセンス表記）のURLを返す。"""
    return "https://commons.wikimedia.org/wiki/File:" + _encode(filename)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(thumb(arg))
