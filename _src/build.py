# -*- coding: utf-8 -*-
"""Generator wersji testowej strony Biura Rachunkowego Buchalter (Chełmno).
Uruchomienie: python _src/build.py  -> strony w katalogach obok (index.html), sitemap.xml, robots.txt, 404.html.
Dane firmy wyłącznie z obecnej strony buchalter.cloud i umowy (CEIDG). Ceny "od" i teksty wg maila klientki z 10.11.2026."""
import json, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROD = "https://buchalter.cloud/"      # docelowy adres (do potwierdzenia przez klientkę)
KIER = os.environ.get("KIERUNEK", "")   # prototypy kierunkow: a / b / c
TEST = True                            # wersja testowa: noindex + robots Disallow
DZIS = "2026-11-13"
import datetime as _dt
ROK = _dt.date.today().year
BADGE = (Path(__file__).parent / "badge.html").read_text(encoding="utf-8").strip()

TEL = "56 691 20 80"; TEL_H = "+48566912080"
TEL_K = "56 691 20 85"; TEL_K_H = "+48566912085"
MAIL = "recepcja@buchalter.home.pl"; MAIL_K = "kadry@buchalter.home.pl"
FB = "https://www.facebook.com/profile.php?id=100063471177071"
TRASA = "https://www.google.com/maps/dir/?api=1&amp;destination=Rybacka+3%2C+86-200+Che%C5%82mno"
OPINIE = "https://www.google.com/maps/search/?api=1&amp;query=Biuro+Rachunkowe+Buchalter+Rybacka+3+Che%C5%82mno"
MAPA = f'''<div class="mapa" id="mapa" data-gmapa>
      <iframe src="https://maps.google.com/maps?q=Rybacka%203%2C%2086-200%20Che%C5%82mno&amp;z=16&amp;output=embed" title="Mapa Google - ul. Rybacka 3, Chełmno" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      <div class="mapa-zaslona mapa-zast" hidden>
        <svg class="ik" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path d="M16 28s-8.5-8.2-8.5-14.5a8.5 8.5 0 0 1 17 0C24.5 19.8 16 28 16 28z"/><circle cx="16" cy="13.5" r="3"/></svg>
        <p><b>ul. Rybacka 3, 86-200 Chełmno</b>Mapa Google jest wyłączona w&nbsp;ustawieniach cookies.</p>
        <div class="mapa-akcje"><a class="btn-out" href="{TRASA}" target="_blank" rel="noopener">Wyznacz trasę</a><button class="link-strz st-ck" type="button" data-ck-otworz>Ustawienia cookies</button></div>
      </div>
    </div>'''

IKONA_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'

OFERTA = [
    ("oferta/ksiegowosc/", "Księgowość"),
    ("oferta/kadry-i-place/", "Kadry i płace"),
    ("oferta/podatki/", "Rozliczenia podatkowe"),
    ("oferta/zakladanie-dzialalnosci/", "Zakładanie działalności"),
]

ORG = {
    "@context": "https://schema.org",
    "@type": "AccountingService",
    "@id": PROD + "#biuro",
    "name": "Biuro Rachunkowe Buchalter Wioletta Prełowska",
    "legalName": "BIURO RACHUNKOWE \"BUCHALTER\" PREŁOWSKA WIOLETTA",
    "alternateName": "Buchalter",
    "url": PROD,
    "logo": PROD + "assets/img/logo.png",
    "image": PROD + "assets/img/og-buchalter.jpg",
    "telephone": "+48 56 691 20 80",
    "email": MAIL,
    "taxID": "8751098647",
    "identifier": [{"@type": "PropertyValue", "propertyID": "REGON", "value": "871183546"}],
    "foundingDate": "1999",
    "founder": {"@type": "Person", "name": "Wioletta Prełowska"},
    "address": {"@type": "PostalAddress", "streetAddress": "ul. Rybacka 3 lok. 1", "postalCode": "86-200",
                "addressLocality": "Chełmno", "addressRegion": "kujawsko-pomorskie", "addressCountry": "PL"},
    "areaServed": [{"@type": "City", "name": "Chełmno"}, {"@type": "AdministrativeArea", "name": "powiat chełmiński"}],
    "contactPoint": [
        {"@type": "ContactPoint", "contactType": "customer service", "name": "Recepcja", "telephone": "+48 56 691 20 80", "email": MAIL, "availableLanguage": "pl"},
        {"@type": "ContactPoint", "contactType": "kadry i płace", "telephone": "+48 56 691 20 85", "email": MAIL_K, "availableLanguage": "pl"},
    ],
    "knowsAbout": ["KSeF", "ewidencja VAT", "JPK_VAT", "księgowość", "księga przychodów i rozchodów", "ryczałt ewidencjonowany", "pełna księgowość", "kadry i płace", "rozliczenia podatkowe", "zakładanie działalności gospodarczej"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "16:00"}],
    "sameAs": [FB],
}


def R(depth):
    return "./" if depth == 0 else "../" * depth


def menu(akt):
    def a(href, txt):
        cur = ' aria-current="page"' if href == akt else ""
        return f'<a href="{{R}}{href}"{cur}>{txt}</a>'
    pod = "".join(a(h, t) for h, t in OFERTA)
    return (f'<nav class="menu" id="menu" aria-label="Menu główne">'
            f'<div class="menu-grupa">{a("oferta/", "Oferta")}<div class="podmenu">{pod}</div></div>'
            f'{a("jak-pracujemy/", "Jak pracujemy")}{a("o-biurze/", "O biurze")}{a("cennik/", "Cennik")}{a("kontakt/", "Kontakt")}<a class="menu-wycena" href="{{R}}kontakt/#formularz">Bezpłatna wycena</a></nav>')


def stopka():
    of = "".join(f'<li><a href="{{R}}{h}">{t}</a></li>' for h, t in OFERTA)
    return f'''<footer class="stopka">
  <div class="wrap stopka-in">
    <div>
      <b class="firma">Buchalter</b>
      <p>Biuro Rachunkowe Wioletta Prełowska<br>ul. Rybacka 3, 86-200 Chełmno<br>pon.-pt. 9:00-16:00</p>
      <p><a href="tel:{TEL_H}">tel. {TEL}</a> (recepcja)<br><a href="tel:{TEL_K_H}">tel. {TEL_K}</a> (kadry)<br><a href="mailto:{MAIL}">{MAIL}</a></p>
      <p>NIP 875-109-86-47, REGON 871183546</p>
    </div>
    <div>
      <h2>Oferta</h2>
      <ul>{of}<li><a href="{{R}}cennik/">Cennik</a></li></ul>
    </div>
    <div>
      <h2>Biuro</h2>
      <ul><li><a href="{{R}}jak-pracujemy/">Jak pracujemy</a></li><li><a href="{{R}}o-biurze/">O biurze</a></li><li><a href="{{R}}kontakt/">Kontakt i dojazd</a></li><li><a href="{FB}" rel="noopener" target="_blank">Facebook</a></li><li><a href="{{R}}polityka-prywatnosci/">Polityka prywatności</a></li><li><button type="button" class="st-ck" data-ck-otworz>Ustawienia cookies</button></li></ul>
    </div>
  </div>
  <div class="wrap stopka-dol">
    <span>&copy; {ROK} Biuro Rachunkowe Buchalter. Wersja testowa nowej strony. Zdjęcia poglądowe: Vitaly Gariev, <a href="https://unsplash.com/photos/M5k978V3qBc" rel="noopener" target="_blank">Unsplash</a> (licencja Unsplash).</span>
    {BADGE}
  </div>
</footer>'''


