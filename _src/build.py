# -*- coding: utf-8 -*-
"""Generator wersji testowej strony Biura Rachunkowego Buchalter (Chełmno).
Uruchomienie: python _src/build.py  -> strony w katalogach obok (index.html), sitemap.xml, robots.txt, 404.html.
Dane firmy wyłącznie z obecnej strony buchalter.cloud i umowy (CEIDG). Bez kwot w cenniku do czasu decyzji klientki."""
import json, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROD = "https://buchalter.cloud/"      # docelowy adres (do potwierdzenia przez klientkę)
KIER = os.environ.get("KIERUNEK", "")   # prototypy kierunkow: a / b / c
TEST = True                            # wersja testowa: noindex + robots Disallow
DZIS = "2026-11-05"
BADGE = (Path(__file__).parent / "badge.html").read_text(encoding="utf-8").strip()

TEL = "56 691 20 80"; TEL_H = "+48566912080"
TEL_K = "56 691 20 85"; TEL_K_H = "+48566912085"
MAIL = "recepcja@buchalter.home.pl"; MAIL_K = "kadry@buchalter.home.pl"
FB = "https://www.facebook.com/profile.php?id=100063471177071"
TRASA = "https://www.google.com/maps/dir/?api=1&amp;destination=Rybacka+3%2C+86-200+Che%C5%82mno"

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
    "knowsAbout": ["księgowość", "księga przychodów i rozchodów", "ryczałt ewidencjonowany", "pełna księgowość", "kadry i płace", "rozliczenia podatkowe", "zakładanie działalności gospodarczej"],
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
      <ul><li><a href="{{R}}jak-pracujemy/">Jak pracujemy</a></li><li><a href="{{R}}o-biurze/">O biurze</a></li><li><a href="{{R}}kontakt/">Kontakt i dojazd</a></li><li><a href="{FB}" rel="noopener" target="_blank">Facebook</a></li><li><a href="{{R}}polityka-prywatnosci/">Polityka prywatności</a></li></ul>
    </div>
  </div>
  <div class="wrap stopka-dol">
    <span>&copy; 2026 Biuro Rachunkowe Buchalter. Wersja testowa nowej strony. Zdjęcie Rynku w Chełmnie: <a href="https://commons.wikimedia.org/wiki/File:Che%C5%82mno_Market_Square.jpg" rel="noopener" target="_blank">Margoz</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pl" rel="noopener" target="_blank">CC BY-SA 4.0</a>; pozostałe zdjęcia poglądowe.</span>
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
    preload = ('<link rel="preload" as="image" href="{R}assets/img/rynek-tel-900.webp" media="(max-width: 760px)">\n'
               '<link rel="preload" as="image" imagesrcset="{R}assets/img/rynek-1000.webp 1000w, {R}assets/img/rynek-1600.webp 1600w, {R}assets/img/rynek-2400.webp 2400w" imagesizes="100vw" media="(min-width: 761px)">\n') if home else ""
    kier_css = f'<link rel="stylesheet" href="{{R}}_src/kierunki/{KIER}.css">\n' if KIER and home else ""
    html = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{robots}<title>{title}</title>
<meta name="description" content="{desc}">
{canon}<meta name="theme-color" content="#0a3563">
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
<link rel="preload" as="font" type="font/woff2" href="{{R}}assets/fonts/sourceserif4-n-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{{R}}assets/fonts/ibmplexsans-n-latin.woff2" crossorigin>
{preload}<link rel="stylesheet" href="{{R}}assets/css/style.css?v=2">
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
<script src="{{R}}assets/js/site.js?v=1" defer></script>
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


