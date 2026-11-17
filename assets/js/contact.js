// Contact form: opens WhatsApp with the message pre-filled. Nothing is stored or sent by the site.
(function () {
  var WHATSAPP = '34654691336';
  var form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var fields = form.elements;
    var name = fields['contact-name'].value.trim();
    var phone = fields['contact-phone'].value.trim();
    var course = fields['contact-class'].value;
    var note = fields['contact-message'].value.trim();
    var text = '¡Hola! Soy ' + (name || '[nombre]') + '. Me interesa ' + course + '.';
    if (note) text += ' ' + note;
    if (phone) text += ' Mi teléfono: ' + phone + '.';
    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
  });
})();
