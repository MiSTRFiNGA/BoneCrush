"""Headless checks for the Crypt Forge additions (piece roster, audio bank, music).

Covers what the 2026-07-31 forge pass added and what a syntax check can't see: that the editor
opens, that adding/removing a relic really moves TYPES on the live board, that an imported clip
becomes selectable everywhere, and that the music mute button is wired to its own setting.

    python -m pytest qa/test_forge.py -q          (needs: pip install playwright pytest)

Serves the game on a throwaway port — the Forge writes to localStorage, which file:// blocks.
"""
import http.server
import socketserver
import threading
import functools
import pathlib
import pytest

try:
    from playwright.sync_api import sync_playwright
except ImportError:                                     # keep the rest of the qa suite runnable
    pytest.skip("playwright not installed", allow_module_level=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8391


@pytest.fixture(scope="module")
def url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{PORT}/index.html"
    srv.shutdown()


@pytest.fixture
def page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(url)
        pg.wait_for_function("typeof TYPES !== 'undefined'")
        pg.errors = errors
        yield pg
        assert not errors, f"page errors: {errors}"
        browser.close()


def test_loads_clean_with_music_button(page):
    assert page.locator("#musicBtn").is_visible()
    assert page.evaluate("typeof music.sync") == "function"
    assert page.evaluate("TYPES") == 8


def test_music_mute_is_separate_from_sfx_mute(page):
    # dispatch_event, not click(): on boot the title-screen overlay covers the HUD, so a real
    # pointer click at those coordinates lands on the overlay. Harmless in play — music only runs
    # on a live board, where the overlay is gone — but it makes a synthetic click test the overlay.
    page.locator("#musicBtn").dispatch_event("click")
    assert page.evaluate("musicMuted") is True
    assert page.evaluate("muted") is False, "music button must not touch the SFX mute"
    assert page.evaluate("localStorage.bc_mute_music") == "1"
    page.locator("#musicBtn").dispatch_event("click")
    assert page.evaluate("musicMuted") is False


def test_forge_opens_and_has_an_audio_tab(page):
    page.keyboard.press("F2")
    assert page.locator("#cf.on").count() == 1
    tabs = page.locator("#cfT div").all_text_contents()
    assert tabs == ["PIECES", "RELICS", "LEVELS", "AUDIO", "DATA"]
    page.locator("#cfT div", has_text="AUDIO").click()
    assert page.locator('[data-cp="ui.pick"]').count() == 1     # select sound
    assert page.locator('[data-cp="ui.swap"]').count() == 1     # move sound
    assert page.locator('[data-cp="music.clip"]').count() == 1  # gameplay music


def test_add_and_delete_relic_moves_types(page):
    page.keyboard.press("F2")
    page.click("#cfAdd")
    assert page.evaluate("TYPES") == 9
    assert page.evaluate("[COLS.length, PIECE_VALUES.length, PIECE_SFX.length, SPRITES.length]") == [9] * 4
    page.on("dialog", lambda d: d.accept())
    page.click('[data-cfdel="8"]')
    assert page.evaluate("TYPES") == 8


def test_edited_piece_sound_and_ui_voice_take_effect(page):
    page.keyboard.press("F2")
    page.fill('[data-cp="pieces.0.sfx"]', "meow")
    page.locator("#cfT div", has_text="AUDIO").click()
    page.fill('[data-cp="ui.pick"]', "coins")
    assert page.evaluate("PIECE_SFX[0]") == ["meow"]
    assert page.evaluate("UI_SFX.pick") == ["coins"]
    # unknown names are dropped rather than silencing the event
    page.fill('[data-cp="ui.pick"]', "nope_not_a_clip")
    assert page.evaluate("UI_SFX.pick") == []


def test_imported_clip_registers_in_the_bank(page):
    # 1-frame silent wav — enough to prove the data-URL path registers a usable CLIPS entry
    page.evaluate("""() => {
      CM_AUD.testclip = { src:'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=', vol:.5 };
      cmSaveAud(); cmApply();
    }""")
    assert page.evaluate("!!CLIPS.testclip") is True
    page.evaluate("() => { CEDIT.music.clip = 'testclip'; cmSave(); cmApply(); }")
    assert page.evaluate("MUSIC_CFG.src").startswith("data:audio/wav")
    page.evaluate("() => { delete CM_AUD.testclip; CEDIT.music.clip=''; cmSaveAud(); cmSave(); cmApply(); }")
    assert page.evaluate("!!CLIPS.testclip") is False