def glowa(h1, lead, okruszki):
    li = '<li><a href="{R}">Strona główna</a></li>'
    for i, (n, h) in enumerate(okruszki):
        cur = ' aria-current="page"' if i == len(okruszki) - 1 else ""
        li += f'<li><a href="{{R}}{h}"{cur}>{n}</a></li>'
    return f'''<section class="glowa-strony">
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
FAQ_LD = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Ile kosztuje prowadzenie księgowości?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Cenę ustalamy indywidualnie. Zależy od formy działalności i opodatkowania, liczby dokumentów w miesiącu i liczby pracowników. Wycena jest bezpłatna - wystarczy telefon do recepcji albo wiadomość przez formularz.'}}, {'@type': 'Question', 'name': 'Czy muszę przychodzić do biura z dokumentami?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Nie. Faktury i inne dokumenty możesz przesyłać elektronicznie. Jeśli wolisz, możesz je też zostawić w recepcji przy ul. Rybackiej 3.'}}, {'@type': 'Question', 'name': 'Czy przypomnicie mi o podatku i ZUS?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Co miesiąc dostajesz informację o wysokości i terminie zapłaty podatków oraz składek ZUS.'}}, {'@type': 'Question', 'name': 'Czy mogę wglądać w swoje dokumenty?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Zaksięgowane dokumenty archiwizujemy i w każdej chwili możesz je przejrzeć oraz skopiować w recepcji biura.'}}, {'@type': 'Question', 'name': 'Czy prowadzicie kadry i płace?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak, mamy osobny dział kadr: tel. 56 691 20 85, kadry@buchalter.home.pl. Przygotowujemy umowy, listy płac, rozliczenia ZUS i deklaracje PIT-11.'}}, {'@type': 'Question', 'name': 'Czy pomagacie osobom, które nie prowadzą firmy?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Wśród naszych klientów są osoby nieprowadzące działalności gospodarczej - rozliczamy ich podatki.'}}, {'@type': 'Question', 'name': 'Czy pomożecie założyć firmę albo spółkę?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Pomagamy wybrać formę działalności i opodatkowania oraz załatwiamy formalności, także rejestrację spółki w KRS.'}}]}

# ---------------------------------------------------------------- STRONA GLOWNA
home = f'''<section class="hero">
  <figure class="hero-foto">
    <picture>
      <source media="(max-width: 760px)" srcset="{{R}}assets/img/rynek-tel-900.webp">
      <img src="{{R}}assets/img/rynek-1600.webp" srcset="{{R}}assets/img/rynek-1000.webp 1000w, {{R}}assets/img/rynek-1600.webp 1600w, {{R}}assets/img/rynek-2400.webp 2400w" sizes="100vw" alt="Rynek w Chełmnie z renesansowym ratuszem, widok z góry" width="1600" height="1225" fetchpriority="high">
    </picture>
  </figure>
  <div class="hero-in">
    <div class="wrap">
      <div class="hero-karta">
        <p class="adres">ul. Rybacka 3, Chełmno, pon.-pt. 9:00-16:00</p>
        <h1>Biuro rachunkowe w&nbsp;Chełmnie od&nbsp;1999&nbsp;roku</h1>
        <p class="lead">Księgowość, kadry i płace oraz podatki firm, fundacji i osób prywatnych. Dokumenty możesz przesyłać elektronicznie.</p>
        <div class="hero-cta" id="heroCta">
          <a class="btn" href="{{R}}kontakt/#formularz">Bezpłatna wycena</a>
          <a class="link-strz dol" href="#oferta">Zobacz ofertę</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="powody">
  <div class="wrap powody-in">
    <h2>Kompetentna obsługa księgowa bez wysokich kosztów</h2>
    <div class="trzy">
      <div>
        <h3>Wygodnie, także zdalnie</h3>
        <p>Dokumenty możesz przesyłać elektronicznie - nie musisz przychodzić do biura. Zespół jest na tyle duży, że urlop czy nieobecność jednej osoby nie zatrzymuje pracy nad Twoimi sprawami.</p>
      </div>
      <div>
        <h3>Bezpiecznie</h3>
        <p>Nasi księgowi mają kierunkowe wykształcenie i stale się szkolą, śledząc zmiany w przepisach. Na co dzień prowadzą różnorodne i złożone sprawy księgowe oraz kadrowe.</p>
      </div>
      <div>
        <h3>Rozsądnie cenowo</h3>
        <p>Wiedzę i doświadczenie zespołu dzielisz z innymi klientami biura. Dzięki temu masz rzetelną obsługę księgową bez kosztu zatrudniania własnej księgowej.</p>
      </div>
    </div>
  </div>
</section>

