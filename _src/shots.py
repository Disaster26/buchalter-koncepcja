# -*- coding: utf-8 -*-
"""Zrzuty i testy: python _src/shots.py <runda> [baza]
_src/shots/<runda>/<strona>_<w>x<h>[_full].png, menu mobilne, raport: konsola, przewijanie poziome, h1, linki wewnętrzne, koniec hero."""
import sys, json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
runda = sys.argv[1] if len(sys.argv) > 1 else "r1"
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8811/"
OUT = ROOT / "_src" / "shots" / runda
OUT.mkdir(parents=True, exist_ok=True)
EXE = str(Path.home() / "AppData/Local/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-win64/chrome-headless-shell.exe")
strony = [""] + sorted(p.parent.relative_to(ROOT).as_posix() + "/" for p in ROOT.glob("**/index.html")
                       if "_src" not in p.as_posix() and "wizualizacja" not in p.as_posix() and p.parent != ROOT) + ["404.html"]
VP = [(390, 844), (2000, 950), (1366, 768)]
raport, linki = [], set()
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=EXE)
    for w, h in VP:
        ctx = br.new_context(viewport={"width": w, "height": h}, is_mobile=w < 768, has_touch=w < 768, locale="pl-PL")
        for s in strony:
            pg = ctx.new_page()
            bl = []
            pg.on("console", lambda m: bl.append(m.text) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: bl.append(str(e)))
            pg.on("requestfailed", lambda r: bl.append("FAIL " + r.url))
            pg.goto(BASE + s, wait_until="networkidle")
            pg.wait_for_timeout(250)
            n = (s.strip("/").replace("/", "_") or "home").replace(".html", "")
            pg.screenshot(path=str(OUT / f"{n}_{w}x{h}.png"))
            info = pg.evaluate("""() => {const cw = document.documentElement.clientWidth;
              const hero = document.querySelector('.hero');
              return {sw: document.documentElement.scrollWidth, cw,
                wide: [...document.querySelectorAll('body *')].filter(e => {const r = e.getBoundingClientRect(); return r.right > cw + 1 && r.width > 0 && getComputedStyle(e).position !== 'fixed' && !e.closest('.skip,.pulapka');}).slice(0, 5).map(e => e.tagName + '.' + e.className),
                h1: document.querySelectorAll('h1').length,
                heroBottom: hero ? Math.round(hero.getBoundingClientRect().bottom) : null,
                links: [...document.querySelectorAll('a[href]')].map(a => a.href)}}""")
            for l in info["links"]:
                if l.startswith(BASE):
                    linki.add(l.split("#")[0].split("?")[0])
            if w != 1366:
                pg.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); }")
                pg.add_style_tag(content=".mob{display:none!important}"); pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"{n}_{w}x{h}_full.png"), full_page=True)
            if w == 390 and s == "":
                pg.click("#burger"); pg.wait_for_timeout(350)
                pg.screenshot(path=str(OUT / f"menu_{w}x{h}.png"))
            r = {"strona": s or "/", "vp": f"{w}x{h}", "hero": info["heroBottom"]}
            if info["sw"] > info["cw"] or bl or info["h1"] != 1:
                r.update({"poziomo": info["sw"] - info["cw"], "el": info["wide"], "bledy": bl[:6], "h1": info["h1"]})
                raport.append(r)
            elif s == "":
                raport.append(r)
            pg.close()
        ctx.close()
    # linki wewnętrzne
    ctx = br.new_context()
    zle = []
    for l in sorted(linki):
        resp = ctx.request.get(l)
        if resp.status != 200:
            zle.append([l, resp.status])
    br.close()
raport.append({"linki_sprawdzone": len(linki), "zle": zle})
(OUT / "raport.json").write_text(json.dumps(raport, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(raport, ensure_ascii=False, indent=1)[:5000])
