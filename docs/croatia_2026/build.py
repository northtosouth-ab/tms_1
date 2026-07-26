#!/usr/bin/env python3
"""母向け旅行案内資料（クロアチア＆スロベニア 2026年9月）を生成する。

  python3 build.py            -> index.html を出力（写真はコモンズから直接読み込み）
  python3 build.py --localize -> 写真を images/ に保存し、オフライン版 index_offline.html も出力

ページは A4（210mm × 297mm）ちょうどに固定してあり、ブラウザの
「印刷 → PDFに保存」でそのまま冊子になる。文字は高齢の読み手に合わせて大きめ。
"""

import html
import os
import sys

from photos import page as commons_page
from photos import thumb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "index.html")

# ---------------------------------------------------------------------------
# 写真（すべてウィキメディア・コモンズの実写真。AI生成画像は不使用）
#   各ページは「大きな1枚 ＋ 4枚」の5枚構成で、A4に隙間なく収まる。
# ---------------------------------------------------------------------------

COVER = "Aerial view of the Old Town of Dubrovnik - Croatia.jpg"

SPOTS = [
    {
        "day": "9/19（土）夜 〜 9/21（月）朝",
        "name": "ドゥブロブニク",
        "name_local": "DUBROVNIK ／ クロアチア",
        "lead": "「アドリア海の真珠」。オレンジ色の屋根と分厚い城壁が、海に浮かんで見える世界遺産の街です。",
        "photos": [
            ("Aerial view of the Old Town of Dubrovnik - Croatia.jpg",
             "城壁にぐるりと囲まれた旧市街",
             "街全体が城壁で囲まれています。上から見るとこの形。", True),
            ("Main street-Dubrovnik-2.jpg",
             "プラツァ通り",
             "大理石で磨かれた目抜き通り。平らで歩きやすい道です。", False),
            ("Minčeta Fortress, Dubrovnik 03.jpg",
             "ミンチェタ要塞",
             "城壁でいちばん高い塔。旧市街の目印です。", False),
            ("Cable car to Mount Srd in Dubrovnik, Croatia (48738636363).jpg",
             "スルジ山のケーブルカー",
             "数分で山頂へ。歩かずに一番の絶景が見られます。", False),
            ("Old City of Dubrovnik-108773.jpg",
             "石畳の路地",
             "洗濯物がひらめく路地。人の暮らしがそのまま残っています。", False),
        ],
        "notes": [
            "城壁の上を一周する散歩道（約2km）は階段が多めです。無理せず、途中の階段で降りられます。",
            "スルジ山はケーブルカーで往復します。夕暮れどきがいちばんきれいです。",
        ],
    },
    {
        "day": "9/21（月）13:25 〜 9/22（火）10:15",
        "name": "スプリト",
        "name_local": "SPLIT ／ クロアチア",
        "lead": "ローマ皇帝の宮殿が、そのまま街になった不思議な世界遺産。1700年前の壁の中に、いまも人が住んでいます。",
        "photos": [
            ("Aerial view of Diocletian's Palace in Split, Croatia (48608247353).jpg",
             "ディオクレティアヌス宮殿",
             "宮殿の跡がまるごと旧市街。ここに店も家も並びます。", True),
            ("Peristyle of Diocletian's Palace, Split (11907776284).jpg",
             "列柱廊（ペリスティル）",
             "宮殿の中心の広場。石段に腰かけて休めます。", False),
            ("Cathedral of Saint Domnius - Bell tower 01.jpg",
             "聖ドムニウス大聖堂の鐘楼",
             "街のシンボル。見上げるだけでも十分な迫力です。", False),
            ("Golden Gate entrance to the Diocletian's Palace in Split, Croatia (48693923167).jpg",
             "黄金の門",
             "宮殿の北門。かつて皇帝が通った入口です。", False),
            ("Riva promenade in Split, Croatia (48693340418).jpg",
             "海沿いのリヴァ通り",
             "ヤシ並木の遊歩道。カフェでひと休みするのにぴったり。", False),
        ],
        "notes": [
            "宮殿の中は石畳がすり減って少し滑ります。歩きやすい靴がおすすめです。",
            "鐘楼の階段はかなり急なので、登らず下から眺めるので十分です。",
        ],
    },
    {
        "day": "9/22（火）〜 9/24（木）朝　※観光は9/23終日",
        "name": "プリトヴィッツェ湖群国立公園",
        "name_local": "PLITVIČKA JEZERA ／ クロアチア",
        "lead": "16の湖が滝でつながる、クロアチアで一番有名な自然遺産。水の色は加工なしで、本当にこの色です。",
        "photos": [
            ("Plitvice Lakes, Croatia, Lower Lakes Panorama.JPG",
             "湖が段々につながる眺め",
             "展望台からの景色。ここは歩かずに見られます。", True),
            ("Veliki Slap in Plitvice Lakes National Park in Croatia.jpg",
             "大滝（ヴェリキ・スラップ）",
             "落差78m。公園でいちばん大きな滝です。", False),
            ("Wood way in plitvicka.jpg",
             "湖の上にかかる木道",
             "水面すれすれを歩きます。ゆっくり行きましょう。", False),
            ("Plitvice Lakes, Galovacki buk.JPG",
             "いくつも重なる小さな滝",
             "歩くたびに景色が変わっていきます。", False),
            ("Plitvice Lakes, Croatia, Lower Lakes.JPG",
             "澄みきった湖面",
             "底の倒木まで透けて見えるほどの透明度。", False),
        ],
        "notes": [
            "園内は電気ボートとバスで移動できます。歩く区間は選べるので、体調に合わせて調整します。",
            "木道は濡れていることがあります。滑りにくい靴と、薄手の上着があると安心です。",
        ],
    },
    {
        "day": "9/24（木）12:00 〜 9/25（金）7:30",
        "name": "ザグレブ",
        "name_local": "ZAGREB ／ クロアチアの首都",
        "lead": "屋根の模様が愛らしい教会と、活気ある青空市場。首都ですが、こぢんまりとして歩きやすい街です。",
        "photos": [
            ("St. Mark's Church, Zagreb 01.jpg",
             "聖マルコ教会",
             "色タイルで紋章を描いた屋根。ザグレブ一番の写真スポット。", True),
            ("Croatia-00448 - Zagreb Cathedral (9286530138).jpg",
             "ザグレブ大聖堂",
             "高さ108m。街のどこからでも尖塔が見えます。", False),
            ("Zagreb, Dolac market.JPG",
             "ドラツ市場",
             "赤い日よけが並ぶ青空市場。果物や蜂蜜が並びます。", False),
            ("Zagrebačka uspinjača (Zagreb Funicular) (13024479974).jpg",
             "世界一短いケーブルカー",
             "高台の上町へ、わずか1分で登れます。", False),
            ("Zagreb (29255640143).jpg",
             "イェラチッチ広場",
             "街の中心の広場。ここを起点に歩きます。", False),
        ],
        "notes": [
            "上町（教会のある高台）へはケーブルカーで登れます。坂道を歩く必要はありません。",
            "市場は午前中がいちばんにぎやかです。",
        ],
    },
    {
        "day": "9/25（金）9:40 〜 9/26（土）朝",
        "name": "リュブリャナ",
        "name_local": "LJUBLJANA ／ スロベニアの首都",
        "lead": "川沿いにカフェが並ぶ、ヨーロッパでいちばん小さくて可愛らしい首都のひとつ。丘の上には古城が建ちます。",
        "photos": [
            ("2021-07-28 Ljubljana-0881.jpg",
             "旧市街と丘の上の城",
             "パステル色の街並みの上に、リュブリャナ城。", True),
            ("Ljubljana - Tromostovje (48764029462).jpg",
             "三本橋（トロモストヴィエ）",
             "橋が3本並んだ、街のシンボル的な広場。", False),
            ("Dragon Bridge (Ljubljana) (52932101473).jpg",
             "竜の橋",
             "街の守り神である竜の像。記念写真の定番です。", False),
            ("Ljubljanica River Waterfront - Ljubljana, Slovenia (7451177760).jpg",
             "リュブリャニツァ川沿い",
             "川べりはカフェだらけ。座って眺めるだけで楽しい。", False),
            ("Ljubljana from the Castle view (1).jpg",
             "城からの眺め",
             "オレンジ屋根の街の向こうにアルプスが見えます。", False),
        ],
        "notes": [
            "リュブリャナ城へはケーブルカーで登れます。歩いて坂を上る必要はありません。",
            "旧市街は車が入らない歩行者天国。平らで歩きやすい街です。",
        ],
    },
    {
        "day": "9/25（金）13:19 〜 18:16　日帰り",
        "name": "ブレッド湖",
        "name_local": "BLED ／ スロベニア",
        "lead": "アルプスのふもと、湖の真ん中に島と教会が浮かぶ絵はがきのような景色。リュブリャナから日帰りで訪ねます。",
        "photos": [
            ("Aerial image of Lake Bled (view from the southwest).jpg",
             "湖に浮かぶ島と教会",
             "スロベニアを代表する景色。奥にはアルプスの山並み。", True),
            ("Pletna-Bled.JPG",
             "手漕ぎ舟プレトナ",
             "船頭さんが漕ぐ舟で島へ渡ります。揺れは穏やかです。", False),
            ("Bled Castle.JPG",
             "ブレッド城",
             "崖の上に建つ古城。バスや車で上まで行けます。", False),
            ("Bled-Lake and Island from Castle.JPG",
             "城のテラスからの眺め",
             "湖を真上から見下ろす、いちばんの絶景ポイント。", False),
            ("Vintgar-gorge-bled-slovenia.jpg",
             "ヴィントガル峡谷",
             "エメラルド色の渓流沿いに木道が続きます。", False),
        ],
        "notes": [
            "島の教会までは階段が99段あります。舟から眺めるだけでも十分きれいです。",
            "ブレッド名物のクリームケーキ（クレムナ・レジナ）は、湖を眺めながらぜひ。",
        ],
    },
]

