#!/usr/bin/env python3
"""各ページがA4（210mm × 297mm）に収まっているかを確かめる。

.page は overflow:hidden なので、はみ出しても見た目では気づけない。
ヘッドレスChromeで実際にレイアウトさせ、2つの見かたで検査する。

  1. 余力  … 高さの固定を外し、写真に最低限の高さ(MIN_PHOTO)を与えたときの実寸。
             A4を超えるなら、文字まわりが多すぎて写真の場所が残らない。
  2. 切れ  … 実際のレイアウトのまま、はみ出して隠れている要素がないか。
             写真の実際の表示高さも併せて報告する。
"""

import os
import re
import subprocess
import sys
import tempfile

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")

A4_H = 1122.52   # 297mm を 96dpi 換算
MIN_PHOTO = 90   # 写真1枚に最低これだけの高さは残したい（px）

PROBE = """
<style id="probe">
  .page{height:auto !important; min-height:0 !important; overflow:visible !important;}
  .ph{min-height:%dpx !important;}
  .grid{grid-template-rows:none !important;}
  .spacer{display:none !important;}
</style>
<script>
function label(p){
  var h = p.querySelector('h2, .cover-title');
  return h ? h.textContent.trim().slice(0, 24) : '(表紙)';
}
window.addEventListener('load', function () {
  var pages = [].slice.call(document.querySelectorAll('.page'));
  // 1回目：高さの固定を外した実寸
  var loose = pages.map(function (p) { return Math.round(p.offsetHeight - %.0f); });
  // 2回目：本来のレイアウトに戻して、隠れている要素と写真の高さを見る
  document.getElementById('probe').remove();
  void document.body.offsetHeight;
  var out = pages.map(function (p, i) {
    var clipped = 0;
    [p].concat([].slice.call(p.querySelectorAll('*'))).forEach(function (el) {
      if (el.scrollHeight - el.clientHeight > 1) clipped++;
    });
    var phs = [].slice.call(p.querySelectorAll('.ph'))
                .map(function (e) { return Math.round(e.offsetHeight); });
    var minph = phs.length ? Math.min.apply(null, phs) : -1;
    return [i + 1, label(p), loose[i], clipped, minph].join('|');
  });
  document.title = 'FIT::' + out.join('#');
});
</script>
""" % (MIN_PHOTO, A4_H)


def main() -> int:
    src = open(SRC, encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "probe.html")
        with open(probe, "w", encoding="utf-8") as f:
            f.write(src.replace("</head>", PROBE + "</head>"))
        res = subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
             "--window-size=1400,1200", "--virtual-time-budget=5000",
             "--dump-dom", "file://" + probe],
            capture_output=True, text=True,
        )
    m = re.search(r"FIT::(.*?)</title>", res.stdout, re.S)
    if not m:
        print("測定に失敗しました\n" + res.stderr[-800:], file=sys.stderr)
        return 2

    bad = []
    print(f"{'':<9}{'ページ':<26}{'余力':>8}{'切れ':>6}{'写真高':>8}")
    for entry in m.group(1).split("#"):
        num, name, over, clipped, minph = entry.split("|")
        over, clipped, minph = int(over), int(clipped), int(minph)
        ng = over > 0 or clipped > 0
        mark = "はみ出し " if ng else "OK       "
        room = f"{over:+d}px" if over > 0 else f"余 {-over}px"
        ph = f"{minph}px" if minph >= 0 else "-"
        print(f"{mark}{name:<26}{room:>8}{clipped:>6}{ph:>8}")
        if ng:
            bad.append(num)

    if bad:
        print(f"\n収まっていないページ: {', '.join(bad)}")
        print(f"（余力 = 写真を各 {MIN_PHOTO}px 確保したときのA4超過分／切れ = 隠れている要素の数）")
        return 1
    print("\nすべてA4 1枚に収まっています。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
