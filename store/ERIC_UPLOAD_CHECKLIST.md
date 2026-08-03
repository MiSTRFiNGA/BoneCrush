# Eric — Skull Crush upload checklist (CM.7)

**Do this when ready. Agents stop here.**

## 1. Packages (fresh 2026-08-02)

| Platform | Artifact | How |
|---|---|---|
| **CrazyGames** | `D:\Dev\SkullCrush\dist\bonecrush-crazygames.zip` | Unzip → upload **folder contents** (CG rejects our zip as-is in past flow) |
| **Poki** | `D:\Dev\SkullCrush\dist\bonecrush-poki.zip` | Upload zip |

Rebuild anytime: `cd D:\Dev\SkullCrush && python build.py`

## 2. Art & video (all under `store/`)

- [ ] `cover_16x9.png` (1920×1080)
- [ ] `cover_2x3_800x1200.png` (800×1200)
- [ ] `cover_1x1_800x800.png` (800×800)
- [ ] `icon_512.png` / `thumb_720.png` as portal asks
- [ ] `preview_landscape_1080p.mp4` + `preview_portrait_1080p.mp4`

## 3. Copy

Paste from `store/SUBMISSION.md` (short/long description, controls).

## 4. Portal rules

- [ ] CrazyGames = **new listing** (not edit of rejected Basic Launch)
- [ ] Confirm public title (see `WHY_THIS_LISTING_DIFFERS.md`)
- [ ] Cold-open smoke: playable ≤1 click, `gameplayStart` fires

## 5. Read if needed

- `WHY_THIS_LISTING_DIFFERS.md` — why this isn’t the rejected build  
- `RELAUNCH_KIT.md` — full CG technical / KPI context  
- `SUBMISSION_STATUS_2026-08-01.md` — prior reconcile  

**No store submit by agents.**
