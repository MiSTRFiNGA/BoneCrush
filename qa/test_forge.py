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


def test_forge_button_is_visible_and_opens_it(page):
    # The ⚱ button only shows on the owner's own builds (localhost / capacitor / ?forge) — a
    # portal player must never get a content editor. This fixture serves from 127.0.0.1.
    btn = page.locator("#forgeBtn")
    assert btn.is_visible()
    btn.dispatch_event("click")                 # title overlay covers the HUD on boot
    assert page.locator("#cf.on").count() == 1
    btn.dispatch_event("click")
    assert page.locator("#cf.on").count() == 0, "the button should toggle, not only open"


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


def test_clicking_a_relic_opens_the_sprite_editor(page):
    page.keyboard.press("F2")
    page.click('[data-cfart="p0"]')                      # skull thumbnail
    assert page.locator("#cfPaint").is_visible(), "sprite editor canvas should open"
    assert "Skull" in page.locator("#cf .bd").inner_text()
    for ctl in ("#cfCol", "#cfSize", "#cfErase", "#cfUndo", "#cfImp2", "#cfSpSave", "#cfDl"):
        assert page.locator(ctl).count() == 1, f"missing control {ctl}"
    # paint on it and save — the piece's live sprite must switch to the edited data URL
    box = page.locator("#cfPaint").bounding_box()
    page.mouse.move(box["x"] + 100, box["y"] + 100)
    page.mouse.down(); page.mouse.move(box["x"] + 180, box["y"] + 180); page.mouse.up()
    page.click("#cfSpSave")
    assert page.evaluate("SPRITES[0].src").startswith("data:image/png")
    assert page.evaluate("!!CM_ART.p0") is True
    # and revert puts the shipped PNG back
    page.on("dialog", lambda d: d.accept())
    page.click("#cfRev")
    assert page.evaluate("SPRITES[0].src").endswith("assets/skull.png")
    page.click("#cfSpBack")
    assert page.locator("#cfAdd").count() == 1, "back should return to the PIECES list"


def test_relic_art_also_opens_the_editor(page):
    page.keyboard.press("F2")
    page.locator("#cfT div", has_text="RELICS").click()
    page.click('[data-cfart="s0"]')
    assert page.locator("#cfPaint").is_visible()
    assert "Potion" in page.locator("#cf .bd").inner_text()


def test_title_screen_offers_the_three_modes(page):
    for btn in ("#tmCampaign", "#tmEndless", "#tmDaily"):
        assert page.locator(btn).is_visible(), f"{btn} should be on the title screen"
    page.locator("#tmEndless").dispatch_event("click")
    assert page.evaluate("MODE") == "endless"
    assert page.evaluate("playing") is True


def test_campaign_level_states_its_rules(page):
    # level 3 (index 2) is a 'drop' level — the one whose counter looks stuck without an explanation
    page.evaluate("() => { MODE='campaign'; campaignLevelIdx=2; start(); }")
    assert page.locator("#lvIntro").is_visible()
    txt = page.locator("#lvIntro").inner_text()
    assert "Drop" in txt and "bottom row" in txt
    assert "moves" in txt.lower()
    assert page.evaluate("busy") is True, "board must not take input under the rules card"
    page.locator("#lvIntro").dispatch_event("click")
    assert page.locator("#lvIntro").is_visible() is False
    assert page.evaluate("busy") is False
    # the big counter must not claim to be a score on a non-score level
    assert page.evaluate("document.getElementById('hud').textContent").startswith("⬇")


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
