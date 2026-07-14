"""Build store-ready zips: dist/bonecrush-crazygames.zip + dist/bonecrush-poki.zip.
Injects the platform SDK adapter at the <!-- PLATFORM_SDK --> marker and bundles the
multi-file game (index.html + assets/ + sounds/).

Mirrors D:/Dev/SkullDrift/build.py. SDK snippets follow current docs:
  - CrazyGames HTML5 SDK v3 (crazygames-sdk-v3.js): CrazyGames.SDK.init(),
    game.loadingStop(), game.gameplayStart(), game.gameplayStop(),
    ad.requestAd('midgame', {adStarted, adFinished, adError}).
  - Poki SDK v2 (poki-sdk.js): PokiSDK.init(), gameLoadingFinished(),
    gameplayStart(), gameplayStop(), commercialBreak().
Both PSDK adapters no-op/resolve gracefully if the SDK fails to load outside the portal."""
import os, zipfile

CG = """<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>
<script>
window.PSDK = (function(){
  let sdk = null;
  const ready = (async()=>{ try { await window.CrazyGames.SDK.init(); sdk = window.CrazyGames.SDK; } catch(e){} })();
  return {
    ready,
    loaded(){ try { sdk && sdk.game.loadingStop && sdk.game.loadingStop(); } catch(e){} },
    start(){ try { sdk && sdk.game.gameplayStart(); } catch(e){} },
    stop(){ try { sdk && sdk.game.gameplayStop(); } catch(e){} },
    midgame(){ return new Promise(res => { if (!sdk) return res();
      try { sdk.ad.requestAd('midgame', { adFinished: res, adError: res, adStarted(){ } }); }
      catch(e){ res(); } }); }
  };
})();
</script>"""

POKI = """<script src="https://game-cdn.poki.com/scripts/v2/poki-sdk.js"></script>
<script>
window.PSDK = (function(){
  const ready = (async()=>{ try { await PokiSDK.init(); } catch(e){} })();
  return {
    ready,
    loaded(){ try { PokiSDK.gameLoadingFinished(); } catch(e){} },
    start(){ try { PokiSDK.gameplayStart(); } catch(e){} },
    stop(){ try { PokiSDK.gameplayStop(); } catch(e){} },
    midgame(){ try { return PokiSDK.commercialBreak(()=>{}).catch(()=>{}); } catch(e){ return Promise.resolve(); } }
  };
})();
</script>"""

src = open('index.html', encoding='utf-8').read()
assert '<!-- PLATFORM_SDK -->' in src, 'marker missing'
os.makedirs('dist', exist_ok=True)

def add_dir(z, folder):
    if not os.path.isdir(folder):
        return
    for root, _, files in os.walk(folder):
        for f in files:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, '.').replace('\\', '/'))

for name, snippet in (('crazygames', CG), ('poki', POKI)):
    html = src.replace('<!-- PLATFORM_SDK -->', snippet, 1)
    out = f'dist/bonecrush-{name}.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html', html)
        add_dir(z, 'assets')
        add_dir(z, 'sounds')
    print(out, os.path.getsize(out), 'bytes')
