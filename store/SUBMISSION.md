# 📦 Skull Crush — NEW LISTING store submission pack (copy-paste ready)

**Author:** Grok · **Date:** 2026-07-30 (Order #3 Job 4)  
**Scope:** new-listing metadata / art-spec / checklist only. **Do NOT open or edit `index.html`.**  
**Why new listing:** CrazyGames Basic Launch already rejected “Skull Crush” (desktop 4/15, mobile 6/15; need ≥9).  
**Hard CG rule:** a failed title **cannot be patched and resubmitted** — it must return as a **new game** with a new listing. The old listing is spent.

Sources: campaign curve in `campaign_curve_40.json`; size audit in `store/RELAUNCH_KIT.md`; Skull Drift format mirror.

---

## Upload reality (Eric)

| Platform | How to upload |
|----------|----------------|
| **CrazyGames** | **Rejects zips from us.** Eric uploads the **extracted** playable (`index.html` + relative assets from the CG build folder), not the zip. |
| **Poki** | Accepts **`dist/bonecrush-poki.zip`**. |

Build (after Claude’s campaign/cold-open land):

```bat
cd /d D:\Dev\SkullCrush
python build.py
```

Prior measurement (2026-07-30, pre-final content): CG zip **1.44 MB / 47 files** — size is **not** the failure mode; KPIs were.

---

## New title treatment / name candidates

Old name **“Skull Crush” is spent** on CG. Listing must read as a **genuinely new game**, not “Skull Crush 2”.

| # | Candidate | Why |
|---|-----------|-----|
| 1 | **Skull Crush** | Clear match-3 genre signal; short; store-safe. **Recommended default.** |
| 2 | **Relic Rush** | Urgency + collectible fantasy; stronger “action energy.” |
| 3 | **Graveyard Gems** | Distinctive; match-3 readable at a glance. |
| 4 | **Bone Cabinet** | Weird-brand fit for art direction; less SEO-obvious. |
| 5 | **Ossuary Puzzle** | Premium/dark; may read slower for younger players. |

**Internal repo folder** renamed to `D:\Dev\SkullCrush` (2026-08-01). GitHub remote may still be `BoneCrush`.  
**Logo lockup:** new wordmark only — do **not** reuse the rejected listing’s exact title treatment.

---

## Tagline (short)

Match cursed relics. Clear the crypt. Dig forever.

## Short description (~160–200 chars)

> Match cursed relics in an 8×8 crypt. Clear **40 campaign levels**, chain specials, chase **endless** high scores, and claim **daily rewards** — dark match-3, one tap to play.

## Long description (paste-ready)

```
The crypt is open. The relics want out.

Skull Crush is a dark match-3 built for quick sessions and deep campaigns:

• Cold-open into the first board — play in one tap
• 40-level campaign with score, clear, drop, and crypt-tile goals
• Specials unlock as you dig deeper (jars, bones, hands, voodoo)
• Endless mode for high scores after the campaign
• Daily login rewards and quests so there’s always a reason to return

No downloads. No accounts required to start. Works on desktop and mobile browsers.

Tips: chain matches for multipliers, save specials for packed boards, and chase three-star clears to open chests.
```

*(If Eric picks another title, replace “Skull Crush” in the first body sentence only; keep feature bullets.)*

## Controls text

**Desktop:** Click or drag a relic to swap with a neighbor (4 directions). Make lines of 3+. Specials activate when matched or tapped per on-screen hints. Esc / menu opens pause.

**Mobile:** Tap a relic, then tap an adjacent relic to swap — or swipe to swap. Tap specials to fire. Use the on-screen menu for pause / restart.

**Portal one-liner:** Swap adjacent relics to match 3+. Specials clear bigger groups. One tap to start.

## Category / tags

- **Primary genre:** Puzzle / Match-3  
- **Tags:** match-3, puzzle, dark, gothic, campaign, casual, mobile-friendly, free, single-player, endless, daily-rewards, crypt, relics  

## Age rating answers

| Topic | Answer |
|-------|--------|
| Violence | None (puzzle; stylized bones/skulls as candy-like pieces) |
| Gore | No — cartoon ossuary aesthetic, not realistic |
| Chat / UGC | None |
| Gambling | None (optional daily rewards are cosmetic/progression, not real money) |
| Suggested | Everyone / all ages (stylized cartoon bones) |

## Technical answers

- Engine: custom HTML5 Canvas (vanilla JS)  
- Save: localStorage  
- Orientation: responsive; desktop landscape OK; mobile touch required  
- SDK: CrazyGames HTML5 SDK v3 + Poki via `build.py` injection (`<!-- PLATFORM_SDK -->`)  
- Self-contained assets; relative paths only  

---

## Cover-art SPEC (sizes + what to depict — do not generate here)

| File | Pixels | Aspect | Depict |
|------|--------|--------|--------|
| `store/cover_16x9.png` | **1920×1080** | 16:9 | Dark crypt chamber, 8×8 board of glowing relics (skulls, gems, cauldrons) mid-match with a big special burst; violet/teal rim light; **new title logo** right or lower third; high contrast for thumbnails. |
| `store/cover_2x3_800x1200.png` | **800×1200** | 2:3 portrait | Vertical hero: board dominant, cascading matches, logo top; readable at phone size. |
| `store/cover_1x1_800x800.png` | **800×800** | 1:1 | Iconic single relic (skull or emerald) + logo; works at 100px. |

**Optional:** `cover_4x3.png` 800×600 · `icon_512.png` · landscape + portrait **15s** H.264 **no-audio** preview (hook match → special → campaign goal → end card with **new title**).

**Rules:** Do not reuse rejected “Skull Crush” lockup. No stolen IP. Safe margin ~5% from edges.

---

## Submission checklist (new game entry)

### Process

- [ ] Create a **new** game in CG developer portal (do **not** patch the failed Skull Crush listing)
- [ ] Eric picks final title from candidates above
- [ ] Claude cold-open + 40-level curve + progression confirmed in playable build
- [ ] `python build.py` fresh artifacts
- [ ] **CG:** upload **extracted** `index.html` tree (zip rejected)
- [ ] **Poki:** upload zip OK
- [ ] Paste short/long description, controls, tags, age answers from this file
- [ ] Upload 3 covers (+ previews when ready)
- [ ] Portal QA (below) → Basic Launch → watch KPIs

### CrazyGames QA / product gates

- [ ] ≤ **1 click** to gameplay (cold-open Level 1)
- [ ] `gameplayStart` when board is interactive (measures initial download)
- [ ] Size ≤ **50 MB** Basic / ≤ **20 MB** mobile homepage (last measure 1.44 MB)
- [ ] File count ≤ **1500** (last measure 47)
- [ ] Chrome + Edge; touch swap works; readable at ~800×450 iframe
- [ ] No absolute paths / external required assets
- [ ] Campaign **40 levels** reachable in meta; endless + daily rewards visible in store copy and game

### KPI reminder (why relaunch exists)

| Metric | Prior fail signal | Target band |
|--------|-------------------|-------------|
| Trial score | Desktop 4/15, Mobile 6/15 | ≥ 9 |
| Conversion (still playing @ 60s) | Weak | **80%+** |
| Playtime | Weak | **10+ min** |
| D1 retention | Weak | **10%+** |

Curve design for conversion: levels 1–5 nearly unloseable (`campaign_curve_40.json`).

---

## Handoff

| Who | Does |
|-----|------|
| **Grok** | New-listing kit (this file + `RELAUNCH_KIT.md` size audit) |
| **Claude** | `index.html` campaign / cold-open / SDK timing (do not touch from this lane) |
| **Eric** | Final title, covers/trailer, **new** CG listing, extracted upload, submit |

See also: `store/RELAUNCH_KIT.md` for full technical table and zip measurement commands.
