(function () {
  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');
  function zamknij() { menu.classList.remove('otwarte'); burger.setAttribute('aria-expanded', 'false'); burger.setAttribute('aria-label', 'Otwórz menu'); }
  burger.addEventListener('click', function () {
    var o = menu.classList.toggle('otwarte');
    burger.setAttribute('aria-expanded', o ? 'true' : 'false');
    burger.setAttribute('aria-label', o ? 'Zamknij menu' : 'Otwórz menu');
  });
  menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') zamknij(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') zamknij(); });

  // dolny pasek na telefonie dopiero po przewinieciu za przyciski hero
  var mob = document.getElementById('mob');
  var cta = document.getElementById('heroCta');
  if ('IntersectionObserver' in window && mob && cta) {
    new IntersectionObserver(function (w) {
      var pokaz = !w[0].isIntersecting && w[0].boundingClientRect.top < 0;
      mob.classList.toggle('widac', pokaz);
      mob.setAttribute('aria-hidden', pokaz ? 'false' : 'true');
      mob.querySelectorAll('a').forEach(function (a) { a.tabIndex = pokaz ? 0 : -1; });
    }).observe(cta);
  }

  // pakiet z cennika -> temat w formularzu
  var form = document.getElementById('form');
  document.querySelectorAll('[data-pakiet]').forEach(function (a) {
    a.addEventListener('click', function () { form.temat.value = a.getAttribute('data-pakiet'); });
  });

  // formularz otwiera program pocztowy
  var info = document.getElementById('formInfo');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var k = form.kontakt, w = form.wiadomosc, ok = true;
    [k, w].forEach(function (p) { var pusty = !p.value.trim(); p.classList.toggle('pole-blad', pusty); if (pusty) ok = false; });
    if (!ok) { info.textContent = 'Uzupełnij kontakt zwrotny i treść wiadomości.'; info.classList.add('blad'); return; }
    info.classList.remove('blad');
    info.textContent = 'Otwieramy program pocztowy z gotową wiadomością.';
    var tresc = w.value.trim() + '\n\n' + (form.imie.value.trim() ? form.imie.value.trim() + '\n' : '') + 'Kontakt: ' + k.value.trim();
    location.href = 'mailto:recepcja@buchalter.home.pl?subject=' + encodeURIComponent(form.temat.value + ' - zapytanie ze strony') + '&body=' + encodeURIComponent(tresc);
  });
})();