def strona(path, title, desc, body, akt="", okruszki=None, schema_extra=None, home=False, og_typ="website"):
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    url = PROD + (path if path != "404.html" else "")
    ld = []
    if home or path == "kontakt/":
        ld.append(ORG)
    if okruszki:
        items = [{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": PROD}]
        for i, (n, h) in enumerate(okruszki, 2):
            items.append({"@type": "ListItem", "position": i, "name": n, "item": PROD + h})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if schema_extra:
        ld.append(schema_extra)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>\n' for x in ld)
    robots = '<meta name="robots" content="noindex, nofollow">\n' if TEST or path == "404.html" else ""
    canon = f'<link rel="canonical" href="{url}">\n' if path != "404.html" else ""
    preload = ('<link rel="preload" as="image" href="{R}assets/img/hero-tel-900.webp" media="(max-width: 760px)">\n'
               '<link rel="preload" as="image" imagesrcset="{R}assets/img/hero-1200.webp 1200w, {R}assets/img/hero-1800.webp 1800w, {R}assets/img/hero-2400.webp 2400w" imagesizes="100vw" media="(min-width: 761px)">\n') if home else ""
    kier_css = f'<link rel="stylesheet" href="{{R}}_src/kierunki/{KIER}.css">\n' if KIER and home else ""
    html = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{robots}<title>{title}</title>
<meta name="description" content="{desc}">
{canon}<meta name="theme-color" content="#022f5e">
<meta property="og:type" content="{og_typ}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="Biuro Rachunkowe Buchalter">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{PROD}assets/img/og-buchalter.jpg">
<meta name="geo.region" content="PL-KP">
<meta name="geo.placename" content="Chełmno">
<link rel="icon" href="{{R}}assets/img/favicon.png">
<link rel="preload" as="font" type="font/woff2" href="{{R}}assets/fonts/newsreader-n-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{{R}}assets/fonts/instrumentsans-latin.woff2" crossorigin>
{preload}<link rel="stylesheet" href="{{R}}assets/css/style.css?v=4">
{kier_css}
{ld_html}</head>
<body class="{'dom' if home else 'pod'}{(' k-' + KIER) if KIER and home else ''}">
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="top">
  <div class="wrap top-in">
    <a class="marka" href="{{R}}" aria-label="Buchalter - strona główna">
      <img src="{{R}}assets/img/logo.png" alt="" width="40" height="40">
      <span><b>Buchalter</b><small>Biuro Rachunkowe Wioletta Prełowska</small></span>
    </a>
    {menu(akt)}
    <a class="tel-top" href="tel:{TEL_H}" aria-label="Zadzwoń do biura: {TEL}">{IKONA_TEL}<span>{TEL}</span></a>
    <button class="burger" id="burger" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="tresc">
{body}
</main>
{stopka()}
<div class="mob" id="mob" aria-hidden="true">
  <a class="mob-tel" href="tel:{TEL_H}" tabindex="-1">Zadzwoń</a>
  <a class="mob-cta" href="{{R}}kontakt/#formularz" tabindex="-1">Bezpłatna wycena</a>
</div>
<div class="ck" id="ck" hidden role="dialog" aria-label="Ustawienia plików cookies">
  <p class="ck-t">Strona używa plików cookies niezbędnych do działania i&nbsp;zapamiętania Twojego wyboru. Osadzona mapa Google może zapisywać własne pliki cookies. <a href="{{R}}polityka-prywatnosci/#cookies">Polityka prywatności</a></p>
  <div class="ck-ust" hidden>
    <label><input type="checkbox" checked disabled> <span><b>Niezbędne</b> - zapamiętanie wyboru, zawsze włączone</span></label>
    <label><input type="checkbox" data-ck-kat="mapy" checked> <span><b>Mapy Google</b> - mapa dojazdu do biura</span></label>
  </div>
  <div class="ck-btn"><button type="button" class="ck-b ck-ustaw" data-ck="ustawienia">Ustawienia</button><button type="button" class="ck-b" data-ck="niezbedne">Tylko niezbędne</button><button type="button" class="ck-b ck-ok" data-ck="wszystkie">Akceptuję wszystkie</button></div>
</div>
<script src="{{R}}assets/js/site.js?v=5" defer></script>
<script src="{{R}}assets/js/ck.js?v=5" defer></script>
</body>
</html>
'''
    html = html.replace("{R}", R(depth))
    # sierotki: pojedyncze litery (w, i, z, o, a, u) sklejone z następnym słowem - tylko w treści body
    gb = html.index("<body")
    html = html[:gb] + re.sub(r">([^<]+)<", lambda m: ">" + re.sub(r"(?<![\w&;])([aiouwzAIOUWZ]) (?=\S)", lambda z: z.group(1) + "&nbsp;", m.group(1)) + "<", html[gb:])
    assert "—" not in html and "–" not in html, path
    out = ROOT / ("404.html" if path == "404.html" else path + "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return path


GLOWA_FOTO = {"oferta/": "narada", "oferta/ksiegowosc/": "spotkanie", "oferta/kadry-i-place/": "zespol", "oferta/podatki/": "rozmowa",
              "oferta/zakladanie-dzialalnosci/": "narada", "jak-pracujemy/": "zespol", "o-biurze/": "zespol", "cennik/": "spotkanie", "kontakt/": "rozmowa"}


def glowa(h1, lead, okruszki):
    li = '<li><a href="{R}">Strona główna</a></li>'
    for i, (n, h) in enumerate(okruszki):
        cur = ' aria-current="page"' if i == len(okruszki) - 1 else ""
        li += f'<li><a href="{{R}}{h}"{cur}>{n}</a></li>'
    f = GLOWA_FOTO.get(okruszki[-1][1])
    fig = (f'<figure class="glowa-foto"><img src="{{R}}assets/img/{f}-1400.webp" srcset="{{R}}assets/img/{f}-800.webp 800w, {{R}}assets/img/{f}-1400.webp 1400w" sizes="50vw" alt="" width="1400" height="788" fetchpriority="high"></figure>') if f else ""
    return f'''<section class="glowa-strony{' z-foto' if f else ''}">
  {fig}
  <div class="wrap">
    <nav class="okruszki" aria-label="Jesteś tutaj"><ol>{li}</ol></nav>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>'''


def boczna(temat, dopisek=""):
    return f'''<aside class="boczna" aria-label="Kontakt z biurem">
  <h2>Zapytaj o wycenę</h2>
  <p>Wycena jest bezpłatna. Zadzwoń do recepcji albo opisz krótko swoją firmę w formularzu.</p>
  <a class="tel-duzy" href="tel:{TEL_H}">{TEL}</a>
  <small>recepcja biura</small>
  {dopisek}
  <a class="btn" href="{{R}}kontakt/?temat={temat}#formularz">Napisz do biura</a>
</aside>'''


def inne(akt):
    li = "".join(f'<li><a href="{{R}}{h}">{t}</a></li>' for h, t in OFERTA if h != akt)
    li += '<li><a href="{R}cennik/">Cennik pakietów</a></li>'
    return f'''<section class="inne">
  <div class="wrap">
    <h2>Pozostałe usługi biura</h2>
    <ul>{li}</ul>
  </div>
</section>'''


def usluga(path, nazwa, title, desc, h1, lead, tresc, temat, dopisek=""):
    ok = [("Oferta", "oferta/"), (nazwa, path)]
    sch = {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": nazwa,
           "provider": {"@id": PROD + "#biuro"}, "areaServed": {"@type": "City", "name": "Chełmno"}, "url": PROD + path}
    body = glowa(h1, lead, ok) + f'''
<section>
  <div class="wrap uklad">
    <div class="tresc">
{tresc}
    </div>
    {boczna(temat, dopisek)}
  </div>
</section>
''' + inne(path)
    return strona(path, title, desc, body, akt=path, okruszki=ok, schema_extra=sch)


strony = []
FAQ_LD = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Ile kosztuje prowadzenie księgowości?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Ceny zaczynają się od: księga przychodów i rozchodów 200 zł netto, ryczałt 180 zł netto, księgi handlowe 800 zł netto, kadry i płace 60 zł netto. Dokładna kwota zależy od formy działalności i opodatkowania, liczby dokumentów w miesiącu i liczby pracowników. Wycena jest bezpłatna - wystarczy telefon do recepcji albo wiadomość przez formularz.'}}, {'@type': 'Question', 'name': 'Czy muszę przychodzić do biura z dokumentami?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Nie. Zdecydowana większość faktur trafia do nas z KSeF. Pozostałe dokumenty, np. faktury zagraniczne, możesz przesyłać elektronicznie albo zostawić w recepcji przy ul. Rybackiej 3.'}}, {'@type': 'Question', 'name': 'Czy przypomnicie mi o podatku i ZUS?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Co miesiąc dostajesz informację o wysokości i terminie zapłaty podatków oraz składek ZUS.'}}, {'@type': 'Question', 'name': 'Czy mogę wglądać w swoje dokumenty?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Faktury z KSeF masz zawsze w KSeF. Dokumenty papierowe archiwizujemy po zakończeniu roku i sporządzeniu zeznania rocznego, a ewidencje podatkowe przekazujemy Ci elektronicznie.'}}, {'@type': 'Question', 'name': 'Czy prowadzicie kadry i płace?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak, mamy osobny dział kadr: tel. 56 691 20 85, kadry@buchalter.home.pl. Przygotowujemy umowy, listy płac, rozliczenia ZUS i deklaracje PIT-11.'}}, {'@type': 'Question', 'name': 'Czy pomagacie osobom, które nie prowadzą firmy?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Rozliczamy podatki osób nieprowadzących działalności gospodarczej i prowadzimy ewidencje podatkowe osób prywatnych i rolników, np. najem prywatny i rozliczanie VAT dla rolników.'}}, {'@type': 'Question', 'name': 'Czy pomożecie założyć firmę albo spółkę?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Pomagamy wybrać formę działalności i załatwiamy formalności, także rejestrację spółki w KRS. Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową (radcy prawni, doradcy podatkowi).'}}]}

# ---------------------------------------------------------------- STRONA GLOWNA
def ik(nazwa):
    return f'<svg class="ik" viewBox="0 0 32 32" aria-hidden="true" focusable="false">{IKONY[nazwa]}</svg>'


IKONY = {
    "ksiega": '<path d="M7 5.5h15a3 3 0 0 1 3 3V27H10a3 3 0 0 1-3-3z"/><path d="M7 24a3 3 0 0 1 3-3h15"/><path d="M12 10.5h8M12 14.5h6"/>',
    "pelna": '<rect x="5" y="6" width="22" height="20" rx="1.5"/><path d="M5 12h22M12 12v14M5 19h22"/>',
    "kadry": '<circle cx="12" cy="11" r="4"/><path d="M4.5 25.5c.8-4.2 3.8-6.5 7.5-6.5s6.7 2.3 7.5 6.5"/><circle cx="22.5" cy="12.5" r="3"/><path d="M21 19.2c3.3-.3 5.8 1.6 6.5 5.3"/>',
    "podatki": '<path d="M8 4.5h12l5 5V27.5H8z"/><path d="M20 4.5v5h5"/><path d="M12.5 21.5l7-7"/><circle cx="13" cy="15" r="1.3"/><circle cx="19" cy="21" r="1.3"/>',
    "start": '<path d="M5 26.5h22"/><path d="M8 26.5V13l8-6 8 6v13.5"/><path d="M13.5 26.5v-7h5v7"/>',
    "prywatni": '<path d="M3.5 26h25"/><path d="M4.5 26V15.5L11 10l6.5 5.5V26"/><path d="M9.5 26v-5h3v5"/><path d="M23.5 26V14"/><path d="M23.5 19.5c-3.6 0-5.5-2.2-5.5-5.5 3.6 0 5.5 2.2 5.5 5.5z"/><path d="M23.5 16.5c0-3.6 2-6 5.5-6 0 3.5-2 6-5.5 6z"/>',
    "wsparcie": '<path d="M16 4.5l9.5 3.8v7.2c0 5.8-4 10-9.5 12-5.5-2-9.5-6.2-9.5-12V8.3z"/><path d="M11.5 16l3.2 3.2 6-6.4"/>',
}

home = f'''<section class="hero">
  <figure class="hero-foto">
    <picture>
      <source media="(max-width: 760px)" srcset="{{R}}assets/img/hero-tel-900.webp">
      <img src="{{R}}assets/img/hero-1800.webp" srcset="{{R}}assets/img/hero-1200.webp 1200w, {{R}}assets/img/hero-1800.webp 1800w, {{R}}assets/img/hero-2400.webp 2400w" sizes="100vw" alt="Księgowa omawia z klientem dokumenty firmy przy stole w jasnym biurze" width="1800" height="1012" fetchpriority="high">
    </picture>
  </figure>
  <div class="hero-in">
    <div class="wrap">
      <div class="hero-tekst">
        <p class="hero-adres">Buchalter, ul. Rybacka 3, Chełmno</p>
        <h1>Biuro Rachunkowe w&nbsp;Chełmnie</h1>
        <p class="lead">Od 1999 roku prowadzimy księgowość oraz obsługujemy kadry i&nbsp;płace jednoosobowych działalności, spółek, fundacji i&nbsp;stowarzyszeń. W&nbsp;Buchalterze pracują wyspecjalizowane zespoły zajmujące się księgami rachunkowymi, uproszczoną księgowością oraz kadrami i&nbsp;płacami. Pomagamy też wdrożyć KSeF, usprawnić elektroniczny obieg dokumentów i&nbsp;korzystać z&nbsp;e-Urzędu Skarbowego. Dokumenty możesz przesyłać online lub zostawić w&nbsp;recepcji przy ul.&nbsp;Rybackiej&nbsp;3.</p>
        <div class="hero-cta" id="heroCta">
          <a class="btn btn-hero" href="{{R}}kontakt/#formularz">Umów bezpłatną wycenę</a>
          <a class="hero-tel" href="tel:{TEL_H}">{IKONA_TEL}<span>lub zadzwoń <b>{TEL}</b></span></a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sek uslugi-sek" id="oferta">
  <div class="wrap">
    <div class="sek-glowa">
      <h2>Zakres usług</h2>
      <p>Obsługujemy jednoosobowe działalności, spółki, fundacje i&nbsp;stowarzyszenia oraz osoby prywatne.</p>
    </div>
    <div class="uslugi">
      <a class="usluga" href="{{R}}oferta/ksiegowosc/">{ik("ksiega")}<h3>Księga przychodów i&nbsp;ryczałt</h3><p>KPiR albo ewidencja przychodów, środki trwałe. Co miesiąc wiesz, ile i&nbsp;do kiedy zapłacić podatku i&nbsp;ZUS.</p><span class="wiecej">Księgowość dla firm</span></a>
      <a class="usluga" href="{{R}}oferta/ksiegowosc/#pelna-ksiegowosc">{ik("pelna")}<h3>Pełna księgowość</h3><p>Księgi rachunkowe spółek, fundacji i&nbsp;stowarzyszeń, polityka rachunkowości, sprawozdania finansowe.</p><span class="wiecej">Księgi rachunkowe</span></a>
      <a class="usluga" href="{{R}}oferta/kadry-i-place/">{ik("kadry")}<h3>Kadry i&nbsp;płace</h3><p>Umowy, akta osobowe, terminy badań i&nbsp;BHP, listy płac, ZUS i&nbsp;PIT-11. Osobny dział kadr.</p><span class="wiecej">Obsługa kadrowo-płacowa</span></a>
      <a class="usluga" href="{{R}}oferta/podatki/">{ik("podatki")}<h3>Rozliczenia podatkowe</h3><p>Rozliczenia firm i&nbsp;osób prywatnych. Reprezentujemy podatników przed organami kontroli.</p><span class="wiecej">Podatki i&nbsp;kontrole</span></a>
      <a class="usluga" href="{{R}}oferta/podatki/#osoby-prywatne-i-rolnicy">{ik("prywatni")}<h3>Osoby prywatne i&nbsp;rolnicy</h3><p>Prowadzimy ewidencje podatkowe osób prywatnych i&nbsp;rolników: najem prywatny, rozliczanie VAT dla rolników.</p><span class="wiecej">Ewidencje podatkowe</span></a>
      <a class="usluga" href="{{R}}oferta/zakladanie-dzialalnosci/">{ik("start")}<h3>Zakładanie działalności</h3><p>Wybór formy działalności, formalności, rejestracja spółki w&nbsp;KRS. Przy wyborze formy opodatkowania współpracujemy z&nbsp;kancelarią prawno-podatkową.</p><span class="wiecej">Start firmy</span></a>
      <a class="usluga usluga-szeroka" href="{{R}}oferta/#wsparcie">{ik("wsparcie")}<h3>Bieżące wsparcie i&nbsp;KSeF</h3><p>Pomagamy we wszystkich formalnościach związanych z&nbsp;KSeF: przy zakładaniu profilu zaufanego, nadawaniu uprawnień i&nbsp;zarządzaniu nimi, wystawianiu i&nbsp;wysyłce faktur sprzedaży. Faktury możemy odbierać bezpośrednio z&nbsp;KSeF albo udostępnić Ci aplikację połączoną z&nbsp;KSeF i&nbsp;naszym systemem księgowym. Śledzimy też zmiany w&nbsp;przepisach i&nbsp;mówimy, co z&nbsp;nich wynika dla Twojej firmy.</p><span class="wiecej">Cała oferta</span></a>
    </div>
  </div>
</section>

<section class="sek szare dlaczego">
  <div class="wrap dlaczego-in">
    <figure class="dlaczego-foto"><img src="{{R}}assets/img/rozmowa-1400.webp" srcset="{{R}}assets/img/rozmowa-800.webp 800w, {{R}}assets/img/rozmowa-1400.webp 1400w" sizes="(max-width: 960px) 100vw, 50vw" alt="Spotkanie z klientami przy kawie w biurze" width="1400" height="788" loading="lazy"></figure>
    <div class="dlaczego-tekst">
      <h2>Rzetelna księgowość bez kosztu własnego działu</h2>
      <dl class="atuty">
        <div><dt>Zdalnie albo na miejscu</dt><dd>Dokumenty przesyłasz elektronicznie albo zostawiasz w&nbsp;recepcji przy Rybackiej. Urlop jednej osoby nie zatrzymuje pracy nad Twoimi sprawami.</dd></div>
        <div><dt>Księgowi z&nbsp;kierunkowym wykształceniem</dt><dd>Stale się szkolą i&nbsp;na co dzień prowadzą złożone sprawy księgowe i&nbsp;kadrowe.</dd></div>
        <div><dt>Działy według rodzaju klientów</dt><dd>Twoją firmę prowadzi dział, który rozlicza firmy o&nbsp;tej samej formie prawnej i&nbsp;sposobie rozliczeń.</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="sek wspolpraca">
  <div class="wrap">
    <div class="sek-glowa">
      <h2>Jak zaczynamy współpracę</h2>
      <p>Najprościej zacząć od telefonu do recepcji albo krótkiej wiadomości przez formularz.</p>
    </div>
    <ol class="kroki">
      <li><h3>Rozmowa i&nbsp;wycena</h3><p>Pytamy o&nbsp;formę działalności, opodatkowanie, liczbę dokumentów i&nbsp;pracowników. Wycena jest bezpłatna.</p></li>
      <li><h3>Umowa</h3><p>Ustalamy, od którego miesiąca przejmujemy księgowość i&nbsp;jak będziesz przekazywać dokumenty.</p></li>
      <li><h3>Faktury z&nbsp;KSeF i&nbsp;dokumenty</h3><p>Ustalamy, jak będą do nas trafiać faktury z&nbsp;KSeF: przez udostępnianą przez nas aplikację (Betterfly od Comarch, prosta, również mobilna) albo pobieramy je sami. Pomagamy nadać uprawnienia w&nbsp;KSeF i&nbsp;podpowiadamy, co jeszcze przygotować.</p></li>
      <li><h3>Stała obsługa</h3><p>Co miesiąc dostajesz kwoty i&nbsp;terminy podatków oraz ZUS. Na pytania odpowiadamy niezwłocznie.</p></li>
    </ol>
    <a class="link-strz" href="{{R}}jak-pracujemy/">Więcej o&nbsp;współpracy</a>
  </div>
</section>

<section class="sek granat wlascicielka">
  <div class="wrap wl-in">
    <div class="wl-glowa">
      <h2>Wioletta Prełowska</h2>
      <p class="wl-rola">Właścicielka biura od 1999 roku</p>
      <p>W&nbsp;rachunkowości pracuje od ponad 30 lat. Ma świadectwo kwalifikacyjne do usługowego prowadzenia ksiąg rachunkowych i&nbsp;jest sygnatariuszką Kodeksu Etyki Zawodowej w&nbsp;Rachunkowości Stowarzyszenia Księgowych w&nbsp;Polsce.</p>
      <a class="link-strz jasny" href="{{R}}o-biurze/">Więcej o&nbsp;biurze</a>
    </div>
    <ul class="sciezka">
      <li><span>1999</span><p>Świadectwo kwalifikacyjne uprawniające do usługowego prowadzenia ksiąg rachunkowych.</p></li>
      <li><span>2001-2002</span><p>Wszystkie stopnie kursów Stowarzyszenia Księgowych w&nbsp;Polsce.</p></li>
      <li><span>2018</span><p>Wpis na listę sygnatariuszy Kodeksu Etyki Zawodowej w&nbsp;Rachunkowości SKwP.</p></li>
      <li><span>Dziś</span><p>Zespół podzielony na działy, z&nbsp;których każdy obsługuje klientów określonego typu.</p></li>
    </ul>
  </div>
</section>

<section class="sek szare cennik-sek">
  <div class="wrap cen-in">
    <div>
      <h2>Cennik pakietów</h2>
      <p class="lead2">Ceny netto. Dokładną kwotę ustalamy indywidualnie, bo zależy od formy działalności, liczby dokumentów w&nbsp;miesiącu i&nbsp;liczby pracowników.</p>
      <table class="rachunek">
        <caption class="sr">Pakiety usług księgowych</caption>
        <tbody>
          <tr><th scope="row">Księgi podatkowe (KPiR)</th><td>od 200 zł netto</td></tr>
          <tr><th scope="row">Ryczałt</th><td>od 180 zł netto</td></tr>
          <tr><th scope="row">Księgi handlowe</th><td>od 800 zł netto</td></tr>
          <tr><th scope="row">Kadry i&nbsp;płace</th><td>od 60 zł netto</td></tr>
        </tbody>
      </table>
      <a class="link-strz" href="{{R}}cennik/">Co obejmują pakiety</a>
    </div>
    <aside class="ocena" aria-label="Ocena w Google">
      <p class="ocena-gw"><span class="gwiazdki" aria-hidden="true"><i style="--p:84%"></i></span><b>4,2</b> na 5</p>
      <p>Średnia ocen biura w&nbsp;Mapach Google, 24 opinie klientów.</p>
      <a class="link-strz" href="{OPINIE}" target="_blank" rel="noopener">Opinie w&nbsp;Google</a>
    </aside>
  </div>
</section>

<section class="sek kontakt-sek">
  <div class="wrap kontakt-pas-in">
    <div>
      <h2>Biuro przy ul. Rybackiej 3</h2>
      <p class="lead2">Zadzwoń, napisz albo przyjdź do recepcji. Powiedz, jaką masz firmę, a&nbsp;przygotujemy bezpłatną wycenę.</p>
      <dl class="telefony">
        <div><dt>Recepcja</dt><dd><a class="nr" href="tel:{TEL_H}">{TEL}</a><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
        <div><dt>Kadry i&nbsp;płace</dt><dd><a class="nr" href="tel:{TEL_K_H}">{TEL_K}</a><a href="mailto:{MAIL_K}">{MAIL_K}</a></dd></div>
        <div><dt>Adres i&nbsp;godziny</dt><dd>ul. Rybacka 3 lok. 1, 86-200 Chełmno<br>poniedziałek - piątek, 9:00-16:00</dd></div>
      </dl>
      <a class="btn" href="{{R}}kontakt/#formularz">Napisz do biura</a>
    </div>
    {MAPA}
  </div>
</section>'''

strony.append(strona("", "Biuro Rachunkowe Chełmno - Buchalter, Wioletta Prełowska",
                     "Biuro Rachunkowe Buchalter w Chełmnie, ul. Rybacka 3. Księgowość, kadry i płace, VAT i JPK, KSeF, ewidencje dla osób prywatnych i rolników. Tel. 56 691 20 80.",
                     home, home=True))

# ---------------------------------------------------------------- OFERTA
of_body = glowa("Oferta biura rachunkowego w Chełmnie",
                "Księgowość, kadry i płace, rozliczenia podatkowe i pomoc przy zakładaniu firmy. Zakres dobieramy do formy działalności i potrzeb klienta.",
                [("Oferta", "oferta/")]) + f'''
<section>
  <div class="wrap">
    <div class="uslugi uslugi-pod">
      <article class="usluga">
        <h2><a href="{{R}}oferta/ksiegowosc/">Księgowość</a></h2>
        <p>Podatkowa księga przychodów i rozchodów, ewidencja przychodów (ryczałt) i pełne księgi rachunkowe. Do tego ewidencja środków trwałych, sprawozdania finansowe i statystyczne dla GUS.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}oferta/kadry-i-place/">Kadry i płace</a></h2>
        <p>Umowy, akta osobowe, terminy badań i szkoleń BHP, listy płac, rozliczenia ZUS i deklaracje PIT-11. Przejmujemy obowiązki kadrowo-płacowe pracodawcy.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}oferta/podatki/">Rozliczenia podatkowe</a></h2>
        <p>Ewidencja i rozliczenia podatkowe firm, mikrofirm i osób prywatnych, także ewidencje najmu prywatnego i rozliczanie VAT dla rolników. Reprezentacja przed organami kontroli podatkowej.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}oferta/zakladanie-dzialalnosci/">Zakładanie działalności</a></h2>
        <p>Wybór formy działalności, formalności rejestracyjne, rejestracja spółki w KRS. Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}cennik/">Cennik pakietów</a></h2>
        <p>Księga przychodów i rozchodów od 200 zł netto, ryczałt od 180 zł netto, księgi handlowe od 800 zł netto, kadry i płace od 60 zł netto.</p>
        <span class="link-strz" aria-hidden="true">Zobacz cennik</span>
      </article>
      <article class="usluga" id="wsparcie">
        <h2>Bieżące wsparcie i KSeF</h2>
        <p>Pomagamy we wszystkich formalnościach związanych z obowiązkami przedsiębiorcy przy obsłudze KSeF: pomagamy założyć profil zaufany, jeśli jest taka potrzeba, nadawać uprawnienia i nimi zarządzać, wystawiać i wysyłać faktury sprzedaży do KSeF. Możemy odbierać bezpośrednio z KSeF wszystkie Twoje faktury albo udostępnić Ci aplikację współpracującą z naszym systemem księgowym i połączoną z KSeF. W aplikacji samodzielnie wystawisz faktury sprzedaży, zaimportujesz z KSeF faktury zakupu i przed przesłaniem faktur dodasz notatki dla biura.</p>
        <p>Monitorujemy też zmiany w przepisach podatkowych i innych przepisach dotyczących prowadzenia działalności i informujemy klientów o tych, które ich dotyczą.</p>
      </article>
    </div>
  </div>
