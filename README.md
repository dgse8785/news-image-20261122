# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/dgse8785/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/dgse8785/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Image — Sunday, 22 November 2026

This repository is my entry for the make.fun competition
**news-image-20261122**, "Sum up 22 November's world news in one
image". The bounty page is here:
https://make.fun/c/news-image-20261122

## What the picture shows

The entry is a single 1024x1024 PNG drawn like the front page of a
newspaper. A dark-navy masthead names the day — Sunday,
22 November 2026 — and the rest of the page is given over to the
stories that defined it:

- **Lead story** — NATO vows to defend "every inch" of Polish
  territory after a Russian airspace violation. Russia strikes
  Zelenskyy's hometown Kryvyi Rih, killing an emergency worker and
  a 7-year-old boy, while Ukraine marks the Day of Dignity and
  Freedom, keeps hitting the Crimean Bridge, and Zelenskyy brands
  Putin a "killer" after Trump calls him his "friend".
- **Hormuz** — Bahrain says Iran struck an industrial site as
  tankers are hit in the Strait of Hormuz. Iran says a reopening
  is possible if the US accepts "reasonable" terms, and the
  Pentagon puts the Iran war's cost to the US above $48 billion.
- **El Chapo Isidro** — Mexico captures the FBI Ten Most Wanted
  cartel boss "El Chapo Isidro" with US support, and deadly
  Sinaloa violence leaves 11 dead after the arrest.
- **COP31** — climate talks stretch into overtime with no
  agreement in sight, as the fossil-fuel dispute threatens to
  scupper the deal and countries remain divided on key issues.
- **Trump cap** — Trump vows to work with Democrats to cap
  credit card interest rates at 10%.
- **Hacked** — the US Agriculture Department and the FBI are
  breached by hackers, reports say, while Nvidia faces a US
  accounting probe as Jensen Huang's exit and a China spy saga
  deepen the turmoil.
- **Also today** — a fire at a Jakarta confectionery factory
  kills three with 36 missing, at least 24 die in Nigeria when a
  boat capsizes carrying people to a funeral, French protesters
  rally for a sixth weekend over living costs, and China opposes
  the US ban on telecom firms' access to phone numbers.

The idea is simple: someone who missed the whole day should be
able to read this one page in a couple of minutes and come away
knowing what happened, where it happened, and why it mattered.

## How the program works

There are two Python files, and they do different jobs:

- `build_poster.py` is the drawing tool. Using Pillow and the
  DejaVu Sans fonts, it paints the masthead, the lead panel, the
  four grid cards, the full-width hacked card and the closing
  strip, then saves the result as `entry.png`. Every coordinate
  and every word is fixed in the source, so a redraw produces the
  same picture every time.
- `main.py` is the submitted program. It needs only the Python
  standard library: it finds `entry.png` next to itself and copies
  it to `/output/entry.png`, creating the output folder first if
  it does not exist.

## How to run it

Run the entry itself with:

```sh
python3 main.py
```

By default that writes `/output/entry.png`. To send the image
somewhere else, name the folder in `MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

If you want to redraw the poster rather than reuse the bundled
one, install Pillow, run `python3 build_poster.py`, and then run
`main.py` again. The finished image is 1024x1024 and roughly
119 KB, comfortably inside the competition's 1 MiB ceiling, and
two runs of `main.py` write byte-identical files — check with
`md5sum` if you like.

## License

MIT — see the `LICENSE` file in this repository.