# ---------------------------------------------------------------------------
# 2ページ目：全体行程
# ---------------------------------------------------------------------------

# (日付, 曜日, 行き先, その日の動き, 宿, 行の色分け)
ITINERARY = [
    ("9/18", "金", "大阪 → 東京",
     "香里園から新幹線で上京。", "息子の家", "japan"),
    ("9/19", "土", "成田 → ドゥブロブニク",
     "10:25 成田発 → イスタンブール乗継 → 19:55 着", "Guest House Nenada", "move"),
    ("9/20", "日", "ドゥブロブニク",
     "終日、旧市街と城壁めぐり。", "Guest House Nenada", "stay"),
    ("9/21", "月", "ドゥブロブニク → スプリト",
     "8:00 発 → 13:25 スプリト着", "Villa Spalatina", "move"),
    ("9/22", "火", "スプリト → プリトヴィッツェ",
     "10:15 発 → 14:45 ムキニェ着", "House Dado", "move"),
    ("9/23", "水", "プリトヴィッツェ国立公園",
     "9:00 から、湖と滝をめぐる一日。", "House Dado", "stay"),
    ("9/24", "木", "プリトヴィッツェ → ザグレブ",
     "9:45 発 → 12:00 ザグレブ着", "Hostel Temza", "move"),
    ("9/25", "金", "リュブリャナ ＆ ブレッド湖",
     "7:30 ザグレブ発 → 9:40 着。昼はブレッド湖へ。", "Apartma N'Poznam zupa", "move"),
    ("9/26", "土", "リュブリャナ → 帰国の途へ",
     "9:30 発 → ヘルシンキ乗継 → 17:45 発", "機内泊", "move"),
    ("9/27", "日", "成田 到着 ／ 母は大阪へ",
     "13:05 成田着。おつかれさまでした。", "—", "japan"),
]

