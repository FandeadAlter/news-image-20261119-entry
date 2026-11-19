# news-image-20261119 entry

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/FandeadAlter/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/FandeadAlter/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun competition **news-image-20261119**: sum up
19 November 2026's world news in one image.

The image is a 1024x1024 newspaper front page, "THE WORLD —
Thursday 19 November 2026". Lead story: Grand Theft Auto VI begins
its global rollout, with gamers entering Vice City. Secondary
stories: Trump, Xi and Putin hold trilateral talks at the APEC
summit in Shenzhen; the US and Iran exchange fire in the Gulf; Nvidia
chief Jensen Huang resigns; Cyclone Akvan nears Andhra Pradesh. The
footer adds Voyager 1 reaching one light-day from Earth and the EU's
proposed 45 billion euro Ukraine loan. Sources: JagranJosh,
Education Times, SimpleLife.news.

## Files

- `draw_image.py` — draws the front page with PIL and saves
  `entry.png` (1024x1024, under 1 MiB).
- `main.py` — the entry program (Python standard library only).
  It copies `entry.png` to the output folder as `entry.png`.
- `entry.png` — the rendered image.

## Run

```sh
python3 draw_image.py   # regenerate entry.png
python3 main.py         # writes /output/entry.png
```

To write somewhere else instead of `/output`:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Running `main.py` twice produces byte-identical output.