<section class="szare" id="oferta">
  <div class="wrap">
    <div class="sek-glowa">
      <h2>Co możemy dla Ciebie zrobić</h2>
      <p>Obsługujemy jednoosobowe działalności, spółki, fundacje i stowarzyszenia, a także spółki-córki dużych firm. Pomagamy również osobom, które nie prowadzą działalności gospodarczej.</p>
    </div>
    <div class="uslugi">
      <article class="usluga">
        <h3><a href="{{R}}oferta/ksiegowosc/">Księga przychodów i ryczałt</a></h3>
        <p>Podatkowa księga przychodów i rozchodów albo ewidencja przychodów dla ryczałtowców, do tego ewidencja środków trwałych. Co miesiąc wiesz, ile i do kiedy zapłacić podatku i składek ZUS.</p>
        <span class="link-strz" aria-hidden="true">Księgowość dla firm</span>
      </article>
      <article class="usluga">
        <h3><a href="{{R}}oferta/ksiegowosc/#pelna-ksiegowosc">Pełna księgowość</a></h3>
        <p>Księgi rachunkowe spółek, fundacji i stowarzyszeń: plan kont, polityka rachunkowości, instrukcje obiegu dokumentów, sprawozdania finansowe i pomoc w ich publikacji.</p>
        <span class="link-strz" aria-hidden="true">Księgi rachunkowe</span>
      </article>
      <article class="usluga">
        <h3><a href="{{R}}oferta/kadry-i-place/">Kadry i płace</a></h3>
        <p>Umowy o pracę i zlecenia, świadectwa pracy, akta osobowe, terminy badań i szkoleń BHP, listy płac, ZUS i deklaracje PIT-11.</p>
        <span class="link-strz" aria-hidden="true">Obsługa kadrowo-płacowa</span>
      </article>
      <article class="usluga">
        <h3><a href="{{R}}oferta/podatki/">Rozliczenia podatkowe</a></h3>
        <p>Ewidencja i rozliczenia podatkowe firm i osób prywatnych. Reprezentujemy podatników przed organami kontroli podatkowej.</p>
        <span class="link-strz" aria-hidden="true">Podatki i kontrole</span>
      </article>
      <article class="usluga">
        <h3><a href="{{R}}oferta/zakladanie-dzialalnosci/">Zakładanie działalności</a></h3>
        <p>Pomagamy wybrać formę działalności i opodatkowania, a potem załatwiamy formalności - także rejestrację spółki w KRS.</p>
        <span class="link-strz" aria-hidden="true">Start firmy</span>
      </article>
      <article class="usluga">
        <h3><a href="{{R}}oferta/#wsparcie">Bieżące wsparcie</a></h3>
        <p>Śledzimy zmiany w przepisach podatkowych i w prawie dotyczącym prowadzenia firmy. Informujemy klientów o tym, co ich dotyczy.</p>
        <span class="link-strz" aria-hidden="true">Cała oferta</span>
      </article>
    </div>
  </div>
</section>

<section class="wspolpraca">
  <div class="wrap">
    <div class="sek-glowa">
      <h2>Jak pracujemy</h2>
      <p>Wiemy, że w firmie liczy się czas. Dlatego jesteśmy do dyspozycji wtedy, kiedy nas potrzebujesz. Tak dzielimy się pracą:</p>
    </div>
    <table class="ksiega">
      <caption class="sr">Podział pracy między klientem a biurem</caption>
      <thead><tr><th scope="col">Po Twojej stronie</th><th scope="col">Po stronie biura</th></tr></thead>
      <tbody>
        <tr><td>Przesyłasz faktury elektronicznie albo zostawiasz je w recepcji przy Rybackiej.</td><td>Księgujemy dokumenty i odkładamy je do archiwum. W każdej chwili możesz je przejrzeć i skopiować w recepcji.</td></tr>
        <tr><td>Pytasz, gdy coś trzeba wyjaśnić.</td><td>Odpowiadamy niezwłocznie i pomagamy rozwiązać sprawę.</td></tr>
        <tr><td>Płacisz podatek i składki.</td><td>Co miesiąc podajemy wysokość i termin zapłaty podatków oraz składek ZUS.</td></tr>
        <tr><td>Prowadzisz firmę.</td><td>Twoje sprawy prowadzi dział, który na co dzień rozlicza firmy o podobnej formie prawnej i sposobie rozliczeń.</td></tr>
      </tbody>
    </table>
    <a class="link-strz po-liscie" href="{{R}}jak-pracujemy/">Jak zacząć współpracę i jakie dokumenty przygotować</a>
  </div>