</section>

<section class="szare">
  <div class="wrap">
    <div class="sek-glowa">
      <h2>Dla kogo pracujemy</h2>
      <p>Każdy dział biura zajmuje się klientami o podobnej formie prawnej i sposobie rozliczeń. Tak wygląda to w praktyce:</p>
    </div>
    <ul class="dla-kogo">
      <li><h3>Jednoosobowa działalność</h3><p>Księga przychodów i rozchodów albo ryczałt, środki trwałe, miesięczna informacja o podatku i składkach ZUS. Jeśli zatrudniasz - także kadry i płace.</p></li>
      <li><h3>Spółki</h3><p>Pełne księgi rachunkowe, polityka rachunkowości, plan kont, sprawozdania finansowe i ich publikacja. Obsługujemy również spółki-córki większych firm.</p></li>
      <li><h3>Fundacje i stowarzyszenia</h3><p>Księgi rachunkowe organizacji, instrukcje obiegu dokumentów i sprawozdania finansowe.</p></li>
      <li><h3>Osoby prywatne</h3><p>Rozliczenia podatkowe osób, które nie prowadzą działalności gospodarczej, i ewidencje podatkowe najmu prywatnego.</p></li>
      <li><h3>Rolnicy</h3><p>Rozliczanie VAT dla rolników, także sama obsługa VAT dla rolników rozliczających VAT na zasadach ogólnych.</p></li>
      <li><h3>Nowe firmy</h3><p>Pomoc w wyborze formy działalności i formalności przy rejestracji. Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową.</p></li>
    </ul>
  </div>
