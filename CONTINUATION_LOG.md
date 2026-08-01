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

## 2026-08-01 — Crypt Forge: full piece roster, sound editing, music

Owner request: *"allow edit of all pieces, add pieces, edit select sound, move sound and match
sounds, edit gameplay music, add mute music button."*

**Forge (F2 on desktop · press-and-hold 🐞 for 700 ms on phone/APK)**

- **PIECES tab** — every relic's art, name, score value, **burst colour** and match SFX. New
  **＋ ADD RELIC** appends a brand-new piece type (`TYPES` is now a live value, not a constant);
  added relics can be deleted again, shipped ones cannot, and the roster floors at 4 types.
  Added relics spawn as soon as the board refills, drawing the vector fallback in their colour
  until art is dropped on them.
- **AUDIO tab (new)** — **SELECT**, **MOVE** and **DENIED** voices (empty = the shipped synth
  beep), the **gameplay music** controls, and an **imported sound bank**: drop in an mp3/ogg/wav
  and its name becomes usable in *every* SFX field, including as the music track.
- Forge export/import now carries imported audio as well as replaced art.

**Music**

- Gameplay music plays while a board is live and stops on the menus. Default is a built-in
  WebAudio "crypt dirge" (drone + sparse pentatonic plucks + heartbeat) with editable tempo, key
  and volume — no asset, so it costs the APK nothing. Any imported track can replace it.
- New **🎵 button** in the right-hand HUD column, with its own `bc_mute_music` setting — the
  existing 🔊 still controls sound effects only.

**Notes**

- The gem's layered glass-shatter is now conditional: it stays layered while its clip list is
  untouched, and behaves like any other relic once the Forge edits it.
- Regression coverage: `qa/test_forge.py` (headless Playwright — 6 tests, run with the packaging
  suite via `python -m pytest qa/ -q`). It caught a real load-order crash during this pass.
