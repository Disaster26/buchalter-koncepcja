(function () {
  'use strict';
  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');
  function zamknij() {
    menu.classList.remove('otwarte');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Otwórz menu');
  }
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var o = menu.classList.toggle('otwarte');
      burger.setAttribute('aria-expanded', o ? 'true' : 'false');
      burger.setAttribute('aria-label', o ? 'Zamknij menu' : 'Otwórz menu');
    });
    menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') zamknij(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('otwarte')) { zamknij(); burger.focus(); } });
  }

  // dolny pasek na telefonie: na stronie głównej po przewinięciu za przyciski hero, na podstronach po nagłówku
  var mob = document.getElementById('mob');
  var cel = document.getElementById('heroCta') || document.querySelector('.glowa-strony');
  if (mob && cel && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (w) {
      var pokaz = !w[0].isIntersecting && w[0].boundingClientRect.top < 0;
      mob.classList.toggle('widac', pokaz);
      mob.setAttribute('aria-hidden', pokaz ? 'false' : 'true');
      mob.querySelectorAll('a').forEach(function (a) { a.tabIndex = pokaz ? 0 : -1; });
    }).observe(cel);
  }

  // mapa Google dopiero po kliknięciu
  var mb = document.getElementById('mapaPokaz');
  if (mb) {
    mb.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.title = 'Mapa: ul. Rybacka 3, Chełmno';
      f.src = 'https://maps.google.com/maps?q=Rybacka%203%2C%2086-200%20Che%C5%82mno&z=16&output=embed';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      var m = document.getElementById('mapa');
      m.innerHTML = '';
      m.appendChild(f);
    });
  }

  // formularz (wersja testowa - makieta, nic nie wysyła)
  var form = document.getElementById('formularz');
  if (form) {
    var t = new URLSearchParams(location.search).get('temat');
    if (t) {
      for (var i = 0; i < form.temat.options.length; i++) {
        if (form.temat.options[i].text === t) { form.temat.selectedIndex = i; break; }
      }
    }
    var wynik = document.getElementById('formWynik');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, pierwsze = null;
      [form.kontakt, form.wiadomosc].forEach(function (p) {
        var pusty = !p.value.trim();
        p.classList.toggle('pole-blad', pusty);
        p.setAttribute('aria-invalid', pusty ? 'true' : 'false');
        if (pusty) { ok = false; pierwsze = pierwsze || p; }
      });
      wynik.hidden = false;
      if (!ok) {
        wynik.className = 'wynik blad';
        wynik.textContent = 'Uzupełnij kontakt zwrotny (e-mail lub telefon) i treść wiadomości.';
        pierwsze.focus();
        return;
      }
      if (form.www.value) return; // pułapka na boty
      wynik.className = 'wynik';
      wynik.textContent = 'Dziękujemy. W wersji testowej formularz niczego nie wysyła - po uruchomieniu strony wiadomość trafi do recepcji biura.';
      form.reset();
    });
  }
})();