</section>'''
strony.append(strona("oferta/", "Oferta - biuro rachunkowe Chełmno | Buchalter",
                     "Usługi Biura Rachunkowego Buchalter w Chełmnie: księga przychodów i rozchodów, ryczałt, VAT i JPK, KSeF, pełna księgowość, kadry i płace, rozliczenia podatkowe, zakładanie działalności.",
                     of_body, akt="oferta/", okruszki=[("Oferta", "oferta/")]))

# ---------------------------------------------------------------- KSIEGOWOSC
strony.append(usluga("oferta/ksiegowosc/", "Księgowość",
    "Księgowość Chełmno - KPiR, ryczałt, VAT, pełna księgowość | Buchalter",
    "Prowadzenie księgowości w Chełmnie: podatkowa księga przychodów i rozchodów, ryczałt ewidencjonowany, ewidencja VAT i JPK_VAT, pełne księgi rachunkowe spółek i fundacji.",
    "Księgowość dla firm i organizacji",
    "Prowadzimy podatkową księgę przychodów i rozchodów, ewidencję przychodów dla ryczałtowców, ewidencję i rozliczenia VAT oraz pełne księgi rachunkowe spółek, fundacji i stowarzyszeń.",
    f'''<h2>Księga przychodów i rozchodów</h2>
