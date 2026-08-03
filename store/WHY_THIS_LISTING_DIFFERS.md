# Why this Crypt Match listing differs from the rejected one

**Author:** Grok · **Date:** 2026-08-02 · **Row:** CM.7  
**Action for Eric:** upload only — do **not** ask an agent to submit.

---

## What failed last time (facts)

| Item | Rejected listing |
|---|---|
| Portal | CrazyGames **Basic Launch** |
| Public title | Crypt Match |
| Scores | Desktop **4/15**, Mobile **6/15** (need ≥9) |
| Death cause | **Quality KPIs** (playtime / D1 / conversion) — **not** zip size or file count |
| Resubmit rule | CG does **not** allow patching a rejected Basic Launch title — needs a **new game entry** |

Zip was already tiny (~1.4 MB / 47 files). Size was never the problem.

---

## What is different now (this kit)

1. **Fresh portal packages** rebuilt 2026-08-02 from `D:\Dev\CryptMatch`:
   - `dist/bonecrush-crazygames.zip` (~1.82 MB) — unzip and upload **extracted** playable for CG
   - `dist/bonecrush-poki.zip` (~1.82 MB) — Poki accepts zip upload
2. **Internal zip names** still use `bonecrush-*` (stable build id). Public title in portal metadata is still **your call** (Crypt Match vs Relic Rush / etc. — see `RELAUNCH_KIT.md` §3).
3. **Cover set checked** against common CG dimensions (2026-08-02):

| File | Size | Typical CG slot |
|---|---|---|
| `cover_16x9.png` | 1920×1080 | Landscape cover |
| `cover_2x3_800x1200.png` | 800×1200 | Portrait cover |
| `cover_1x1_800x800.png` | 800×800 | Square |
| `cover_4x3.png` | 1600×1200 | Alternate landscape |
| `icon_512.png` | 512×512 | Icon |
| `thumb_720.png` | 1280×720 | Thumbnail |
| `preview_landscape_1080p.mp4` | present | Landscape trailer |
| `preview_portrait_1080p.mp4` | present | Portrait trailer |

4. **Game/Forge work since rejection** lives in git (`21a15d1` store kit + Forge image-editor backports). This is not a re-upload of the same broken build folder.
5. **Cold-open / SDK** still your smoke check in portal QA: `gameplayStart` ≤1 click (see `RELAUNCH_KIT.md`).

---

## Explicitly unchanged / still Eric

- No agent will click Submit, create the CG listing, or change billing/store accounts.
- Final **public title** if “Crypt Match” remains spent on CG.
- KPI trial after Basic Launch (playtime 10+ min, D1 10%+, conversion 80%+ targets in kit docs).