# ---------------------------------------------------------------------------
# 3ページ目：9/18 香里園 → 不動前
# ---------------------------------------------------------------------------

ROUTE = [
    {
        "time": "13:35 ごろ 発",
        "place": "香里園駅",
        "line": "京阪本線・急行　淀屋橋ゆき",
        "detail": "いつもの香里園駅から乗ります。<b>淀屋橋ゆき</b>ならどれでも大丈夫。約30分。",
        "kind": "start",
    },
    {
        "time": "14:05 ごろ",
        "place": "淀屋橋駅　でのりかえ",
        "line": "大阪メトロ 御堂筋線・新大阪ゆき方面",
        "detail": "案内板の<b>「御堂筋線」</b>へ地下を5分ほど歩きます。約13分。",
        "kind": "change",
    },
    {
        "time": "14:30 着 ／ 15:00 ごろ 発",
        "place": "新大阪 → 品川",
        "line": "東海道新幹線 のぞみ（指定席）",
        "detail": "<b>品川で降ります。終点の東京ではありません。</b>約2時間25分。",
        "kind": "ride",
    },
    {
        "time": "17:25 ごろ",
        "place": "品川駅　でのりかえ",
        "line": "JR山手線・内回り",
        "detail": "大崎・五反田の次が<b>目黒</b>です（3つ目・約8分）。",
        "kind": "change",
    },
    {
        "time": "17:50 ごろ",
        "place": "目黒駅　でのりかえ",
        "line": "東急目黒線・各駅停車",
        "detail": "<b>不動前はとなりの駅（1つ目）</b>です。約2分。",
        "kind": "change",
    },
    {
        "time": "18:00",
        "place": "不動前駅 改札口　で待ち合わせ",
        "line": "東急目黒線 不動前駅",
        "detail": "<b>不動前駅の改札は1か所だけ</b>です。改札を出たところで待っています。",
        "kind": "goal",
    },
]

# ---------------------------------------------------------------------------
# スタイル
# ---------------------------------------------------------------------------