<p>Prowadzimy podatkową księgę przychodów i rozchodów zgodnie z obowiązującymi przepisami. W ramach obsługi:</p>
<ul>
  <li>ewidencjonujemy dokumenty księgowe,</li>
  <li>co miesiąc informujemy o wysokości i terminie zapłaty podatku oraz składek ZUS,</li>
  <li>konsultujemy bieżącą sytuację firmy, gdy masz pytania albo planujesz zmiany.</li>
</ul>
<h2>Ryczałt ewidencjonowany</h2>
<p>Dla firm rozliczających się ryczałtem prowadzimy ewidencję przychodów. Tak samo jak przy księdze przychodów dostajesz informację o kwocie i terminie podatku oraz składek ZUS, a w razie wątpliwości - konsultację.</p>
<h2 id="vat">Ewidencja i rozliczenia VAT</h2>
<p>Prowadzimy ewidencję sprzedaży i zakupów VAT oraz przygotowujemy i wysyłamy pliki JPK_VAT. Rozliczenia VAT możemy połączyć z prowadzeniem KPiR, ewidencji przychodów na ryczałcie lub ksiąg rachunkowych. Oferujemy też samą obsługę VAT, m.in. dla rolników rozliczających VAT na zasadach ogólnych.</p>
<h2 id="pelna-ksiegowosc">Pełna księgowość</h2>
<p>Prowadzimy księgi rachunkowe (księgi handlowe) spółek, fundacji i stowarzyszeń. Oprócz samego księgowania przygotowujemy dokumenty, których wymaga ustawa o rachunkowości:</p>
<ul>
  <li>zakładowy plan kont i politykę rachunkowości,</li>
  <li>instrukcje obiegu dokumentów, kasową i inwentaryzacyjną,</li>
  <li>regulaminy pracy i wynagradzania,</li>
  <li>sprawozdania finansowe - i pomagamy w ich publikacji.</li>
</ul>
<h2>Ewidencje i sprawozdania</h2>
<p>Prowadzimy ewidencję środków trwałych, sporządzamy sprawozdania statystyczne dla GUS oraz ewidencje i rejestry według potrzeb klienta.</p>
<h2>Faktury z KSeF i dokumenty papierowe</h2>
<p>Zdecydowana większość faktur trafia do nas z KSeF. Dokumenty spoza KSeF, np. faktury zagraniczne, możesz przesyłać elektronicznie albo zostawić w biurze przy ul. Rybackiej 3. Faktur z KSeF nie drukujemy. Po zakończeniu roku i sporządzeniu zeznania rocznego archiwizujemy dokumenty papierowe, a ewidencje podatkowe przekazujemy Ci elektronicznie.</p>''',
    "Księgowość"))

# ---------------------------------------------------------------- KADRY
strony.append(usluga("oferta/kadry-i-place/", "Kadry i płace",
    "Kadry i płace Chełmno - obsługa kadrowo-płacowa | Buchalter",
    "Obsługa kadrowo-płacowa w Chełmnie: umowy o pracę i zlecenia, akta osobowe, badania i szkolenia BHP, listy płac, ZUS, PIT-11. Dział kadr: tel. 56 691 20 85.",
    "Kadry i płace",
    "Wyręczamy pracodawców w obowiązkach kadrowo-płacowych: od umowy o pracę, przez listy płac i ZUS, po deklaracje PIT-11.",
    '''<h2>Co robimy w ramach obsługi kadrowej</h2>
<ul>
  <li>sporządzamy umowy o pracę, umowy zlecenia i świadectwa pracy,</li>
  <li>prowadzimy akta osobowe pracowników,</li>
  <li>prowadzimy ewidencję związaną z zatrudnieniem,</li>
  <li>pilnujemy terminów badań lekarskich i szkoleń BHP,</li>
  <li>prowadzimy bieżące sprawy kadrowe.</li>
</ul>
<h2>Płace i ZUS</h2>
<ul>
  <li>sporządzamy listy płac i naliczamy wynagrodzenia,</li>
  <li>przygotowujemy rozliczenia i dokumentację ZUS,</li>
  <li>sporządzamy roczne deklaracje PIT-11 dla pracowników.</li>
</ul>
<h2>Jak liczymy cenę</h2>
<p>Pakiet kadry i płace wyceniamy za każdą zatrudnioną osobę, od 60 zł netto. Szczegóły znajdziesz w <a href="{R}cennik/">cenniku</a>, a dokładną kwotę podamy po krótkiej rozmowie o liczbie pracowników i rodzajach umów.</p>
<p class="ramka">Dział kadr ma osobny numer: <a href="tel:+48566912085">56 691 20 85</a>, e-mail <a href="mailto:kadry@buchalter.home.pl">kadry@buchalter.home.pl</a>.</p>''',
    "Kadry i płace",
    '<small class="kadry">dział kadr: <a href="tel:+48566912085">56 691 20 85</a></small>'))

# ---------------------------------------------------------------- PODATKI
strony.append(usluga("oferta/podatki/", "Rozliczenia podatkowe",
    "Rozliczenia podatkowe Chełmno - firmy, osoby prywatne, rolnicy | Buchalter",
    "Ewidencja i rozliczenia podatkowe firm i osób prywatnych w Chełmnie: najem prywatny, VAT dla rolników, reprezentacja przed organami kontroli podatkowej. Biuro Rachunkowe Buchalter.",
    "Rozliczenia podatkowe",
    "Ewidencja i rozliczenia podatkowe firm, mikrofirm, osób prywatnych i rolników, zgodnie z obowiązującymi przepisami. W razie kontroli reprezentujemy podatnika.",
    '''<h2>Podatki w firmie</h2>
