#!/usr/bin/env python3
"""写真が表示できない原因を切り分けるためのページ (photo_diag.html) を作る。

写真が出ない理由は3つ考えられる。このページを開けば、どれなのかが一目で分かる。

  (1) そもそもWikimediaに繋がらない        -> 一番上の「対照実験」も出ない
  (2) ファイル名が実在しない                -> どちらの方式でも出ない
  (3) URLの組み立て方(MD5)が間違っている    -> FilePath方式だけ出る

MD5方式  : upload.wikimedia.org の実体パスを自前で計算する。速いが計算を誤ると全滅する。
FilePath : commons.wikimedia.org の公式リダイレクト。計算不要で、原寸より大きい幅を
           指定しても勝手に縮めてくれる。確実だがリダイレクトを1回挟む。
"""

import os
from build import all_photos
from photos import md5_thumb, page, thumb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "photo_diag.html")

# 対照実験用。コモンズに昔からある標準のテスト画像。
# これが出ないなら、ファイル名以前にWikimediaへ到達できていない。
CONTROL = "Example.jpg"


def filepath(filename: str, width: int = 320) -> str:
    """Special:FilePath 経由のURL。資料本体もいまはこちらを使っている。"""
    return thumb(filename, width)


def esc(s):
    import html

    return html.escape(str(s), quote=True)


def build():
    rows = []
    for i, (_pagename, fn, cap) in enumerate(all_photos(), 1):
        rows.append(
            f"<tr>"
            f'<td class="n">{i}</td>'
            f'<td class="cap">{esc(cap)}<br>'
            f'<a href="{esc(page(fn))}" target="_blank">{esc(fn)}</a></td>'
            f'<td><img class="t md5" src="{esc(md5_thumb(fn, 320))}" data-file="{esc(fn)}"></td>'
            f'<td><img class="t fp" src="{esc(filepath(fn))}" data-file="{esc(fn)}"></td>'
            f"</tr>"
        )
    return TEMPLATE.replace("__ROWS__", "\n".join(rows)).replace(
        "__CONTROL__", esc(filepath(CONTROL))
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>写真の原因切り分け</title>
<style>
body{font-family:"Yu Gothic UI","Yu Gothic","Hiragino Sans",sans-serif;
  margin:0; padding:24px; background:#f4f6f8; color:#1b2a38;}
h1{font-size:21px; margin:0 0 12px;}
#verdict{position:sticky; top:0; z-index:5; background:#fff; border:2px solid #1b4f72;
  border-radius:10px; padding:14px 18px; margin-bottom:18px; font-size:15px; line-height:1.7;}
#verdict .big{font-size:18px; font-weight:800; display:block; margin-bottom:6px;}
.ok{color:#1e7a46;} .ng{color:#c0392b;}
.ctrl{background:#fff; border-radius:10px; padding:12px 16px; margin-bottom:16px;
  display:flex; align-items:center; gap:14px; font-size:14px;}
.ctrl img{width:120px; border:1px solid #ccd;}
table{border-collapse:collapse; background:#fff; width:100%;
  box-shadow:0 1px 4px rgba(0,0,0,.1); border-radius:10px; overflow:hidden;}
th,td{border-bottom:1px solid #e3e8ec; padding:8px 10px; text-align:left; vertical-align:middle;}
th{background:#eef3f7; font-size:13px; position:sticky; top:96px;}
td.n{color:#8a99a8; font-size:12px; width:28px;}
td.cap{font-size:13px; max-width:280px;}
td.cap a{color:#8a99a8; font-size:11px; word-break:break-all;}
img.t{width:150px; height:113px; object-fit:cover; background:#dfe5ea; display:block;}
img.t.bad{outline:3px solid #c0392b; opacity:.25;}
</style>
</head>
<body>
<h1>写真が出ない原因の切り分け</h1>

<div id="verdict">判定中…</div>

<div class="ctrl">
  <img id="control" src="__CONTROL__">
  <div><b>対照実験</b><br>
  コモンズに確実にある標準テスト画像です。<br>
  <b>これが出ないなら、ファイル名ではなくネットワークの問題です。</b></div>
</div>

<table>
<thead><tr><th></th><th>写真</th><th>MD5方式<br>(upload.wikimedia.org)</th>
<th>FilePath方式<br>(commons.wikimedia.org)</th></tr></thead>
<tbody>
__ROWS__
</tbody>
</table>

<script>
(function () {
  var state = { md5: {ok: 0, ng: 0}, fp: {ok: 0, ng: 0}, control: null };

  function verdict() {
    var v = document.getElementById("verdict");
    var m = state.md5, f = state.fp;
    var total = document.querySelectorAll("img.t.md5").length;
    var head;
    if (state.control === false) {
      head = '<span class="big ng">Wikimediaに接続できていません。</span>'
        + 'ファイル名ではなくネットワーク（社内プロキシ・セキュリティソフト・DNS）が'
        + '原因です。ブラウザで commons.wikimedia.org が開けるか確かめてください。';
    } else if (state.control === true && f.ok === 0 && m.ok === 0 && (f.ng + m.ng) > 0) {
      head = '<span class="big ng">Wikimediaには繋がっていますが、指定した写真が1枚も存在しません。</span>'
        + 'ファイル名が実在しないということです。写真を選び直す必要があります。';
    } else if (f.ok > 0 && m.ok === 0) {
      head = '<span class="big ng">URLの組み立て方（MD5）が間違っています。</span>'
        + 'FilePath方式では表示できているので、写真自体は実在します。'
        + 'FilePath方式に切り替えれば直ります。';
    } else if (f.ok > 0 || m.ok > 0) {
      head = '<span class="big ok">一部は表示できています。</span>'
        + '出ないものだけ差し替えれば大丈夫です。';
    } else {
      head = '<span class="big">読み込み中…</span>';
    }
    v.innerHTML = head
      + '<hr style="border:0;border-top:1px solid #e3e8ec;margin:10px 0">'
      + '対照実験：' + (state.control === true ? '<b class="ok">表示OK</b>'
          : state.control === false ? '<b class="ng">表示できず</b>' : '確認中')
      + '　／　MD5方式：<b class="' + (m.ok ? 'ok' : 'ng') + '">' + m.ok + ' / ' + total + '</b>'
      + '　／　FilePath方式：<b class="' + (f.ok ? 'ok' : 'ng') + '">' + f.ok + ' / ' + total + '</b>';
  }

  var ctrl = document.getElementById("control");
  ctrl.addEventListener("load", function () { state.control = true; verdict(); });
  ctrl.addEventListener("error", function () { state.control = false; verdict(); });
  if (ctrl.complete) { state.control = ctrl.naturalWidth > 0; }

  document.querySelectorAll("img.t").forEach(function (im) {
    var key = im.classList.contains("md5") ? "md5" : "fp";
    function done(good) {
      if (im.dataset.done) return;
      im.dataset.done = "1";
      state[key][good ? "ok" : "ng"]++;
      if (!good) im.classList.add("bad");
      verdict();
    }
    im.addEventListener("load", function () { done(true); });
    im.addEventListener("error", function () { done(false); });
    if (im.complete) done(im.naturalWidth > 0);
  });

  verdict();
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print("出力:", OUT)
