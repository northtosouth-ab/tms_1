#!/usr/bin/env python3
"""差し替え候補の写真をコモンズから探し、一覧画像（コンタクトシート）にする。

写真の中身を見ずに説明文を書くと、キャプションと絵が食い違う。それを防ぐため、
候補を実際に並べて目で確かめてから採用するのに使う。

  python3 find_photos.py "Dragon Bridge Ljubljana" out.jpg
"""

import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

UA = {
    "User-Agent": "croatia-guide/1.0 "
                  "(https://github.com/northtosouth-ab/tms_1; personal travel document)"
}
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cand_cache")


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    for wait in (2, 4, 8, 0):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read() if binary else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait == 0:
                raise
            time.sleep(wait)
    raise RuntimeError("unreachable")


def search(query, limit=8):
    """コモンズの画像を検索し、(ファイル名, サムネイルURL) を返す。"""
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=" + str(limit) +
           "&gsrsearch=" + urllib.parse.quote(query) +
           "&prop=imageinfo&iiprop=url|size&iiurlwidth=480")
    data = get(url).get("query", {}).get("pages", {})
    out = []
    for p in sorted(data.values(), key=lambda x: x.get("index", 99)):
        ii = p.get("imageinfo", [{}])[0]
        if ii.get("thumburl") and ii.get("width", 0) >= 900:
            out.append((p["title"][len("File:"):], ii["thumburl"]))
    return out


def sheet(cands, out_path, cols=3, cell=(380, 285)):
    """候補を並べた1枚の画像にする。左上に番号を焼き込む。"""
    os.makedirs(CACHE, exist_ok=True)
    rows = (len(cands) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell[0], rows * cell[1]), (240, 242, 245))
    draw = ImageDraw.Draw(sh)
    for i, (name, url) in enumerate(cands):
        cp = os.path.join(CACHE, str(abs(hash(url))) + ".img")
        if not os.path.exists(cp):
            with open(cp, "wb") as f:
                f.write(get(url, binary=True))
            time.sleep(0.5)
        try:
            im = Image.open(cp).convert("RGB")
        except Exception:
            continue
        im.thumbnail(cell)
        x, y = (i % cols) * cell[0], (i // cols) * cell[1]
        sh.paste(im, (x + (cell[0] - im.width) // 2, y + (cell[1] - im.height) // 2))
        draw.rectangle([x + 4, y + 4, x + 40, y + 34], fill=(0, 0, 0))
        draw.text((x + 15, y + 12), str(i + 1), fill=(255, 255, 255))
    sh.save(out_path, quality=88)
    for i, (name, _u) in enumerate(cands, 1):
        print(f"  {i}. {name}")


if __name__ == "__main__":
    q, out = sys.argv[1], sys.argv[2]
    c = search(q)
    print(f"[{q}] {len(c)}件")
    sheet(c, out)
    print("->", out)