<p>Prowadzimy ewidencje podatkowe i rozliczamy podatki naszych klientów. Co miesiąc dostajesz informację, ile podatku i składek ZUS trzeba zapłacić i do kiedy, więc nie musisz sam pilnować terminów.</p>
<h2 id="osoby-prywatne-i-rolnicy">Osoby prywatne i rolnicy</h2>
<p>Pomagamy także osobom, które nie prowadzą działalności gospodarczej. Prowadzimy ewidencje podatkowe osób prywatnych i rolników:</p>
<ul>
  <li>najem prywatny,</li>
  <li>rozliczanie VAT dla rolników, także sama obsługa VAT dla rolników rozliczających VAT na zasadach ogólnych (więcej w części o <a href="{R}oferta/ksiegowosc/#vat">ewidencji i rozliczeniach VAT</a>).</li>
</ul>
<p>Zadzwoń do recepcji i powiedz, czego dotyczy rozliczenie, a umówimy termin.</p>
<h2>Kontrola podatkowa</h2>
<p>Reprezentujemy podatników przed organami kontroli podatkowej.</p>
<h2>Zmiany w przepisach</h2>
<p>Śledzimy zmiany w przepisach podatkowych i informujemy klientów o tych, które ich dotyczą.</p>''',
    "Rozliczenia podatkowe"))

# ---------------------------------------------------------------- ZAKLADANIE
strony.append(usluga("oferta/zakladanie-dzialalnosci/", "Zakładanie działalności",
    "Zakładanie działalności Chełmno - forma działalności, rejestracja | Buchalter",
    "Pomoc w zakładaniu firmy w Chełmnie: wybór formy działalności, formalności urzędowe, rejestracja spółki w KRS, współpraca z kancelarią prawno-podatkową. Biuro Rachunkowe Buchalter.",
    "Zakładanie działalności gospodarczej",
    "Pomagamy wybrać formę działalności, a potem załatwiamy formalności - także przy rejestracji spółki w KRS. Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową.",
    '''<h2>Wybór formy działalności</h2>
<p>Doradzamy, czy lepsza będzie jednoosobowa działalność, czy spółka - tak, żeby forma odpowiadała Twoim planom i zabezpieczała Twoje interesy.</p>
<h2>Wybór formy opodatkowania</h2>
<p>Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową, w której pracują radcy prawni i doradcy podatkowi.</p>
<h2>Formalności</h2>
<p>Możesz zlecić nam formalności urzędowe związane z rejestracją działalności, w tym rejestrację spółki w Krajowym Rejestrze Sądowym.</p>
<h2>Co przygotować na pierwszą rozmowę</h2>
<ul>
  <li>czym firma będzie się zajmować i od kiedy chcesz zacząć,</li>
  <li>jakich przychodów i kosztów się spodziewasz w pierwszym roku,</li>
  <li>czy planujesz zatrudniać pracowników albo zleceniobiorców,</li>
  <li>czy zakładasz firmę sam, czy ze wspólnikami.</li>
</ul>
<p>Po rejestracji możemy od pierwszego miesiąca prowadzić księgowość i kadry nowej firmy.</p>''',
    "Zakładanie działalności"))

# ---------------------------------------------------------------- JAK PRACUJEMY
jp = glowa("Jak pracujemy",
           "Musisz działać szybko i potrzebujesz kogoś, kto sprawnie załatwi sprawy firmy. Rozumiemy to i tak organizujemy pracę, żeby być do dyspozycji wtedy, kiedy nas potrzebujesz.",
           [("Jak pracujemy", "jak-pracujemy/")]) + f'''
<section>
  <div class="wrap dwie">
    <div>
      <ul class="punkty">
        <li><b>Odpowiadamy szybko.</b> Na pytania odpowiadamy niezwłocznie i pomagamy, gdy trzeba coś pilnie wyjaśnić.</li>
        <li><b>Dokumenty w wygodnej formie.</b> Zdecydowana większość faktur trafia do nas z KSeF. Dokumenty spoza KSeF, np. faktury zagraniczne, możesz przesyłać elektronicznie albo zostawić w recepcji przy ul. Rybackiej 3.</li>
        <li><b>Księgujemy i archiwizujemy.</b> Po otrzymaniu dokumentów księgujemy je. Faktur z KSeF nie drukujemy. Po zakończeniu roku i sporządzeniu zeznania rocznego archiwizujemy dokumenty papierowe, a ewidencje podatkowe przekazujemy Ci elektronicznie.</li>
        <li><b>Pilnujemy terminów.</b> Co miesiąc dostajesz informację o wysokości i terminie podatków oraz składek ZUS.</li>
        <li><b>Działy według rodzaju klientów.</b> Każdy dział obsługuje firmy z określonych branż, o tej samej formie prawnej i sposobie rozliczeń.</li>
        <li><b>Ciągłość obsługi.</b> Zespół jest na tyle duży, że sezon urlopowy czy nieobecność jednej osoby nie wstrzymuje pracy nad Twoimi sprawami.</li>
      </ul>
    </div>
    <figure class="foto"><img src="{{R}}assets/img/spotkanie-1400.webp" srcset="{{R}}assets/img/spotkanie-800.webp 800w, {{R}}assets/img/spotkanie-1400.webp 1400w" sizes="(max-width: 960px) 100vw, 600px" alt="Rozmowa księgowego z klientem przy stole w biurze" width="1400" height="788" loading="lazy"></figure>
  </div>
</section>

<section class="szare" id="jak-zaczac">
  <div class="wrap dwie dwie-gora">
    <div>
      <h2>Jak zacząć współpracę</h2>
      <p class="lead2">Najprościej zadzwonić do recepcji pod numer <a href="tel:{TEL_H}">{TEL}</a> albo napisać przez <a href="{{R}}kontakt/#formularz">formularz</a>.</p>
      <p class="odst">Zapytamy o formę działalności, sposób opodatkowania, przybliżoną liczbę dokumentów w miesiącu i to, czy zatrudniasz pracowników. Na tej podstawie przygotujemy bezpłatną wycenę. Jeśli ją zaakceptujesz, podpisujemy umowę i ustalamy, od którego miesiąca przejmujemy księgowość oraz w jaki sposób będziesz przekazywać dokumenty.</p>
      <p class="odst">Ustalamy też sposób dostarczania faktur z KSeF: możesz korzystać z udostępnianej przez nas aplikacji (Betterfly od Comarch, prosta, również mobilna) albo sami będziemy pobierać Twoje faktury. Pomagamy nadać odpowiednie uprawnienia w KSeF.</p>
    </div>
    <div>
      <h2>Jakie dokumenty przygotować</h2>
      <p class="odst">Przy przejściu do nas z innego biura albo od własnej księgowości zwykle przydają się:</p>
      <ul class="punkty punkty-dok">
        <li>dane firmy: NIP, REGON, a w przypadku spółki numer KRS i umowa spółki,</li>
        <li>informacja o formie opodatkowania i o tym, czy firma jest czynnym podatnikiem VAT,</li>
        <li>księgi lub ewidencje i deklaracje za bieżący rok oraz wykaz środków trwałych,</li>
        <li>przy zatrudnieniu: akta osobowe, umowy i dokumenty płacowe pracowników.</li>
      </ul>
      <p class="odst">Nie musisz mieć wszystkiego od razu - dokładną listę ustalimy przy pierwszej rozmowie.</p>
    </div>
  </div>
</section>

<section id="pytania">
  <div class="wrap dwie dwie-gora">
    <div>
      <h2>Najczęstsze pytania</h2>
      <p class="lead2">Nie ma tu odpowiedzi na Twoje pytanie? Zadzwoń do recepcji: <a href="tel:{TEL_H}">{TEL}</a>.</p>
    </div>
    <div class="faq"><details><summary>Ile kosztuje prowadzenie księgowości?</summary><p>Ceny zaczynają się od: księga przychodów i rozchodów 200 zł netto, ryczałt 180 zł netto, księgi handlowe 800 zł netto, kadry i płace 60 zł netto. Dokładna kwota zależy od formy działalności i opodatkowania, liczby dokumentów w miesiącu i liczby pracowników. Wycena jest bezpłatna - wystarczy telefon do recepcji albo wiadomość przez formularz.</p></details><details><summary>Czy muszę przychodzić do biura z dokumentami?</summary><p>Nie. Zdecydowana większość faktur trafia do nas z KSeF. Pozostałe dokumenty, np. faktury zagraniczne, możesz przesyłać elektronicznie albo zostawić w recepcji przy ul. Rybackiej 3.</p></details><details><summary>Czy przypomnicie mi o podatku i ZUS?</summary><p>Tak. Co miesiąc dostajesz informację o wysokości i terminie zapłaty podatków oraz składek ZUS.</p></details><details><summary>Czy mogę wglądać w swoje dokumenty?</summary><p>Tak. Faktury z KSeF masz zawsze w KSeF. Dokumenty papierowe archiwizujemy po zakończeniu roku i sporządzeniu zeznania rocznego, a ewidencje podatkowe przekazujemy Ci elektronicznie.</p></details><details><summary>Czy prowadzicie kadry i płace?</summary><p>Tak, mamy osobny dział kadr: tel. 56 691 20 85, kadry@buchalter.home.pl. Przygotowujemy umowy, listy płac, rozliczenia ZUS i deklaracje PIT-11.</p></details><details><summary>Czy pomagacie osobom, które nie prowadzą firmy?</summary><p>Tak. Rozliczamy podatki osób nieprowadzących działalności gospodarczej i prowadzimy ewidencje podatkowe osób prywatnych i rolników, np. najem prywatny i rozliczanie VAT dla rolników.</p></details><details><summary>Czy pomożecie założyć firmę albo spółkę?</summary><p>Tak. Pomagamy wybrać formę działalności i załatwiamy formalności, także rejestrację spółki w KRS. Przy wyborze formy opodatkowania współpracujemy z kancelarią prawno-podatkową (radcy prawni, doradcy podatkowi).</p></details></div>
  </div>
