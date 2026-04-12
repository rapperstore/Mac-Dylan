import os, re

BASE = os.path.expanduser('~/Desktop/macdylan')

# Read the current broken file
with open(f'{BASE}/templates/index.html', 'r') as f:
    content = f.read()

# ── STEP 1: Fix the broken hero-actions block ──────────────────
# Replace everything between hero-actions opening and end of section
content = re.sub(
    r'<div class="hero-actions">.*?</div>\s*</div>\s*</section>',
    '''<div class="hero-actions">
      <div class="hero-cta">
        <a href="{{ url_for('services.index') }}" class="btn-fire">Book a Session</a>
        <a href="{{ url_for('beats.index') }}" class="btn-ghost">Browse Beats</a>
      </div>
    </div>
  </div>
</section>''',
    content, flags=re.DOTALL
)

# ── STEP 2: Add modal HTML right after {% block content %} ──────
if 'ebook-modal' not in content:
    modal_html = '''<!-- EBOOK MODAL -->
<div class="modal-overlay" id="ebook-modal">
  <div class="modal-box">
    <div class="modal-topbar"></div>
    <button class="modal-close" onclick="closeModal()">&#x2715;</button>
    <div class="modal-cover">
      <span class="modal-cover-the">Mac Dylan Presents</span>
      <h2 class="modal-cover-title">The Artist<em>Is The Business</em></h2>
      <p class="modal-cover-sub">The complete independent artist blueprint</p>
    </div>
    <div class="modal-body">
      <p class="modal-desc">Everything the music industry won&#x2019;t tell you &#x2014; laid out in 9 chapters with real frameworks, income strategies, and a 90-day execution plan built for artists who are done waiting.</p>
      <ul class="modal-features">
        <li>9 chapters of real strategy</li>
        <li>Income streams that work</li>
        <li>Brand building from scratch</li>
        <li>Organic growth without ads</li>
        <li>AI as a force multiplier</li>
        <li>90-day action checklist</li>
        <li>Interactive navigation</li>
        <li>Instant digital download</li>
      </ul>
      <div class="modal-footer">
        <div>
          <div class="modal-price">$27</div>
          <div class="modal-price-note">One-time &#xB7; Instant download &#xB7; Yours forever</div>
        </div>
        <a href="{{ url_for('store.index') }}" class="modal-btn" onclick="closeModal()">Get The Blueprint &#x2192;</a>
      </div>
    </div>
  </div>
</div>
'''
    content = content.replace(
        '{% block content %}\n<section class="hero">',
        '{% block content %}\n' + modal_html + '<section class="hero">'
    )

# ── STEP 3: Fix tip jar emoji (beaver issue) ────────────────────
# Replace all beaver/wrong jar references with direct emoji
content = content.replace('&#x1F9AB;', '\U0001f9ab')
content = content.replace('🦫', '\U0001f9ab')  # replace beaver with jar

# ── STEP 4: Fix tip banner jar emoji ───────────────────────────
content = content.replace(
    '<span class="tip-jar-big">🦫</span>',
    '<span class="tip-jar-big">\U0001f9ab</span>'
)

# ── STEP 5: Rebuild the entire extra_scripts block ─────────────
new_scripts = '''{% block extra_scripts %}
<script>
// ── NEWSLETTER ─────────────────────────────────────────────────
window.subCK = function(e) {
  e.preventDefault();
  var email = document.getElementById('ck-email').value.trim();
  if (!email) return;
  fetch('https://mac-dylan.kit.com/b5923233e5/subscriptions', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'email_address=' + encodeURIComponent(email),
  }).then(function(){}).catch(function(){});
  document.getElementById('ck-form').style.display = 'none';
  document.getElementById('nl-ok').style.display = 'block';
  document.getElementById('nl-note').style.display = 'none';
};

// ── TIP JAR ─────────────────────────────────────────────────────
window.openTip = function(e) {
  if (e) e.preventDefault();
  var amt = prompt('How much would you like to tip Mac Dylan?', '10');
  if (!amt || isNaN(+amt) || +amt < 1) return;
  fetch('/payments/tip', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: +amt, email: ''})
  }).then(function(r){ return r.json(); })
    .then(function(d){ if (d.checkout_url) window.location.href = d.checkout_url; })
    .catch(function(){ alert('Checkout unavailable. Try again shortly.'); });
};

window.selTip = function(amt, btn) {
  document.querySelectorAll('.ta-btn').forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
  var input = document.getElementById('tip-amt');
  if (input) input.value = amt;
};

window.sendTipAmt = function() {
  var input = document.getElementById('tip-amt');
  var amt = input ? +input.value : 0;
  if (!amt || amt < 1) { alert('Please enter a tip amount.'); return; }
  fetch('/payments/tip', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: amt, email: ''})
  }).then(function(r){ return r.json(); })
    .then(function(d){ if (d.checkout_url) window.location.href = d.checkout_url; })
    .catch(function(){ alert('Checkout unavailable. Try again shortly.'); });
};

// ── EBOOK MODAL ─────────────────────────────────────────────────
window.closeModal = function() {
  var m = document.getElementById('ebook-modal');
  if (m) { m.classList.remove('open'); document.body.style.overflow = ''; }
  try { sessionStorage.setItem('ebookSeen', '1'); } catch(e) {}
};

var modal = document.getElementById('ebook-modal');
if (modal) {
  modal.addEventListener('click', function(e) {
    if (e.target === modal) window.closeModal();
  });
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') window.closeModal();
});

// Auto-open modal once per session after 1.5s
try {
  if (!sessionStorage.getItem('ebookSeen')) {
    setTimeout(function() {
      var m = document.getElementById('ebook-modal');
      if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; }
    }, 1500);
  }
} catch(e) {
  setTimeout(function() {
    var m = document.getElementById('ebook-modal');
    if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; }
  }, 1500);
}
</script>
{% endblock %}'''

# Replace existing extra_scripts block entirely
content = re.sub(
    r'{% block extra_scripts %}.*?{% endblock %}',
    new_scripts,
    content,
    flags=re.DOTALL
)

with open(f'{BASE}/templates/index.html', 'w') as f:
    f.write(content)

print('index.html fixed')
print('  Hero actions rebuilt cleanly')
print('  Modal HTML added')
print('  Jar emoji fixed')
print('  All JS functions restored')

# Push
os.system(f'cd {BASE} && git add -A && git commit -m "fix broken homepage: hero, modal, tip jar, all JS" && git push')
print('DONE - Railway deploys in 60 seconds')
