#!/usr/bin/env python3
"""ウィキメディア・コモンズのファイル名から写真の配信URLを組み立てる。

コモンズの画像には2通りの参照方法がある。

  (A) Special:FilePath 経由（この資料で使う方法）
        https://commons.wikimedia.org/wiki/Special:FilePath/<名前>?width=<幅>
      コモンズ側が正しい配信URLへ転送してくれる。こちらで場所を計算しなくてよく、
      指定した幅が原寸より大きい場合も勝手に原寸を返してくれるので 404 にならない。

  (B) upload.wikimedia.org の実体パスを自前で計算する方法
        /wikipedia/commons/thumb/<h[0]>/<h[0:2]>/<名前>/<幅>px-<名前>   (h = 名前のMD5)
      転送を挟まない分だけ速いが、計算を1文字でも誤ると全滅する。実際に
      この資料では (B) で30枚すべてが表示できず、(A) に切り替えて解決した。
      いまは photo_diag.html での原因切り分け専用に md5_thumb() として残してある。

AI生成画像は一切使っていない。すべて実際に撮影された写真。
"""

import hashlib
import urllib.parse

# コモンズのパスはこれらの記号をエスケープしない
_SAFE = "()',!*-._~"


def _encode(name: str) -> str:
    return urllib.parse.quote(name.replace(" ", "_"), safe=_SAFE)


def thumb(filename: str, width: int = 1600) -> str:
    """指定した幅の写真URLを返す（Special:FilePath 経由）。"""
    return (
        f"https://commons.wikimedia.org/wiki/Special:FilePath/"
        f"{_encode(filename)}?width={width}"
    )


def original(filename: str) -> str:
    """原寸画像のURLを返す。"""
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{_encode(filename)}"


def md5_thumb(filename: str, width: int = 1600) -> str:
    """upload.wikimedia.org の実体パスを計算する旧方式。

    この方式では写真が表示できなかったため、資料本体では使っていない。
    原因切り分け用のページ (diag.py) から、比較対象としてのみ呼ばれる。
    """
    name = filename.replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    enc = _encode(name)
    return (
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/"
        f"{h[0]}/{h[0:2]}/{enc}/{width}px-{enc}"
    )


def page(filename: str) -> str:
    """コモンズの解説ページ（撮影者・ライセンス表記）のURLを返す。"""
    return "https://commons.wikimedia.org/wiki/File:" + _encode(filename)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(thumb(arg))