CSS = """
:root{
  --ink:#1c2430; --sub:#54626f; --line:#d6dce4;
  --sea:#0f5d8c; --sea-l:#e7f1f8; --sun:#c25c19; --paper:#fcfbf8;
}
*{box-sizing:border-box;}
body{
  margin:0; background:#868d96; color:var(--ink);
  font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic UI","Yu Gothic",
              "Meiryo","Noto Sans JP",system-ui,sans-serif;
  font-size:20px; line-height:1.7;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3{margin:0; line-height:1.25;}
p{margin:0;}
a{color:inherit;}

/* A4 ちょうどのページ。中身は縦フレックスで詰める */
.page{
  width:210mm; height:297mm; margin:10mm auto; padding:15mm 14mm;
  background:var(--paper); box-shadow:0 4px 20px rgba(0,0,0,.32);
  position:relative; overflow:hidden;
  display:flex; flex-direction:column;
}

/* ---------- 表紙 ---------- */
.cover{padding:0; justify-content:flex-end;}
.cover-photo{position:absolute; inset:0; background:#3b4a58;}
.cover-photo img{width:100%; height:100%; object-fit:cover; color:transparent; font-size:0;}
.cover-veil{position:absolute; inset:0;
  background:linear-gradient(to bottom,rgba(9,28,48,.45) 0%,rgba(9,28,48,.08) 34%,
             rgba(7,22,38,.74) 70%,rgba(5,18,32,.93) 100%);}
.cover-text{position:relative; color:#fff; padding:0 18mm 24mm;}
.cover-eyebrow{font-size:23px; letter-spacing:.32em; font-weight:700; opacity:.93; margin-bottom:14px;}
.cover-title{font-size:64px; font-weight:800; letter-spacing:.02em;
             text-shadow:0 2px 16px rgba(0,0,0,.55);}
.cover-amp{font-size:38px; opacity:.8; padding:0 .12em;}
.cover-sub{font-size:29px; font-weight:600; margin-top:18px; opacity:.96;}
.cover-rule{width:110px; height:5px; background:#fff; opacity:.85; margin:26px 0 20px; border-radius:3px;}
.cover-for{font-size:23px; line-height:1.95; opacity:.96;}

/* ---------- 共通ヘッダ ---------- */
.phead{flex:0 0 auto; border-bottom:4px solid var(--sea); padding-bottom:11px; margin-bottom:16px;
       display:flex; align-items:flex-end; justify-content:space-between; gap:16px;}
.phead h2{font-size:32px; font-weight:800; color:var(--sea);}
.pnum{font-size:18px; color:var(--sub); font-weight:700; white-space:nowrap; padding-bottom:4px;}
.plead{flex:0 0 auto; font-size:21px; color:var(--sub); margin-bottom:10px;}

/* ---------- 行程一覧 ---------- */
.itin{flex:0 0 auto; width:100%; border-collapse:collapse;}
.itin td{padding:2px 12px; border-bottom:1px solid var(--line); vertical-align:middle;}
.itin th{padding:0 12px 4px; font-size:15px; color:var(--sub); text-align:left;
  font-weight:700; border-bottom:2px solid var(--line);}
.itin th.d-stay{text-align:right;}
.itin tr.japan{background:#fff3e6;}
.itin tr.stay{background:var(--sea-l);}
.d-date{font-weight:800; font-size:23px; white-space:nowrap; width:104px; color:var(--sea);}
.d-dow{font-size:16px; color:var(--sub); font-weight:700; width:30px; text-align:center;}
.d-place{font-weight:700; font-size:20px;}
.d-note{font-size:16px; color:var(--sub); line-height:1.4;}
.d-stay{font-size:14px; color:var(--sub); width:180px; line-height:1.35; text-align:right;}
.legend{flex:0 0 auto; margin-top:10px; font-size:17px; color:var(--sub);
        display:flex; gap:26px; flex-wrap:wrap;}
.legend span{display:flex; align-items:center; gap:9px;}
.chip{width:22px; height:12px; vertical-align:middle; border-radius:4px; border:1px solid var(--line); display:inline-block;}

/* ---------- 道順 ---------- */
.route{flex:0 0 auto; list-style:none; padding:0; margin:0;}
.route li{display:flex; gap:16px; padding-bottom:5px; position:relative;}
.route li:not(:last-child)::before{content:""; position:absolute; left:23px; top:48px; bottom:0;
  width:4px; background:var(--line); border-radius:2px;}
.bullet{flex:0 0 50px; height:50px; border-radius:50%; background:var(--sea); color:#fff;
  display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:800;
  position:relative; z-index:1;}
.route li.start .bullet{background:#2c7a4d;}
.route li.goal .bullet{background:var(--sun);}
.rbody{flex:1; min-width:0;}
.rtop{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;}
.rtime{font-size:17px; font-weight:800; color:var(--sun); white-space:nowrap;}
.rline{font-size:16px; color:#fff; background:var(--sea); display:inline-block;
  padding:2px 11px; border-radius:5px; font-weight:700;}
.route li.goal .rline{background:var(--sun);}
.rplace{font-size:22px; font-weight:800; margin:1px 0 2px;}
.rdetail{font-size:16px; line-height:1.55; color:var(--ink);}

.callout{flex:0 0 auto; background:var(--sea-l); border-left:9px solid var(--sea);
  padding:10px 18px; border-radius:0 8px 8px 0; font-size:16px; line-height:1.55;}
.callout b{color:var(--sea);}
.ctitle{font-size:21px; font-weight:800; color:var(--sea); margin-bottom:3px;}
.spacer{flex:1 1 auto; min-height:0;}

/* ---------- 観光地ページ ---------- */
.spot-day{display:inline-block; background:var(--sun); color:#fff; font-size:18px; font-weight:800;
  padding:3px 15px; border-radius:20px; margin-bottom:8px;}
.spot-name{font-size:44px; font-weight:800; color:var(--sea); line-height:1.12;}
.spot-local{font-size:17px; color:var(--sub); font-weight:700; letter-spacing:.1em; margin-top:5px;}
.spot-lead{flex:0 0 auto; font-size:21px; margin-bottom:14px; line-height:1.6;}

/* 写真グリッド：残りの高さをすべて写真が吸収する。
   説明は写真の上に重ねるので、写真の面積を一切削らない。 */
.grid{flex:1 1 auto; min-height:0; display:grid; grid-template-columns:1fr 1fr;
      grid-template-rows:1.5fr 1fr 1fr; gap:12px;}
figure{margin:0; border-radius:10px; overflow:hidden; position:relative;
  min-height:0; background:#e9edf1;}
figure.wide{grid-column:1 / -1;}
/* 写真が届かなかったとき（圏外・印刷前の読み込み失敗）にも体裁が崩れないよう、
   写真の下に薄い地とキャプション名を敷いておく。写真が出れば完全に隠れる。 */
.ph{position:absolute; inset:0;
  background:repeating-linear-gradient(45deg,#eef1f4,#eef1f4 12px,#e5eaef 12px,#e5eaef 24px);}
.ph::after{content:attr(data-label); position:absolute; inset:0; display:flex;
  align-items:center; justify-content:center; color:#93a0ac; font-size:15px; font-weight:700;
  text-align:center; padding:10px;}
.ph img{position:relative; z-index:1; width:100%; height:100%; object-fit:cover; display:block;
  color:transparent; font-size:0;}
figcaption{position:absolute; left:0; right:0; bottom:0; color:#fff;
  padding:26px 16px 12px;
  background:linear-gradient(to top,rgba(6,20,34,.88) 0%,rgba(6,20,34,.6) 55%,rgba(6,20,34,0) 100%);}
.cap-t{font-size:21px; font-weight:800; line-height:1.25; text-shadow:0 1px 4px rgba(0,0,0,.6);}
.cap-d{font-size:16px; line-height:1.45; margin-top:2px; opacity:.94;
  text-shadow:0 1px 4px rgba(0,0,0,.6);}
figure.wide .cap-t{font-size:25px;}
figure.wide .cap-d{font-size:18px;}

.tips{flex:0 0 auto; margin-top:12px; border-top:3px solid var(--line); padding-top:10px;}
.tips-h{font-size:19px; font-weight:800; color:var(--sun); margin-bottom:3px;}
.tips ul{margin:0; padding-left:1.25em; font-size:17px; line-height:1.55;}
.tips li{margin-bottom:2px;}

.foot{flex:0 0 auto; margin-top:12px; padding-top:10px; font-size:15px; color:#8a97a4;
      border-top:1px solid var(--line);}
.credits{flex:1 1 auto; min-height:0; overflow:hidden; margin:0; padding-left:1.2em;
         font-size:13px; line-height:1.6; color:var(--sub); word-break:break-word;}

@media print{
  body{background:#fff;}
  .page{margin:0; box-shadow:none; page-break-after:always; break-after:page;}
  .page:last-child{page-break-after:auto; break-after:auto;}
  @page{size:A4; margin:0;}
}
/* スマートフォンで見るとき。写真は position:absolute なので、
   figure 側に縦横比を与えないと高さが 0 に潰れてしまう。 */
@media screen and (max-width:820px){
  .page{width:auto; height:auto; margin:0 0 8px; padding:20px;}
  .grid{grid-template-columns:1fr; grid-template-rows:none; gap:14px;}
  figure{aspect-ratio:16/10; min-height:200px;}
  .cover{height:78vh; min-height:460px;}
  .cover-title{font-size:42px;}
  .cover-amp{font-size:28px;}
  .cover-sub{font-size:22px;}
  .cover-for{font-size:18px;}
  .cover-text{padding:0 22px 30px;}
  .phead h2{font-size:27px;}
  .spot-name{font-size:34px;}
}
"""


