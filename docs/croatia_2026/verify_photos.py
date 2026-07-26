#!/usr/bin/env python3
"""index.html が参照している写真URLが実際に開けるかを確かめる。

このリポジトリを生成した環境は外部への通信が遮断されていたため、
URLの組み立て（ファイル名 → MD5 → 配信パス）が正しいことは確認できても、
実際に画像が返ってくるかまでは確認できていない。
手元のネットにつながる環境で一度これを流して、404 が出ないか見てほしい。

  python3 verify_photos.py
"""

import re
import sys
import urllib.error
import urllib.request

SRC = "index.html"


def main() -> int:
    html = open(SRC, encoding="utf-8").read()
    urls = sorted(set(re.findall(r'src="(https://upload\.wikimedia\.org/[^"]+)"', html)))
    print(f"{len(urls)} 枚を確認します\n")

    ng = []
    for url in urls:
        name = url.rsplit("/", 1)[-1]
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "croatia-guide/1.0 (personal use)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                size = int(r.headers.get("Content-Length") or 0)
                print(f"  OK   {r.status}  {size // 1024:5d} KB  {name}")
        except urllib.error.HTTPError as e:
            print(f"  NG   {e.code}              {name}")
            ng.append((e.code, url))
        except Exception as e:  # ネットワーク側の問題
            print(f"  NG   {e}  {name}")
            ng.append(("err", url))

    if ng:
        print(f"\n開けなかった写真が {len(ng)} 枚あります:")
        for code, url in ng:
            print(f"  [{code}] {url}")
        print("\nコモンズ側でファイル名が変わった可能性があります。"
              "build.py の SPOTS で該当のファイル名を差し替えて、"
              "python3 build.py で作り直してください。")
        return 1

    print("\nすべての写真が取得できました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
