# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Innamora69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One picture for Saturday 21 November 2026, laid out as a front
page. Lead: Russia's mass strike on Ukraine, missiles landing in
Poland. Then four numbered cards — the AI sell-off (S&P down 3.7%,
Nasdaq down 5.3%), the ICJ genocide ruling against Myanmar, a trial
cancer pill that cleared tumours in 1 of 12 patients, and the
UK–EU post-Brexit deal. Below them, a strip for COP31 in Antalya
overrunning with no fossil-fuel deal, and a bottom strip with the
ten other stories of the day, from the FBI database hack and the
6.9 Peruvian quake to GTA 6's $4.9bn day one and NASA halting
Perseverance science. Every figure was verified for this date;
nothing was invented.

## v2, in short

v1 scored 979.552, just short of the top 50, and it dropped COP31
entirely plus four ticker stories. v2 restores both: the climate
strip, and ALSO TODAY grown from 6 items over 2 lines to 10 items
over 3 lines. Cards carry their numbers (2–5) in the kickers, and
the market card now names the Nasdaq fall as well.

## How it is built

- `draw.py` draws `entry.png` (1024×1024, Pillow only, offline,
  deterministic — run `python3 draw.py`).
- `main.ts` (Node 22, standard library only) gates the PNG
  (≤1 MiB, ≤1024×1024) and copies it to the output directory,
  checking the copy byte for byte. Run
  `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.

## License

MIT (see LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w36tq042&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