TOTAL = 3 + len(SPOTS) + 1


def esc(s):
    return html.escape(s, quote=True)


def photo_box(filename, width, label):
    return (f'<div class="ph" data-label="{esc(label)}">'
            f'<img src="{esc(thumb(filename, width))}" alt="{esc(label)}" loading="lazy"'
            f' data-file="{esc(filename)}">'
            f"</div>")


def build_cover():
    return f"""
<section class="page cover">
  <div class="cover-photo"><img src="{esc(thumb(COVER, 2000))}" alt="ドゥブロブニク旧市街" data-file="{esc(COVER)}"></div>
  <div class="cover-veil"></div>
  <div class="cover-text">
    <div class="cover-eyebrow">2026年9月</div>
    <h1 class="cover-title">クロアチア<span class="cover-amp">＆</span><br>スロベニア</h1>
    <div class="cover-sub">アドリア海と湖をめぐる 10日間</div>
    <div class="cover-rule"></div>
    <div class="cover-for">
      9月18日（金）〜 9月27日（日）<br>
      ドゥブロブニク ／ スプリト ／ プリトヴィッツェ<br>
      ザグレブ ／ リュブリャナ ／ ブレッド湖
    </div>
  </div>
</section>"""


def build_itinerary():
    rows = "".join(
        f'<tr class="{k}"><td class="d-date">{esc(d)}</td><td class="d-dow">{esc(w)}</td>'
        f'<td><div class="d-place">{esc(p)}</div><div class="d-note">{esc(n)}</div></td>'
        f'<td class="d-stay">{esc(stay)}</td></tr>'
        for d, w, p, n, stay, k in ITINERARY
    )
    return f"""
<section class="page">
  <div class="phead"><h2>ぜんたいの行程</h2><div class="pnum">2 / {TOTAL}</div></div>
  <p class="plead">9月18日から27日までの10日間。おおまかな流れです。</p>
  <table class="itin"><thead><tr><th colspan="3">日付と行き先</th><th class="d-stay">泊まる宿</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="spacer"></div>
  <div class="callout">
    <div class="ctitle">持ちものメモ</div>
    パスポート ／ 常備薬は多めに ／ 歩きやすい靴 ／ 薄手の上着（朝晩は15度ほど）<br>
    日本との時差は <b>7時間</b>（日本のほうが進んでいます）。
  </div>
  <div class="foot"><i class="chip" style="background:#fff3e6"></i> 日本国内　<i class="chip" style="background:#e7f1f8"></i> 同じ町に連泊し、観光が中心の日　／ 便名・時刻・宿は変わることがあります。</div>
</section>"""


