# Post-v0.50 continuation

## 2026-07-11 — Claude handoff completed

- Score flyers now pop at the crush, dip downward under gravity, and then travel to the upper-left score counter.
- Match scoring now uses per-relic values: Skull 20, Emerald gem 15, Black cat 13, Cauldron 12, Heart 15; the remaining relics stay at 10. The legend and rules match the actual scoring.
- Fingerjar glass-shatters the four board corners in sequence, then the centre.
- Megabone is a two-row horizontal sweep only.
- Hand is a top-to-bottom four-row claw drag.
- Key uses the voodoo-doll art and the supplied `sounds/wooden-doll.mp3` clip.

The pre-change rollback archives remain in `D:\Dev\GameBackups`.

## 2026-07-11 — Hand balance

- Hand now clears only board rows 1, 3, 5, and 7 (the one-indexed visible rows); it no longer clears an extra cell outside those rows.
- Its in-game power icon/label and the left legend now communicate that limit.