</section>'''
strony.append(strona("jak-pracujemy/", "Jak pracujemy i jak zacząć współpracę | Buchalter Chełmno",
                     "Jak pracuje Biuro Rachunkowe Buchalter w Chełmnie: faktury z KSeF, pozostałe dokumenty elektronicznie lub w recepcji, terminy podatków i ZUS. Jak zacząć współpracę.",
                     jp, akt="jak-pracujemy/", okruszki=[("Jak pracujemy", "jak-pracujemy/")], schema_extra=FAQ_LD))

# ---------------------------------------------------------------- O BIURZE
ob = glowa("O biurze",
           "Biuro Rachunkowe Buchalter działa w Chełmnie od 1999 roku. Obsługujemy firmy, organizacje i osoby prywatne z Chełmna i okolic.",
           [("O biurze", "o-biurze/")]) + '''
<section class="foto-pas">
  <div class="wrap"><figure class="foto foto-szeroka"><img src="{R}assets/img/narada-1400.webp" srcset="{R}assets/img/narada-800.webp 800w, {R}assets/img/narada-1400.webp 1400w" sizes="(max-width: 1240px) 100vw, 1200px" alt="Rozmowa z klientami przy stole w biurze" width="1400" height="788" loading="lazy"></figure></div>
</section>
<section>
  <div class="wrap dwie dwie-gora">
    <div class="tresc">
      <h2>Biuro podzielone na działy</h2>
      <p>Potrzebujesz pewności, że księgowość Twojej firmy jest prowadzona prawidłowo. Dlatego biuro jest podzielone na działy, z których każdy specjalizuje się w obsłudze klientów określonego typu: z podobnych branż, o tej samej formie prawnej i sposobie rozliczeń.</p>
      <p>Nasi księgowi mają kierunkowe wykształcenie i stale poszerzają wiedzę na szkoleniach i kursach. Na co dzień prowadzą różnorodne i złożone sprawy księgowe oraz kadrowe.</p>
      <p>Obsługujemy jednoosobowe działalności, spółki, spółki-córki dużych firm, fundacje i stowarzyszenia, a także osoby prywatne.</p>
      <p>Współpracujemy z kancelarią prawno-podatkową, w której pracują radcy prawni i doradcy podatkowi.</p>
    </div>
    <div class="tresc">
      <h2>Wioletta Prełowska</h2>
      <p>Właścicielka Biura Rachunkowego Buchalter od 1999 roku. W rachunkowości pracuje od ponad 30 lat.</p>
      <ul class="sciezka sciezka-jasna">
        <li><span>od 1995</span><p>Pierwsze doświadczenia zawodowe na stanowiskach księgowej i samodzielnej księgowej.</p></li>
        <li><span>1999</span><p>Świadectwo kwalifikacyjne uprawniające do usługowego prowadzenia ksiąg rachunkowych.</p></li>
        <li><span>2001-2002</span><p>Ukończone wszystkie stopnie kursów księgowych prowadzonych przez Stowarzyszenie Księgowych w Polsce.</p></li>
        <li><span>2018</span><p>Wpis na Listę Sygnatariuszy Kodeksu Etyki Zawodowej w Rachunkowości, prowadzoną przez Zarząd Główny Stowarzyszenia Księgowych w Polsce pod patronatem Komisji Etyki.</p></li>
        <li><span>Wykształcenie</span><p>Studia magisterskie na kierunku Zarządzanie Finansami Przedsiębiorstw, wcześniej studia licencjackie na kierunku rachunkowość.</p></li>
      </ul>
    </div>
  </div>
</section>'''
strony.append(strona("o-biurze/", "O biurze - Wioletta Prełowska, biuro rachunkowe od 1999 | Buchalter",
                     "Biuro Rachunkowe Buchalter w Chełmnie działa od 1999 roku. Właścicielka Wioletta Prełowska: ponad 30 lat w rachunkowości, sygnatariuszka Kodeksu Etyki.",
                     ob, akt="o-biurze/", okruszki=[("O biurze", "o-biurze/")]))

# ---------------------------------------------------------------- CENNIK
def pakiet(nazwa, pozycje, cena, temat):
    li = "".join(f"<li>{p}</li>" for p in pozycje)
    return f'''<article class="pakiet">
  <h2>{nazwa}</h2>
  <ul>{li}</ul>
  <p class="cena">{cena}<small>dokładna wycena bezpłatna</small></p>
  <a class="btn-out" href="{{R}}kontakt/?temat={temat}#formularz">Zapytaj o wycenę</a>
</article>'''

wsp = ["Informacja o wysokości i terminie podatków oraz składek ZUS", "Konsultacje w sprawie bieżącej sytuacji firmy"]
cn = glowa("Cennik usług księgowych",
           "Zobacz, co wchodzi w skład naszych pakietów i od jakich kwot zaczynają się ceny. Dokładną cenę ustalamy indywidualnie, bo zależy od wielkości i rodzaju firmy - wycena jest bezpłatna.",
           [("Cennik", "cennik/")]) + f'''
<section>
  <div class="wrap">
    <div class="pakiety">
      {pakiet("Księgi podatkowe", ["Ewidencja dokumentów księgowych"] + wsp, "od 200 zł netto", "Księgi podatkowe")}
      {pakiet("Ryczałt", ["Prowadzenie ewidencji ryczałtowych"] + wsp, "od 180 zł netto", "Ryczałt")}
      {pakiet("Księgi handlowe", ["Ewidencja dokumentów księgowych"] + wsp, "od 800 zł netto", "Księgi handlowe")}
      {pakiet("Kadry i płace", ["Sporządzanie list płac pracowników", "Naliczanie wynagrodzeń", "Prowadzenie akt pracowniczych", "Sporządzanie deklaracji PIT-11"], "od 60 zł netto", "Kadry i płace")}
    </div>
    <div class="pod-cennikiem">
      <div>
        <h2>O co zapytamy przy wycenie</h2>
        <ul>
          <li>forma działalności i sposób opodatkowania,</li>
          <li>przybliżona liczba dokumentów w miesiącu,</li>
          <li>czy firma jest czynnym podatnikiem VAT,</li>
          <li>liczba pracowników i zleceniobiorców.</li>
        </ul>
      </div>
      <div>
        <h2>Jak dostać wycenę</h2>
        <p>Zadzwoń do recepcji pod numer <a href="tel:{TEL_H}">{TEL}</a> albo wyślij <a href="{{R}}kontakt/#formularz">krótką wiadomość przez formularz</a>. Odpowiemy z wyceną dopasowaną do Twojej firmy.</p>
      </div>
    </div>
  </div>
</section>'''
strony.append(strona("cennik/", "Cennik biura rachunkowego Chełmno - pakiety | Buchalter",
                     "Cennik Biura Rachunkowego Buchalter w Chełmnie: KPiR od 200 zł netto, ryczałt od 180 zł netto, księgi handlowe od 800 zł netto, kadry i płace od 60 zł netto.",
                     cn, akt="cennik/", okruszki=[("Cennik", "cennik/")]))

# ---------------------------------------------------------------- KONTAKT
tematy = ["Bezpłatna wycena", "Księgi podatkowe", "Ryczałt", "Księgi handlowe", "Księgowość", "Kadry i płace", "Rozliczenia podatkowe", "Zakładanie działalności", "Inne pytanie"]
opcje = "".join(f"<option>{t}</option>" for t in tematy)
kt = glowa("Kontakt z biurem",
           "Masz pytania do oferty albo nie wiesz, czy możemy Ci pomóc? Zadzwoń, napisz albo przyjdź do biura przy ul. Rybackiej 3 w Chełmnie.",
           [("Kontakt", "kontakt/")]) + f'''