def build_route():
    items = "".join(
        f'<li class="{s["kind"]}"><div class="bullet">{i}</div><div class="rbody">'
        f'<div class="rtop"><span class="rtime">{esc(s["time"])}</span>'
        f'<span class="rline">{esc(s["line"])}</span></div>'
        f'<div class="rplace">{esc(s["place"])}</div>'
        f'<div class="rdetail">{s["detail"]}</div></div></li>'
        for i, s in enumerate(ROUTE, 1)
    )
    return f"""
<section class="page">
  <div class="phead"><h2>9月18日（金）　香里園 → 不動前</h2><div class="pnum">3 / {TOTAL}</div></div>
  <p class="plead">東京へ移動して、息子の家に泊まります。旅行かばんはこの日から。</p>
  <ol class="route">{items}</ol>
  <div class="spacer"></div>
  <div class="callout">
    <div class="ctitle">これだけ覚えておけば大丈夫</div>
    ① 新幹線は <b>品川</b> で降りる（東京まで行かない）
    ② 品川から <b>山手線・内回り</b> で目黒（3つ目）
    ③ 目黒から <b>東急目黒線</b> で不動前（となり）<br>
    <b>不動前駅の改札は1か所だけ</b>なので、迷うことはありません。18時にそこで待っています。
    電車が遅れたときは、いつでも携帯に電話してください。<br>
    <b>翌9/19（土）は朝5時台に家を出ます。</b>8:00に成田空港で搭乗手続き、10:25 発です。
  </div>
  <div class="foot">※ 時刻は目安です。指定席が取れしだい、正確な列車名をお知らせします。</div>
</section>"""