</section>

<section class="wlascicielka">
  <div class="wrap dwie">
    <div class="ob-glowa">
      <h2>Wioletta Prełowska</h2>
      <p>Właścicielka Biura Rachunkowego Buchalter od 1999 roku. W rachunkowości pracuje od ponad 30 lat.</p>
      <a class="btn btn-jasny" href="{{R}}o-biurze/">Więcej o biurze</a>
    </div>
    <ul class="sciezka">
      <li><span>1999</span><p>Świadectwo kwalifikacyjne uprawniające do usługowego prowadzenia ksiąg rachunkowych.</p></li>
      <li><span>2001-2002</span><p>Wszystkie stopnie kursów Stowarzyszenia Księgowych w Polsce.</p></li>
      <li><span>2018</span><p>Sygnatariuszka Kodeksu Etyki Zawodowej w Rachunkowości.</p></li>
      <li><span>dziś</span><p>Biuro podzielone na działy, z których każdy obsługuje klientów określonego typu.</p></li>
    </ul>
  </div>
</section>

<section class="cennik-sek">
  <div class="wrap dwie dwie-gora">
    <div>
      <h2>Cennik pakietów</h2>
      <p class="lead2">Cenę ustalamy indywidualnie. Zależy od formy działalności, liczby dokumentów w miesiącu i liczby pracowników.</p>
      <a class="btn" href="{{R}}cennik/">Co obejmują pakiety</a>
    </div>
    <table class="rachunek">
      <caption class="sr">Pakiety usług księgowych</caption>
      <tbody>
        <tr><th scope="row">Księgi podatkowe</th><td>wycena indywidualna</td></tr>
        <tr><th scope="row">Ryczałt</th><td>wycena indywidualna</td></tr>
        <tr><th scope="row">Księgi handlowe</th><td>wycena indywidualna</td></tr>
        <tr><th scope="row">Kadry i płace</th><td>za osobę, indywidualnie</td></tr>
      </tbody>
      <tfoot><tr><th scope="row">Wycena</th><td>bezpłatna</td></tr></tfoot>
    </table>
  </div>
</section>

<section class="kontakt-pas">
  <div class="wrap kontakt-pas-in">
    <div>
      <h2>Biuro przy ul. Rybackiej 3 w Chełmnie</h2>
      <p>Zadzwoń, napisz albo wpadnij do recepcji. Powiedz, jaką masz firmę, a przygotujemy bezpłatną wycenę.</p>
      <a class="btn" href="{{R}}kontakt/#formularz">Napisz do biura</a>
    </div>
    <dl class="telefony">
      <div><dt>Recepcja</dt><dd><a class="nr" href="tel:{TEL_H}">{TEL}</a><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      <div><dt>Kadry i płace</dt><dd><a class="nr" href="tel:{TEL_K_H}">{TEL_K}</a><a href="mailto:{MAIL_K}">{MAIL_K}</a></dd></div>
      <div><dt>Adres i godziny</dt><dd>ul. Rybacka 3, 86-200 Chełmno<br>pon.-pt. 9:00-16:00<br><a href="{TRASA}" target="_blank" rel="noopener">Wyznacz trasę</a></dd></div>
    </dl>
  </div>
