# The World in One Image — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Jo3st4r/news-image-20261119-bot/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Jo3st4r/news-image-20261119-bot/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for make.fun's **news-image-20261119** bounty:
https://make.fun/bounty/news-image-20261119

A front-page poster that sums up Thursday 19 November 2026's world news
in a single 1024×1024 image. Every headline on the page is drawn as real
text, so the story is readable from the image itself.

## What the image shows

- **THREE AT ONE TABLE** — Trump, Xi and Putin meet for the first
  trilateral summit of the three powers in Shenzhen, on the APEC
  sidelines. Nuclear arms on the agenda; no deal expected.
- **GTA VI ROLLS OUT** — the 13-year wait ends as the game unlocks
  worldwide at midnight local time, starting in New Zealand. Early
  reviews hit Metacritic 99.
- **ONE LIGHT-DAY FROM EARTH** — NASA confirms Voyager 1 is one
  light-day away, the first human-made object so far out. A radio
  signal now takes a full day to reach it.
- **AKVAN BEARS DOWN** — a severe cyclone closes on India's east coast.
  Red alerts, schools shut, landfall due 20 November.
- **ISLAM TO BE LARGEST FAITH** — Pew Research projects Muslims will
  outnumber Christians by 2035, driven by higher birth rates.
- **Also today** — Fed minutes point to more rate hikes; EU proposes a
  €45bn Ukraine loan; Democrats nominate Jeffries as first Black Speaker.

Sources (checked 19 Nov 2026): Chinese Foreign Ministry / The Hindu
BusinessLine, Reuters, AP, NASA/JPL, India Meteorological Department /
The Hindu, Pew Research Center / NDTV, Federal Reserve, Financial Times,
BBC.

## How it works

`main.py` (Python 3, standard library only) copies the vendored poster
`assets/entry.png` byte-for-byte to `/output/entry.png`. No network, no
clock, no randomness — two runs produce identical bytes.

The poster itself is drawn with code (Pillow) in `tools/render.py`:
flat-vector editorial style, real text throughout, no AI-generated imagery.

## Run it

```sh
python3 main.py        # writes /output/entry.png (1024x1024 PNG)
python3 main.py        # second run: byte-identical output
sha256sum /output/entry.png
```

## License

MIT — see `LICENSE`.