def build_spot(spot, num):
    figs = "".join(
        f'<figure class="{"wide" if wide else ""}">'
        + photo_box(f, 1600 if wide else 1000, title)
        + f'<figcaption><div class="cap-t">{esc(title)}</div>'
          f'<div class="cap-d">{esc(cap)}</div></figcaption></figure>'
        for f, title, cap, wide in spot["photos"]
    )
    tips = "".join(f"<li>{esc(n)}</li>" for n in spot["notes"])
    return f"""
<section class="page">
  <div class="phead">
    <div>
      <div class="spot-day">{esc(spot["day"])}</div>
      <h2 class="spot-name">{esc(spot["name"])}</h2>
      <div class="spot-local">{esc(spot["name_local"])}</div>
    </div>
    <div class="pnum">{num} / {TOTAL}</div>
  </div>
  <p class="spot-lead">{esc(spot["lead"])}</p>
  <div class="grid">{figs}</div>
  <div class="tips"><div class="tips-h">歩きかたのヒント</div><ul>{tips}</ul></div>
</section>"""


def all_files():
    seen, out = set(), []
    for f in [COVER] + [p[0] for s in SPOTS for p in s["photos"]]:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def build_credits():
    rows = "".join(
        f'<li><a href="{esc(commons_page(f))}">{esc(f)}</a></li>' for f in all_files()
    )
    return f"""
<section class="page">
  <div class="phead"><h2>写真について</h2><div class="pnum">{TOTAL} / {TOTAL}</div></div>
  <p class="plead">
    掲載した写真はすべて、ウィキメディア・コモンズで自由な利用が認められている
    <b>実際に撮影された写真</b>です。AIで生成した画像は使っていません。
    撮影者とライセンスは、下のリンク先のページで確認できます。
  </p>
  <ul class="credits">{rows}</ul>
  <div class="foot">出典：Wikimedia Commons — https://commons.wikimedia.org/</div>
</section>"""


# 写真が読み込めなかったとき、黙って空白になるのではなく赤枠とファイル名を出すための部品。
# f-string の中に波括弧を書かなくて済むよう、定数として切り出してある。
FAIL_CSS = """
.imgfail{position:absolute; inset:0; background:#fdecea; border:2px dashed #c0392b;
  color:#8b1a10; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:8px; font-size:12px; line-height:1.4; gap:4px; word-break:break-all;}
.imgfail b{font-size:15px;}
.cover-photo .imgfail{border-width:4px;}
"""

FAIL_JS = """<script>
(function () {
  function fail(im) {
    if (im.dataset.failed) return;
    im.dataset.failed = "1";
    var d = document.createElement("div");
    d.className = "imgfail";
    d.innerHTML = "<b>写真が表示できません</b>";
    var n = document.createElement("small");
    n.textContent = im.dataset.file || im.alt || "";
    d.appendChild(n);
    im.parentNode.appendChild(d);
    im.style.visibility = "hidden";
  }
  document.querySelectorAll("img").forEach(function (im) {
    im.addEventListener("error", function () { fail(im); });
    if (im.complete && im.naturalWidth === 0) fail(im);
  });
})();
</script>"""


