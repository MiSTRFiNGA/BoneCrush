from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(r"C:\Users\MiSTRFiNGA\Desktop\Tests\skullcrush-cm8")
out.mkdir(parents=True, exist_ok=True)
url = "http://127.0.0.1:8793/index.html?forge=1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 900, "height": 1100})
    page.goto(url, wait_until="load", timeout=30000)
    page.wait_for_timeout(800)
    page.keyboard.press("F2")
    page.wait_for_timeout(500)
    page.evaluate(
        """() => {
      const tabs = [...document.querySelectorAll('#cf .tabs div')];
      const a = tabs.find(t => /AUDIO/i.test(t.textContent || ''));
      if (a) a.click();
    }"""
    )
    page.wait_for_timeout(400)
    info = page.evaluate(
        """() => {
      const multi = document.querySelectorAll('#cf select[multiple]').length;
      const singles = document.querySelectorAll('#cf select:not([multiple])').length;
      const up = !!document.querySelector('#cfSndAdd');
      const sel = document.querySelector('#cf select[multiple]');
      const opts = sel ? sel.options.length : 0;
      const text = document.querySelector('#cfB')?.innerText || '';
      return {
        multi, singles, up, opts,
        hasCM8: /CM\\.8|UPLOAD SOUND/i.test(text),
        title: document.querySelector('#cf h3')?.textContent || ''
      };
    }"""
    )
    print("forge", info)
    page.screenshot(path=str(out / "cm8_audio_tab.png"), full_page=True)
    page.evaluate(
        """() => {
      const tabs = [...document.querySelectorAll('#cf .tabs div')];
      const a = tabs.find(t => /PIECES/i.test(t.textContent || ''));
      if (a) a.click();
    }"""
    )
    page.wait_for_timeout(300)
    pinfo = page.evaluate(
        """() => ({
      multi: document.querySelectorAll('#cf select[multiple]').length,
      opts: document.querySelector('#cf select[multiple]')?.options?.length || 0
    })"""
    )
    print("pieces", pinfo)
    page.screenshot(path=str(out / "cm8_pieces_sfx.png"), full_page=True)
    b.close()
print("ok", sorted(p.name for p in out.glob("*.png")))
