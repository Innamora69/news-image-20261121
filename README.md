# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image summing up the world's news of Saturday 21 November 2026, drawn
as a newspaper front page: a lead strip on Russia's mass drone-and-missile
strike on Ukraine, with missiles landing in Poland, plus the AI sell-off
pushing the S&P 500 into correction, the ICJ finding Myanmar guilty of
genocide against the Rohingya, a pancreatic-cancer trial pill making tumours
undetectable in 1 in 12 patients, the UK–EU signing its biggest post-Brexit
deal — and an "also today" ticker with the FBI database hack, Gen Z protests
across 25 EU states, the Peru quake, Indonesia's forest fires, the Basra
plant fire, the Palisades arson conviction, Bayer's $7.25bn Roundup payout
and GTA 6's ~$4.9bn day one.

## Files

- `draw.py` — draws `entry.png` (1024×1024, Pillow, no network, no
  randomness: same run, same bytes). Run `python3 draw.py`.
- `entry.png` — the image the entry ships.
- `main.ts` — entrypoint (Node 22, stdlib only): validates the PNG (whole
  file, ≤1 MiB, ≤1024×1024), copies it to `/output/entry.png` and
  verifies the copy byte for byte.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT (see LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w36tq042&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