</section>'''

strony.append(strona("", "Biuro rachunkowe Chełmno - Buchalter, Wioletta Prełowska",
                     "Biuro Rachunkowe Buchalter w Chełmnie, ul. Rybacka 3. Księga przychodów, ryczałt, pełna księgowość, kadry i płace, podatki, zakładanie firmy. Tel. 56 691 20 80.",
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
        <p>Ewidencja i rozliczenia podatkowe firm, mikrofirm i osób prywatnych. Reprezentacja przed organami kontroli podatkowej.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}oferta/zakladanie-dzialalnosci/">Zakładanie działalności</a></h2>
        <p>Wybór formy działalności i opodatkowania, formalności rejestracyjne, rejestracja spółki w KRS.</p>
        <span class="link-strz" aria-hidden="true">Szczegóły</span>
      </article>
      <article class="usluga">
        <h2><a href="{{R}}cennik/">Cennik pakietów</a></h2>
        <p>Co obejmują pakiety: księgi podatkowe, ryczałt, księgi handlowe oraz kadry i płace.</p>
        <span class="link-strz" aria-hidden="true">Zobacz cennik</span>
      </article>
      <article class="usluga" id="wsparcie">
        <h2>Bieżące wsparcie w prowadzeniu firmy</h2>
        <p>Monitorujemy zmiany w przepisach podatkowych i innych przepisach dotyczących prowadzenia działalności. Informujemy klientów o zmianach, które ich dotyczą, i podpowiadamy, co z nich wynika dla firmy.</p>
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
      <li><h3>Osoby prywatne</h3><p>Rozliczenia podatkowe osób, które nie prowadzą działalności gospodarczej.</p></li>
      <li><h3>Nowe firmy</h3><p>Pomoc w wyborze formy działalności i opodatkowania oraz formalności przy rejestracji.</p></li>
    </ul>
  </div>
</section>'''
strony.append(strona("oferta/", "Oferta - biuro rachunkowe Chełmno | Buchalter",
                     "Usługi Biura Rachunkowego Buchalter w Chełmnie: księga przychodów i rozchodów, ryczałt, pełna księgowość, kadry i płace, rozliczenia podatkowe, zakładanie działalności.",
                     of_body, akt="oferta/", okruszki=[("Oferta", "oferta/")]))

