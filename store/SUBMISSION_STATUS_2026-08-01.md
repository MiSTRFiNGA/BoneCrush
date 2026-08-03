# Skull Crush — store submission status (reconcile)

**Author:** Grok · **Date:** 2026-08-01 · **Task:** MASTER_TODO CM.4  
**Sources:** `store/SUBMISSION.md`, `store/RELAUNCH_KIT.md`, live files under `store/`, Desktop packages

---

## What is actually on disk (live assets)

| Asset | Path | Status |
|---|---|---|
| CG / Poki build script | `build.py` | ✅ present (zip names still `bonecrush-*.zip` — portal-safe internal id) |
| Cover 16:9 | `store/cover_16x9.png` | ✅ untracked in git but present |
| Cover 2:3 portrait | `store/cover_2x3_800x1200.png` | ✅ |
| Cover 1:1 | `store/cover_1x1_800x800.png` | ✅ |
| Cover 4:3 | `store/cover_4x3.png` | ✅ |
| Icon 512 | `store/icon_512.png` | ✅ |
| Thumb 720 | `store/thumb_720.png` | ✅ |
| Preview landscape 1080p | `store/preview_landscape_1080p.mp4` | ✅ |
| Preview portrait 1080p | `store/preview_portrait_1080p.mp4` | ✅ |
| APK | `C:\Users\MiSTRFiNGA\Desktop\My Games\_APKs\SkullCrush-1.3.apk` | ✅ built |
| Desktop CG/Poki zips (older name) | `Desktop\Games\Bone Crush\bonecrush-*.zip` | ⚠️ legacy package name |
| Dev folder | **`D:\Dev\SkullCrush`** (renamed from BoneCrush 2026-08-01) | ✅ |

---

## Portal state (from kit docs — Eric owns the portal UI)

| Platform | Status | What's left for Eric |
|---|---|---|
| **CrazyGames** | Prior **Basic Launch rejected** (“Skull Crush”, desktop 4/15, mobile 6/15; need ≥9). **Cannot patch that listing** — must submit a **new game** entry. | 1) New portal entry with a **new public title** if still desired (kit listed Relic Rush / Graveyard Gems / …). 2) Upload **extracted** playable (CG rejects zip from us). 3) Paste metadata from `SUBMISSION.md`. 4) Attach covers + both preview videos. 5) Confirm cold-open fires `gameplayStart` ≤1 click. |
| **Poki** | Zip path ready (`dist/bonecrush-poki.zip` after `python build.py`) | Upload zip + metadata; no CG-style “spent name” rule known. |
| **Mobile APK** | SkullCrush-1.3.apk on Desktop | Sideload / store packaging separate from portals. |

---

## Checklist — still to submit (actionable)

1. [ ] Rebuild portal packages from **`D:\Dev\SkullCrush`**: `python build.py` (update SUBMISSION.md path from BoneCrush).  
2. [ ] **CrazyGames new listing** (not a resubmit of the rejected one).  
3. [ ] Confirm Eric’s final **public title** (Skull Crush vs alternate).  
4. [ ] Upload covers: 16:9, portrait, square (all present under `store/`).  
5. [ ] Upload preview videos landscape + portrait (present).  
6. [ ] Paste short/long description + controls from `SUBMISSION.md`.  
7. [ ] Poki: upload `dist/bonecrush-poki.zip` (or rename zips to SkullCrush if Eric wants brand match).  
8. [ ] After CG trial: watch playtime / D1 / conversion KPIs (rejection was quality KPIs, not size).

---

## Not blockers anymore

- File size / count (1.44 MB / 47 files — well under CG limits).  
- Forge discoverability (F2 + ⚱ + 700 ms hold on 🐞 — verified in code + `qa/test_forge.py` 11 passed).  
- Folder rename: **`D:\Dev\SkullCrush`**.

---

## VERIFIED

- Read `store/SUBMISSION.md` + `store/RELAUNCH_KIT.md`  
- Listed `store/` art + videos present  
- APK path confirmed on Desktop  
- **No portal API call made** — Eric’s Brave/CG account is the live source of “is it live?”
