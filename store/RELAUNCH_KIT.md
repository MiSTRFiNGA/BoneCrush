# Bone Crush — CrazyGames Relaunch Kit

**Author:** Grok · **Date:** 2026-07-30  
**Scope:** submission / metadata / infra only — **no `index.html` edits** (Claude owns game rebuild).  
**Why new listing:** CG Basic Launch already rejected “Bone Crush”; a failed title **cannot be patched and resubmitted** — it must return as a **new game**.

Sources: [CG Technical requirements](https://docs.crazygames.com/requirements/technical/), [Gameplay requirements](https://docs.crazygames.com/requirements/gameplay/), [Getting to first frame](https://docs.crazygames.com/resources/getting-to-the-first-frame/), FAQ submission flow.

---

## 1. CrazyGames submission checklist (actual requirements)

### Technical — file size & count

| Rule | Limit | Current CG zip | Pass? |
|------|-------|----------------|-------|
| Initial download (Basic, with SDK) | ≤ **50 MB** to `gameplayStart` | **1.44 MB** zip / **1.53 MB** uncompressed | ✅ |
| **Mobile homepage** eligibility | Initial download ≤ **20 MB** | 1.44 MB | ✅ |
| Total file size (Basic, no SDK path) | ≤ 50 MB (250 MB Full w/ SDK host rules) | 1.53 MB | ✅ |
| File count | ≤ **1500** | **47** files in zip | ✅ |
| Paths | **Relative only** (no absolute) | `build.py` packs relative `assets/`, `sounds/` | ✅ verify in QA |
| Externally hosted assets | Load-to-playable ≤ **20 s** | N/A if fully self-contained (current) | ✅ |

### Technical — device / browser

| Rule | Notes | Owner |
|------|-------|-------|
| Chrome + Edge required | Safari breakage → disabled on Safari | Claude smoke |
| Chromebook / 4 GB RAM | Must stay smooth or disabled on CrOS | Keep single-file + few assets |
| Mouse + keyboard + **touch** if mobile | Match-3 needs reliable touch | Claude |
| Landscape OK on desktop; portrait OK if mobile-friendly | Configure orientation in CG portal | Eric on submit |
| Mobile: `user-select: none` on `body` | Prevents magnifier / select menu | Claude CSS |
| iOS AudioContext resume on gesture | If WebAudio used | Claude if needed |

### SDK (Basic Launch vs Full)

| Item | Basic | Full | Current build |
|------|-------|------|----------------|
| SDK script | Optional | **Required** | Injected by `build.py` (v3) |
| `gameplayStart` when **playable** (not menu-only) | Required **if** SDK present (measures initial download) | Required | `PSDK.start()` wired — **confirm cold-open path fires it ≤1 click** |
| `gameplayStop` | — | Required | Present |
| Ads | **Disabled** on Basic even if integrated | Allowed per policy | midgame helper present; fine for Full later |
| `loadingStop` | Recommended | Recommended | `PSDK.loaded()` present |

### Gameplay / product (submission quality)

| Rule | Implication for relaunch |
|------|---------------------------|
| ≤ **1 click** to gameplay | Cold-open into Level 1 (Claude rebuild) — no multi-screen wall |
| Load quickly, no crashes | 1.5 MB helps; fire `gameplayStart` as soon as board is interactive |
| Readable at 800×450 mobile iframe | UI scale check |
| Original name / assets | **New title required** — old “Bone Crush” is spent |
| Cover art + trailer | Still required for portal (Eric assets) |

### Process reality (Eric)

1. New game entry in CG developer portal (not a patch of the rejected listing).  
2. Upload `dist/bonecrush-crazygames.zip` (or rebuilt after Claude’s campaign land).  
3. Metadata + covers + controls text (below).  
4. QA → Basic Launch → trial KPIs (playtime / D1 / conversion).  
5. Only after Full Launch: ads + full SDK modules.

**KPI reminder (why the rebuild exists):** rejected Desktop 4/15, Mobile 6/15; conversion = still playing after **60s**; targets playtime **10+ min**, D1 **10%+**, conversion **80%+**. Math tables: `campaign_curve_40.json`.

---

## 2. Current bundle measurement (2026-07-30)

Rebuilt with `python build.py` from `D:\Dev\BoneCrush`.

| Artifact | On-disk size | Files | Uncompressed |
|----------|--------------|-------|--------------|
| `dist/bonecrush-crazygames.zip` | **1,440,655 B (1.37 MiB / 1.44 MB)** | **47** | 1.53 MB |
| `dist/bonecrush-poki.zip` | 1,440,574 B | 47 | 1.53 MB |

Largest entries (CG zip): `sounds/evil_laugh_over.mp3` ~253 KB, `assets/title_logo.jpg` ~100 KB, `index.html` ~90 KB.

### Verdict

| Gate | Result |
|------|--------|
| Basic Launch size (≤50 MB) | **PASS** (huge margin) |
| Mobile homepage (≤20 MB) | **PASS** |
| File count (≤1500) | **PASS** (47) |
| Size is **not** the reason the old listing died | Correct — KPIs (conversion / D1 / playtime) killed it |

After Claude lands campaign + cold-open, **re-run** `python build.py` and re-check that `gameplayStart` still fires on first interactive frame (SDK initial-download measurement).

---

## 3. New-listing metadata

### Title candidates (old name is spent)

1. **Crypt Match** — clear genre signal; short; store-safe.  
2. **Relic Rush** — urgency + collectible fantasy; good for conversion copy.  
3. **Graveyard Gems** — distinctive; match-3 readable.  
4. **Bone Cabinet** — slightly weirder brand; fits art direction.  
5. **Ossuary Puzzle** — premium/dark; may read slower for kids.

**Recommendation:** ship as **Crypt Match** (or **Relic Rush** if Eric wants more action energy). Keep “Bone Crush” only as internal repo/folder name until rename is intentional.

### Short description (≤ ~160–200 chars, portal blurb)

> Match cursed relics in an 8×8 crypt. Clear 40 campaign levels, chain specials, and dig endless runs — dark match-3 you can play in one tap.

### Long description (store page)

```
The crypt is open. The relics want out.

Crypt Match is a dark match-3 built for quick sessions and deep campaigns:
• Cold-open into the first board — play in one tap
• 40-level campaign with score, clear, drop, and crypt-tile goals
• Specials unlock as you dig deeper (jars, bones, hands, voodoo)
• Endless mode for high scores after the campaign
• Daily login rewards and quests so there’s always a reason to return

No downloads, no accounts required to start. Works on desktop and mobile browsers.

Tips: chain matches for multipliers, save specials for packed boards, and chase three-star clears to open chests.
```

### Controls text

**Desktop:** Click or drag a relic to swap with a neighbor (4 directions). Make lines of 3+. Specials activate when matched or tapped per on-screen hints. Esc / menu button opens pause.

**Mobile:** Tap a relic, then tap an adjacent relic to swap — or swipe to swap. Tap specials to fire. Use the on-screen menu for pause / restart.

### Tags / genre

- **Primary genre:** Puzzle / Match-3  
- **Tags:** match-3, puzzle, dark, gothic, campaign, casual, mobile-friendly, free, single-player, endless  
- **Similar feel (for Eric’s notes only, not copy-paste competitors):** dark jewel matchers, crypt/loot aesthetics  

### Cover / trailer checklist (Eric art pass)

- Cover stills at CG required sizes (see gameplay requirements: mobile 800×450 class art; portal will list exact upload slots).  
- Short vertical + landscape trailer: 0–3s hook (big match + special), 3–15s campaign goal, end card with **new title**.  
- Do **not** reuse the rejected listing’s exact title lockup.

---

## 4. Build / upload commands

```bat
cd /d D:\Dev\BoneCrush
python build.py
:: Upload: dist\bonecrush-crazygames.zip
:: Poki mirror: dist\bonecrush-poki.zip
```

SDK snippets live in `build.py` (CrazyGames HTML5 SDK v3 + Poki v2). Marker in HTML: `<!-- PLATFORM_SDK -->`.

---

## 5. Handoff

| Who | Does |
|-----|------|
| **Claude** | Cold-open, 40-level curve apply, progression, `gameplayStart` timing, no multi-click wall |
| **Grok** | This kit + bundle measurement (done) |
| **Eric** | Pick final title, covers/trailer, create **new** CG game listing, submit zip |

When Claude’s rebuild lands: re-run measurement section, update zip sizes if assets grow, confirm mobile homepage still &lt; 20 MB (should).