# ---------------------------------------------------------------- KSIEGOWOSC
strony.append(usluga("oferta/ksiegowosc/", "Księgowość",
    "Księgowość Chełmno - KPiR, ryczałt, pełna księgowość | Buchalter",
    "Prowadzenie księgowości w Chełmnie: podatkowa księga przychodów i rozchodów, ryczałt ewidencjonowany, pełne księgi rachunkowe spółek i fundacji, sprawozdania finansowe.",
    "Księgowość dla firm i organizacji",
    "Prowadzimy podatkową księgę przychodów i rozchodów, ewidencję przychodów dla ryczałtowców oraz pełne księgi rachunkowe spółek, fundacji i stowarzyszeń.",
    f'''<h2>Księga przychodów i rozchodów</h2>
<p>Prowadzimy podatkową księgę przychodów i rozchodów zgodnie z obowiązującymi przepisami. W ramach obsługi:</p>
<ul>
  <li>ewidencjonujemy dokumenty księgowe,</li>
  <li>co miesiąc informujemy o wysokości i terminie zapłaty podatku oraz składek ZUS,</li>
  <li>konsultujemy bieżącą sytuację firmy, gdy masz pytania albo planujesz zmiany.</li>
</ul>
<h2>Ryczałt ewidencjonowany</h2>
<p>Dla firm rozliczających się ryczałtem prowadzimy ewidencję przychodów. Tak samo jak przy księdze przychodów dostajesz informację o kwocie i terminie podatku oraz składek ZUS, a w razie wątpliwości - konsultację.</p>
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
<h2>Dokumenty elektronicznie albo w recepcji</h2>
<p>Faktury i inne dokumenty możesz przesyłać w formie elektronicznej albo zostawić w biurze przy ul. Rybackiej 3. Po zaksięgowaniu archiwizujemy je, a Ty w każdej chwili możesz je przejrzeć i skopiować w recepcji.</p>''',
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
<p>Pakiet kadry i płace wyceniamy za każdą zatrudnioną osobę. Szczegóły znajdziesz w <a href="{R}cennik/">cenniku</a>, a dokładną kwotę podamy po krótkiej rozmowie o liczbie pracowników i rodzajach umów.</p>
<p class="ramka">Dział kadr ma osobny numer: <a href="tel:+48566912085">56 691 20 85</a>, e-mail <a href="mailto:kadry@buchalter.home.pl">kadry@buchalter.home.pl</a>.</p>''',
    "Kadry i płace",
    '<small class="kadry">dział kadr: <a href="tel:+48566912085">56 691 20 85</a></small>'))

# ---------------------------------------------------------------- PODATKI
strony.append(usluga("oferta/podatki/", "Rozliczenia podatkowe",
    "Rozliczenia podatkowe Chełmno - firmy i osoby prywatne | Buchalter",
    "Ewidencja i rozliczenia podatkowe firm, mikrofirm i osób prywatnych w Chełmnie. Reprezentacja podatników przed organami kontroli podatkowej. Biuro Rachunkowe Buchalter.",
    "Rozliczenia podatkowe",
    "Ewidencja i rozliczenia podatkowe firm, mikrofirm i osób prywatnych, zgodnie z obowiązującymi przepisami. W razie kontroli reprezentujemy podatnika.",
    '''<h2>Podatki w firmie</h2>
<p>Prowadzimy ewidencje podatkowe i rozliczamy podatki naszych klientów. Co miesiąc dostajesz informację, ile podatku i składek ZUS trzeba zapłacić i do kiedy, więc nie musisz sam pilnować terminów.</p>
<h2>Osoby prywatne</h2>
<p>Pomagamy także osobom, które nie prowadzą działalności gospodarczej. Zadzwoń do recepcji i powiedz, czego dotyczy rozliczenie, a umówimy termin.</p>
<h2>Kontrola podatkowa</h2>
<p>Reprezentujemy podatników przed organami kontroli podatkowej.</p>
<h2>Zmiany w przepisach</h2>
<p>Śledzimy zmiany w przepisach podatkowych i informujemy klientów o tych, które ich dotyczą.</p>''',
    "Rozliczenia podatkowe"))

# ---------------------------------------------------------------- ZAKLADANIE
strony.append(usluga("oferta/zakladanie-dzialalnosci/", "Zakładanie działalności",
    "Zakładanie działalności Chełmno - forma, podatek, rejestracja | Buchalter",
    "Pomoc w zakładaniu firmy w Chełmnie: wybór formy działalności i formy opodatkowania, formalności urzędowe, rejestracja spółki w KRS. Biuro Rachunkowe Buchalter.",
    "Zakładanie działalności gospodarczej",
    "Pomagamy wybrać formę działalności i opodatkowania, a potem załatwiamy formalności - także przy rejestracji spółki w KRS.",
    '''<h2>Wybór formy działalności</h2>
<p>Doradzamy, czy lepsza będzie jednoosobowa działalność, czy spółka - tak, żeby forma odpowiadała Twoim planom i zabezpieczała Twoje interesy.</p>
<h2>Wybór formy opodatkowania</h2>
<p>Porównujemy dostępne formy opodatkowania i pomagamy wybrać najkorzystniejszą przy przychodach i kosztach, jakich się spodziewasz.</p>
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
        <li><b>Dokumenty w wygodnej formie.</b> Faktury i inne dokumenty możesz przesyłać elektronicznie albo zostawić w recepcji przy ul. Rybackiej 3.</li>
        <li><b>Księgujemy i archiwizujemy.</b> Po otrzymaniu dokumentów księgujemy je i odkładamy do archiwum. Zawsze możesz je przejrzeć i skopiować w recepcji.</li>
        <li><b>Pilnujemy terminów.</b> Co miesiąc dostajesz informację o wysokości i terminie podatków oraz składek ZUS.</li>
        <li><b>Działy według rodzaju klientów.</b> Każdy dział obsługuje firmy z określonych branż, o tej samej formie prawnej i sposobie rozliczeń.</li>
        <li><b>Ciągłość obsługi.</b> Zespół jest na tyle duży, że sezon urlopowy czy nieobecność jednej osoby nie wstrzymuje pracy nad Twoimi sprawami.</li>
      </ul>
    </div>
    <figure class="foto"><img src="{{R}}assets/img/notatnik-1000.webp" srcset="{{R}}assets/img/notatnik-640.webp 640w, {{R}}assets/img/notatnik-1000.webp 1000w" sizes="(max-width: 960px) 100vw, 560px" alt="Laptop, notatnik i okulary na biurku" width="1000" height="667" loading="lazy"></figure>
  </div>
</section>

<section class="szare" id="jak-zaczac">
  <div class="wrap dwie dwie-gora">
    <div>
      <h2>Jak zacząć współpracę</h2>
      <p class="lead2">Najprościej zadzwonić do recepcji pod numer <a href="tel:{TEL_H}">{TEL}</a> albo napisać przez <a href="{{R}}kontakt/#formularz">formularz</a>.</p>
      <p class="odst">Zapytamy o formę działalności, sposób opodatkowania, przybliżoną liczbę dokumentów w miesiącu i to, czy zatrudniasz pracowników. Na tej podstawie przygotujemy bezpłatną wycenę. Jeśli ją zaakceptujesz, podpisujemy umowę i ustalamy, od którego miesiąca przejmujemy księgowość oraz w jaki sposób będziesz przekazywać dokumenty.</p>
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
    <div class="faq"><details><summary>Ile kosztuje prowadzenie księgowości?</summary><p>Cenę ustalamy indywidualnie. Zależy od formy działalności i opodatkowania, liczby dokumentów w miesiącu i liczby pracowników. Wycena jest bezpłatna - wystarczy telefon do recepcji albo wiadomość przez formularz.</p></details><details><summary>Czy muszę przychodzić do biura z dokumentami?</summary><p>Nie. Faktury i inne dokumenty możesz przesyłać elektronicznie. Jeśli wolisz, możesz je też zostawić w recepcji przy ul. Rybackiej 3.</p></details><details><summary>Czy przypomnicie mi o podatku i ZUS?</summary><p>Tak. Co miesiąc dostajesz informację o wysokości i terminie zapłaty podatków oraz składek ZUS.</p></details><details><summary>Czy mogę wglądać w swoje dokumenty?</summary><p>Tak. Zaksięgowane dokumenty archiwizujemy i w każdej chwili możesz je przejrzeć oraz skopiować w recepcji biura.</p></details><details><summary>Czy prowadzicie kadry i płace?</summary><p>Tak, mamy osobny dział kadr: tel. 56 691 20 85, kadry@buchalter.home.pl. Przygotowujemy umowy, listy płac, rozliczenia ZUS i deklaracje PIT-11.</p></details><details><summary>Czy pomagacie osobom, które nie prowadzą firmy?</summary><p>Tak. Wśród naszych klientów są osoby nieprowadzące działalności gospodarczej - rozliczamy ich podatki.</p></details><details><summary>Czy pomożecie założyć firmę albo spółkę?</summary><p>Tak. Pomagamy wybrać formę działalności i opodatkowania oraz załatwiamy formalności, także rejestrację spółki w KRS.</p></details></div>
  </div>
</section>'''
strony.append(strona("jak-pracujemy/", "Jak pracujemy i jak zacząć współpracę | Buchalter Chełmno",
                     "Jak pracuje Biuro Rachunkowe Buchalter w Chełmnie: dokumenty elektronicznie lub w recepcji, terminy podatków i ZUS, działy według rodzaju klientów. Jak zacząć współpracę.",
                     jp, akt="jak-pracujemy/", okruszki=[("Jak pracujemy", "jak-pracujemy/")], schema_extra=FAQ_LD))

# ---------------------------------------------------------------- O BIURZE
ob = glowa("O biurze",
           "Biuro Rachunkowe Buchalter działa w Chełmnie od 1999 roku. Obsługujemy firmy, organizacje i osoby prywatne z Chełmna i okolic.",
           [("O biurze", "o-biurze/")]) + '''
<section>
  <div class="wrap dwie dwie-gora">
    <div class="tresc">
      <h2>Biuro podzielone na działy</h2>
      <p>Potrzebujesz pewności, że księgowość Twojej firmy jest prowadzona prawidłowo. Dlatego biuro jest podzielone na działy, z których każdy specjalizuje się w obsłudze klientów określonego typu: z podobnych branż, o tej samej formie prawnej i sposobie rozliczeń.</p>
      <p>Nasi księgowi mają kierunkowe wykształcenie i stale poszerzają wiedzę na szkoleniach i kursach. Na co dzień prowadzą różnorodne i złożone sprawy księgowe oraz kadrowe.</p>
      <p>Obsługujemy jednoosobowe działalności, spółki, spółki-córki dużych firm, fundacje i stowarzyszenia, a także osoby prywatne.</p>
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
  <p class="cena">{cena}<small>wycena bezpłatna</small></p>
  <a class="btn-out" href="{{R}}kontakt/?temat={temat}#formularz">Zapytaj o wycenę</a>
</article>'''

wsp = ["Informacja o wysokości i terminie podatków oraz składek ZUS", "Konsultacje w sprawie bieżącej sytuacji firmy"]
cn = glowa("Cennik usług księgowych",
           "Zobacz, co wchodzi w skład naszych pakietów. Cenę ustalamy indywidualnie, bo zależy od wielkości i rodzaju firmy - wycena jest bezpłatna.",
           [("Cennik", "cennik/")]) + f'''
<section>
  <div class="wrap">
    <div class="pakiety">
      {pakiet("Księgi podatkowe", ["Ewidencja dokumentów księgowych"] + wsp, "Cena ustalana indywidualnie", "Księgi podatkowe")}
      {pakiet("Ryczałt", ["Prowadzenie ewidencji ryczałtowych"] + wsp, "Cena ustalana indywidualnie", "Ryczałt")}
      {pakiet("Księgi handlowe", ["Ewidencja dokumentów księgowych"] + wsp, "Cena ustalana indywidualnie", "Księgi handlowe")}
      {pakiet("Kadry i płace", ["Sporządzanie list płac pracowników", "Naliczanie wynagrodzeń", "Prowadzenie akt pracowniczych", "Sporządzanie deklaracji PIT-11"], "Cena za osobę, ustalana indywidualnie", "Kadry i płace")}
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
                     "Cennik pakietów Biura Rachunkowego Buchalter w Chełmnie: księgi podatkowe, ryczałt, księgi handlowe, kadry i płace. Bezpłatna wycena: tel. 56 691 20 80.",
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
      <div class="mapa" id="mapa">
        <div class="mapa-zaslona">
          <p><b>ul. Rybacka 3, Chełmno</b>Mapa Google wczyta się dopiero po kliknięciu, razem z plikami cookie Google.</p>
          <button class="btn-out" type="button" id="mapaPokaz">Pokaż mapę</button>
        </div>
      </div>
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
      <h2>Pliki cookie i usługi zewnętrzne</h2>
      <p>Strona nie używa plików cookie do statystyk ani reklam i nie śledzi odwiedzających. Czcionki są wczytywane z naszego serwera. Mapa Google na stronie kontaktowej wczytuje się dopiero po kliknięciu przycisku "Pokaż mapę" - wtedy Google może zapisać swoje pliki cookie zgodnie z <a href="https://policies.google.com/privacy?hl=pl" rel="noopener" target="_blank">polityką prywatności Google</a>. Link do profilu na Facebooku prowadzi do serwisu Meta, który stosuje własne zasady.</p>
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
    <p style="margin-top:24px;display:flex;gap:16px 28px;flex-wrap:wrap"><a class="btn" href="https://disaster26.github.io/buchalter-koncepcja/">Strona główna</a><a class="link-strz" href="https://disaster26.github.io/buchalter-koncepcja/oferta/">Oferta</a><a class="link-strz" href="https://disaster26.github.io/buchalter-koncepcja/cennik/">Cennik</a><a class="link-strz" href="https://disaster26.github.io/buchalter-koncepcja/kontakt/">Kontakt</a></p>
  </div>
</section>'''
strona("404.html", "Nie ma takiej strony | Buchalter", "Strona nie istnieje.", e404)

# ---------------------------------------------------------------- sitemap / robots
sm = "".join(f"<url><loc>{PROD}{p}</loc><lastmod>{DZIS}</lastmod></url>" for p in strony)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text("# Wersja testowa - nie indeksować\nUser-agent: *\nDisallow: /\n" if TEST else f"User-agent: *\nAllow: /\nSitemap: {PROD}sitemap.xml\n", encoding="utf-8")
(Path(__file__).parent / "robots_produkcja.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PROD}sitemap.xml\n", encoding="utf-8")
print("OK", len(strony) + 1, "stron:", ", ".join(p or "/" for p in strony))