def build():
    parts = [build_cover(), build_itinerary(), build_route()]
    parts += [build_spot(s, 4 + i) for i, s in enumerate(SPOTS)]
    parts.append(build_credits())
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>クロアチア＆スロベニア 2026年9月｜旅のご案内</title>
<style>{CSS}{FAIL_CSS}</style>
</head>
<body>
{''.join(parts)}
{FAIL_JS}
</body>
</html>
"""


def localize():
    """写真をダウンロードして images/ に置き、ローカル参照版を出力する。"""
    import urllib.request

    imgdir = os.path.join(HERE, "images")
    os.makedirs(imgdir, exist_ok=True)
    doc = build()
    wanted = [(COVER, 2000)] + [
        (p[0], 1600 if p[3] else 1000) for s in SPOTS for p in s["photos"]
    ]
    for name, width in wanted:
        url = thumb(name, width)
        local = os.path.join(imgdir, f"{width}px-{name.replace(' ', '_')}")
        if not os.path.exists(local):
            print("取得:", url)
            req = urllib.request.Request(url, headers={"User-Agent": "croatia-guide/1.0 (personal)"})
            with urllib.request.urlopen(req) as r, open(local, "wb") as f:
                f.write(r.read())
        # ファイル名に ' を含む写真は doc 側で &#x27; に変換されているため、
        # エスケープ後の形でも置き換える（Diocletian's Palace など）
        ref = "images/" + os.path.basename(local)
        doc = doc.replace(esc(url), ref).replace(url, ref)
    out = os.path.join(HERE, "index_offline.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("出力:", out)


CHECK_OUT = os.path.join(HERE, "photo_check.html")


def all_photos():
    """資料で使っている写真を（ページ名, ファイル名, 見出し）の順に並べて返す。"""
    out = [("表紙", COVER, "表紙のドゥブロブニク")]
    for sp in SPOTS:
        for fn, cap, _sub, _big in sp["photos"]:
            out.append((sp["name"], fn, cap))
    seen, uniq = set(), []
    for item in out:
        if item[1] in seen:
            continue
        seen.add(item[1])
        uniq.append(item)
    return uniq



CHECK_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>写真チェック｜クロアチア＆スロベニア</title>
<style>
body{font-family:"Yu Gothic UI","Yu Gothic","Hiragino Sans","Noto Sans JP",sans-serif;
  margin:0; padding:24px; background:#f4f6f8; color:#1b2a38;}
h1{font-size:22px; margin:0 0 4px;}
p.lead{margin:0 0 16px; color:#5a6b7b; font-size:14px;}
#tally{position:sticky; top:0; z-index:5; background:#fff; border:2px solid #1b4f72;
  border-radius:10px; padding:12px 16px; font-size:17px; font-weight:700; margin-bottom:18px;}
#tally .ng{color:#c0392b;}
#tally .ok{color:#1e7a46;}
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:14px;}
.c{margin:0; background:#fff; border-radius:10px; overflow:hidden;
  box-shadow:0 1px 4px rgba(0,0,0,.12);}
.c .ph{position:relative; width:100%; aspect-ratio:4/3; background:#dfe5ea;}
.c img{width:100%; height:100%; object-fit:cover; display:block;}
figcaption{padding:8px 10px; font-size:12px; line-height:1.5;}
figcaption b{display:block; font-size:13px;}
figcaption .pg{display:block; color:#5a6b7b;}
figcaption a{color:#8a99a8; word-break:break-all; font-size:11px;}
.imgfail{position:absolute; inset:0; background:#fdecea; border:2px dashed #c0392b;
  color:#8b1a10; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:8px; font-size:11px; gap:4px; word-break:break-all;}
.imgfail b{font-size:14px;}
</style>
</head>
<body>
<h1>写真チェック</h1>
<p class="lead">資料で使う写真 __COUNT__ 枚です。すべて絵が出ていれば、そのまま印刷して大丈夫です。</p>
<div id="tally">読み込み中…</div>
<div class="grid">
__CARDS__
</div>
<script>
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll("img"));
  var bad = [];
  function render() {
    var t = document.getElementById("tally");
    if (bad.length === 0) {
      t.innerHTML = '<span class="ok">✓ ' + imgs.length + ' 枚すべて表示できました。</span>';
    } else {
      var head = bad.slice(0, 8).map(function (f) { return "・" + f; }).join("<br>");
      var rest = bad.length > 8 ? "<br>・ほか " + (bad.length - 8) + " 枚" : "";
      t.innerHTML = '<span class="ng">✕ ' + bad.length + ' 枚が表示できません：</span><br>'
        + '<span style="font-weight:400;font-size:13px">' + head + rest + '</span>';
    }
  }
  function fail(im) {
    if (im.dataset.failed) return;
    im.dataset.failed = "1";
    bad.push(im.dataset.file);
    var d = document.createElement("div");
    d.className = "imgfail";
    d.innerHTML = "<b>表示できません</b>";
    im.parentNode.appendChild(d);
    im.style.visibility = "hidden";
    render();
  }
  imgs.forEach(function (im) {
    im.addEventListener("error", function () { fail(im); });
    im.addEventListener("load", render);
    if (im.complete && im.naturalWidth === 0) fail(im);
  });
  render();
})();
</script>
</body>
</html>
"""


def build_check():
    """写真が全部ちゃんと表示できるかを、ブラウザで一目で確かめるためのページ。

    Python を動かさなくても、このファイルを開くだけで確認できる。
    """
    photos = all_photos()
    cards = []
    for i, (page_name, fn, cap) in enumerate(photos, 1):
        cards.append(
            f'<figure class="c"><div class="ph">'
            f'<img src="{esc(thumb(fn, 400))}" alt="{esc(cap)}" data-file="{esc(fn)}">'
            f'</div><figcaption><b>{i}. {esc(cap)}</b>'
            f'<span class="pg">{esc(page_name)}</span>'
            f'<a href="{esc(commons_page(fn))}" target="_blank">{esc(fn)}</a>'
            f"</figcaption></figure>"
        )
    return (CHECK_TEMPLATE
            .replace("__COUNT__", str(len(photos)))
            .replace("__CARDS__", "\n".join(cards)))


if __name__ == "__main__":
    if "--localize" in sys.argv:
        localize()
    else:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(build())
        print("出力:", OUT, f"（全{TOTAL}ページ）")
        with open(CHECK_OUT, "w", encoding="utf-8") as f:
            f.write(build_check())
        print("出力:", CHECK_OUT, "（写真の確認用）")
