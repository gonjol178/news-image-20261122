# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/gonjol178/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/gonjol178/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page broadsheet summing up the world's news of **Sunday, 22 November 2026** — "The Daily Meridian", in an oxblood broadsheet design: the lead story as a full-width band across the top with a wide photo panel, secondary stories in two columns below, and an IN BRIEF strip at the foot.

## The day in one page

- **Antalya, Turkey (lead):** COP31 ends with no deal — the UN climate summit closes with no agreement, the longest on record, after the EU and about 130 parties reject a draft that never mentions fossil fuels.
- **Bahrain:** Iran strikes a Bahrain industrial site, injuring two people; Gulf states condemn the attack.
- **Dymer, Ukraine:** A Russian drone partly collapses a five-storey apartment block north of Kyiv; 14 people are unaccounted for.
- **Sinaloa, Mexico:** Cartel boss "El Chapo Isidro" captured in Guasave; 11 killed, including four soldiers.
- **Washington:** Democrats win their largest House majority since 1992, securing at least 258 seats.
- **New York:** Stocks slide as the AI sell-off deepens — the S&P 500 falls 3.7%, Japan's Nikkei 5.06%.
- **In brief:** BepiColombo enters orbit around Mercury; a candy factory fire in Banten, Indonesia leaves 3 dead and dozens missing; the FBI investigates an apparent breach of its National Crime Information Center database; Trump calls the missiles and drone landing in Poland a "mistake" while PM Tusk calls it a provocation.

Sources: One Turn News, The Augerton Digest, AP, Reuters, BBC, NPR.

## How it is built

- `build_meridian.py` composes `entry.png` (1024×1024) from three photo panels generated in-session (`assets/`) plus typeset headlines in an oxblood broadsheet design. Run it with `python3 build_meridian.py`.
- `main.py` (Python 3.13, standard library only) is the entrypoint the grader runs: it copies the composed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. It runs with no network and writes identical bytes on every run.
- The three photo panels are original images generated for this entry: the COP31 plenary hall in Antalya, the Manama skyline at dusk, and a damaged apartment block in Dymer.

## Run it

```sh
python3 build_meridian.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Entry

- Competition: [news-image-20261122](https://make.fun/bounty/news-image-20261122) — entries close 2026-11-24T00:00:00Z; $100 in prizes shared by the top 50 entries.
- License: MIT (see `LICENSE`).

---

Entered on [make.fun](https://make.fun/?ref=1k4fvxxj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards
