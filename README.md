# The World in One Day — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the [make.fun bounty "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121).

## What it draws

One newspaper front page for Saturday 21 November 2026: the date in giant type,
six numbers that tell the day at a glance, a region bar, three illustrated lead
stories, ten smaller illustrated cards, a world map, and 22 more stories in a
numbered list — 35 stories in all, across 7 regions.

## The v3 rule: Saturday only

Every story on the page happened, or was first reported, on Saturday 21
November 2026. Friday's news is named in the DATE CHECK box as left out: the
Russian barrage on Kyiv, the missiles that landed in Poland, Wall Street's
slide into correction, the UK–EU deal, the ICJ Myanmar ruling, and Cyclone
Akvan's landfall. GTA VI launched on Thursday, so it is out too.

## How to run

```sh
python3 draw.py        # writes entry.png (1024x1024, deterministic)
node main.ts           # draws twice, checks the bytes match, writes /output/entry.png
```

`draw.py` uses only Pillow and the DejaVu fonts, draws everything in code, and
needs no network. `main.ts` is the entrypoint: it runs the drawing twice and
refuses to publish unless both runs produce identical bytes.