<section>
  <div class="wrap kontakt-in">
    <div>
      <dl class="dane">
        <div><dt>Recepcja</dt><dd><a class="nr" href="tel:{TEL_H}">{TEL}</a><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
        <div><dt>Kadry i płace</dt><dd><a class="nr" href="tel:{TEL_K_H}">{TEL_K}</a><a href="mailto:{MAIL_K}">{MAIL_K}</a></dd></div>
        <div><dt>Adres biura</dt><dd>ul. Rybacka 3 lok. 1<br>86-200 Chełmno<br><a href="{TRASA}" target="_blank" rel="noopener">Wyznacz trasę w Mapach Google</a></dd></div>
        <div><dt>Godziny pracy</dt><dd>poniedziałek - piątek: 9:00-16:00<br>sobota, niedziela: nieczynne</dd></div>
        <div><dt>Dane firmy</dt><dd>Biuro Rachunkowe „Buchalter” Prełowska Wioletta<br>NIP 875-109-86-47<br>REGON 871183546</dd></div>
      </dl>
      {MAPA}
    </div>
    <form class="formularz" id="formularz" novalidate>
      <h2>Napisz do nas</h2>
      <label>Imię i nazwisko<input name="imie" autocomplete="name"></label>
      <label>E-mail lub telefon *<input name="kontakt" required autocomplete="email" aria-describedby="formWynik"></label>
      <label>Czego dotyczy pytanie<select name="temat">{opcje}</select></label>
      <label>Wiadomość *<textarea name="wiadomosc" rows="5" required placeholder="Np. forma działalności, liczba dokumentów w miesiącu, liczba pracowników"></textarea></label>
      <label class="pulapka" aria-hidden="true">Strona www<input name="www" tabindex="-1" autocomplete="off"></label>
      <button class="btn" type="submit">Wyślij wiadomość</button>
      <p class="wynik" id="formWynik" role="status" hidden></p>
      <p class="uwaga">Dane z formularza wykorzystamy tylko do odpowiedzi na wiadomość. Szczegóły w <a href="{{R}}polityka-prywatnosci/">polityce prywatności</a>.</p>
      <p class="test-uw"><b>Wersja testowa:</b> formularz jest makietą i niczego nie wysyła. Po uruchomieniu strony wiadomości będą trafiać na adres {MAIL}.</p>
    </form>
  </div>
</section>'''
strony.append(strona("kontakt/", "Kontakt - biuro rachunkowe Chełmno, ul. Rybacka 3 | Buchalter",
                     "Biuro Rachunkowe Buchalter, ul. Rybacka 3, 86-200 Chełmno. Recepcja: tel. 56 691 20 80, recepcja@buchalter.home.pl. Kadry: tel. 56 691 20 85. Formularz i dojazd.",
                     kt, akt="kontakt/", okruszki=[("Kontakt", "kontakt/")]))

# ---------------------------------------------------------------- POLITYKA
pp = glowa("Polityka prywatności",
           "Jak przetwarzamy dane osób, które kontaktują się z biurem przez stronę internetową.",
           [("Polityka prywatności", "polityka-prywatnosci/")]) + f'''
<section>
  <div class="wrap">
    <div class="tresc">
      <h2>Administrator danych</h2>
      <p>Administratorem danych osobowych jest Wioletta Prełowska, prowadząca działalność gospodarczą pod firmą BIURO RACHUNKOWE "BUCHALTER" PREŁOWSKA WIOLETTA, ul. Rybacka 3 lok. 1, 86-200 Chełmno, NIP 875-109-86-47, REGON 871183546. Kontakt w sprawie danych: <a href="mailto:{MAIL}">{MAIL}</a>, tel. <a href="tel:{TEL_H}">{TEL}</a>.</p>
      <h2>Jakie dane i po co</h2>
      <p>Gdy wysyłasz wiadomość przez formularz, piszesz e-mail albo dzwonisz, przetwarzamy dane, które nam podajesz: imię i nazwisko, adres e-mail lub numer telefonu oraz treść wiadomości. Wykorzystujemy je wyłącznie po to, żeby odpowiedzieć na pytanie, przygotować wycenę albo podjąć działania przed zawarciem umowy na Twoje żądanie.</p>
      <p>Podstawą prawną jest art. 6 ust. 1 lit. b RODO (działania przed zawarciem umowy) oraz art. 6 ust. 1 lit. f RODO (nasz prawnie uzasadniony interes, czyli odpowiedź na wiadomość).</p>
      <h2>Jak długo przechowujemy dane</h2>
      <p>Korespondencję przechowujemy przez czas potrzebny do udzielenia odpowiedzi i ewentualnej dalszej rozmowy o współpracy, nie dłużej niż 12 miesięcy od ostatniego kontaktu. Jeśli zawrzemy umowę, dane przetwarzamy na zasadach opisanych w umowie i przez okres wynikający z przepisów.</p>
      <h2>Komu przekazujemy dane</h2>
      <p>Dane mogą być przetwarzane przez dostawców usług, z których korzystamy przy prowadzeniu strony i poczty (hosting i poczta e-mail), wyłącznie na nasze zlecenie. Nie sprzedajemy danych i nie przekazujemy ich do państw spoza Europejskiego Obszaru Gospodarczego.</p>
      <h2>Twoje prawa</h2>
      <p>Masz prawo do dostępu do swoich danych, ich sprostowania, usunięcia lub ograniczenia przetwarzania, wniesienia sprzeciwu oraz przenoszenia danych. Masz też prawo wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych (ul. Stawki 2, 00-193 Warszawa). Podanie danych jest dobrowolne, ale bez danych kontaktowych nie odpowiemy na wiadomość.</p>
      <h2 id="cookies">Pliki cookie i usługi zewnętrzne</h2>
      <p>Strona nie używa plików cookie do statystyk ani reklam i nie śledzi odwiedzających. Czcionki są wczytywane z naszego serwera.</p>
      <p><b>Niezbędne:</b> w pamięci przeglądarki (localStorage) zapisujemy Twój wybór dotyczący cookies, na 12 miesięcy. Bez tego baner pokazywałby się przy każdej wizycie.</p>
      <p><b>Mapy Google:</b> na stronie głównej i kontaktowej jest osadzona mapa Google. Podczas jej wyświetlania Google LLC może zapisywać własne pliki cookie i otrzymuje adres IP przeglądarki, zgodnie z <a href="https://policies.google.com/privacy?hl=pl" rel="noopener" target="_blank">polityką prywatności Google</a>. Jeśli wybierzesz "Tylko niezbędne", zamiast mapy pokażemy adres i link do wyznaczenia trasy.</p>
      <p>Swój wybór możesz zmienić w każdej chwili przyciskiem "Ustawienia cookies" w stopce strony. Link do profilu na Facebooku prowadzi do serwisu Meta, który stosuje własne zasady.</p>
      <p class="drobny">Ostatnia aktualizacja: 5 listopada 2026 r.</p>
    </div>
  </div>
</section>'''
strony.append(strona("polityka-prywatnosci/", "Polityka prywatności | Biuro Rachunkowe Buchalter Chełmno",
                     "Polityka prywatności strony Biura Rachunkowego Buchalter w Chełmnie: administrator danych, cel i podstawa przetwarzania, prawa osób, pliki cookie.",
                     pp, okruszki=[("Polityka prywatności", "polityka-prywatnosci/")]))

# ---------------------------------------------------------------- 404
e404 = '''<section class="glowa-strony" style="min-height:60svh;display:flex;align-items:center">
  <div class="wrap">
    <h1>Nie ma takiej strony</h1>
    <p class="lead">Adres mógł się zmienić po przebudowie strony. Wybierz, czego szukasz:</p>
    <p style="margin-top:24px;display:flex;gap:16px 28px;flex-wrap:wrap"><a class="btn" href="https://wylinka-podglad.pl/buchalter-koncepcja/">Strona główna</a><a class="link-strz" href="https://wylinka-podglad.pl/buchalter-koncepcja/oferta/">Oferta</a><a class="link-strz" href="https://wylinka-podglad.pl/buchalter-koncepcja/cennik/">Cennik</a><a class="link-strz" href="https://wylinka-podglad.pl/buchalter-koncepcja/kontakt/">Kontakt</a></p>
  </div>
</section>'''
strona("404.html", "Nie ma takiej strony | Buchalter", "Strona nie istnieje.", e404)

# ---------------------------------------------------------------- sitemap / robots
sm = "".join(f"<url><loc>{PROD}{p}</loc><lastmod>{DZIS}</lastmod></url>" for p in strony)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text("# Wersja testowa - nie indeksować\nUser-agent: *\nDisallow: /\n" if TEST else f"User-agent: *\nAllow: /\nSitemap: {PROD}sitemap.xml\n", encoding="utf-8")
(Path(__file__).parent / "robots_produkcja.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PROD}sitemap.xml\n", encoding="utf-8")
print("OK", len(strony) + 1, "stron:", ", ".join(p or "/" for p in strony))
