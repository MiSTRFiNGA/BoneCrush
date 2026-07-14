# Bone Crush — v0.50 baseline

**Baseline frozen:** 2026-07-11 (America/New_York)

## What is included

- Single-file HTML5 daily match-3 game with an ossuary/dirt visual theme, local art and sound assets, a test mode (`?test=1`), and debug hooks.
- Eight normal piece types: skull, crossbones, ribcage, femur, emerald gem, black cat, cauldron, and heart.
- Current special-piece system, animated score readout/flyers, score panel, and local asset/sound integration.

## Pending continuation from Claude

- Rework score flyers so they pop at the crush, dip under gravity, then travel to the score counter.
- Assign requested values: Skull 20, Emerald 15, Cat 13, Cauldron 12, Heart 15.
- Rework Fingerjar, Megabone, Hand, and Key/Voodoo special behavior and panel descriptions.

## Release position

- This is the protected pre-continuation baseline. The pending changes above were dispatched by Claude but were not applied before its session/credit limit was reached.
- Subsequent work must be tested and be reversible to the v0.50 backup.

## Primary files

- `index.html` — complete game source
- `assets/`, `sounds/`, `art_src/` — local game assets and sources
