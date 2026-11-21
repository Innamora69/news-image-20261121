# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One picture that sums up Saturday 21 November 2026, drawn as a newspaper
front page: a masthead, then the lead story — Russia's mass drone-and-
missile strike on Ukraine, with missiles landing in Poland — followed by
four story cards: the AI sell-off dragging the S&P 500 into correction,
the ICJ ruling Myanmar guilty of genocide against the Rohingya, a
pancreatic-cancer trial pill making tumours undetectable in 1 of 12
patients, and the UK–EU signing its biggest post-Brexit deal. An "also
today" strip at the bottom covers the FBI database hack, Gen Z protests
in 25 EU states, the 6.9 quake in the Peruvian Andes, Indonesia's forest
fires, the Basra power-plant fire and the Palisades arson conviction.

## Files

- `draw.py` — renders `entry.png` (1024×1024, pure Pillow, no network,
  no randomness: every run draws the same bytes). Run `python3 draw.py`.
- `entry.png` — the image this entry ships.
- `main.ts` — entrypoint (Node 22, standard library only): checks the PNG
  is whole and inside the gates (≤1 MiB, ≤1024×1024), copies it to
  `/output/entry.png`, then verifies the copy byte for byte.

## Reproduce it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT (see LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w36tq042&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
