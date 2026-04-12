import re

with open('templates/index.html', 'r') as f:
    idx = f.read()

print('Before - tip-hero:', idx.count('tip-hero-jar'), '| credits:', idx.count('credits-section'))

# Remove ALL tip-hero duplicates
idx = re.sub(r'    <a class="tip-hero".*?</a>\n', '', idx, flags=re.DOTALL)

# Add back exactly ONE tip jar after hero CTA
tip = '    <a class="tip-hero" href="#" onclick="openTip(event)">\n      <span class="tip-hero-jar">🫙</span>\n      <span class="tip-coin"></span><span class="tip-coin"></span><span class="tip-coin"></span>\n      <span class="tip-hero-txt">Leave a Tip</span>\n    </a>\n'
idx = idx.replace('    </div>\n</section>\n\n<section class="about"', tip + '    </div>\n</section>\n\n<section class="about"', 1)

# Remove ALL credits-section duplicates
idx = re.sub(r'\n<!-- Credits -->.*?</section>\n', '', idx, flags=re.DOTALL)

# Add back exactly ONE credits section before services
credits = '\n<!-- Credits -->\n<section class="credits-section" data-reveal>\n  <div class="sec-hdr"><div class="sec-lbl">Credits</div></div>\n  {% if credits %}\n    <div class="credits-grid">\n      {% for c in credits %}\n      <div class="credit-card">\n        <div class="credit-artist">{{ c.artist }}</div>\n        <div class="credit-role">{{ c.role }}</div>\n        {% if c.track_name %}<div class="credit-track">{{ c.track_name }}</div>{% endif %}\n        {% if c.year %}<div class="credit-year">{{ c.year }}</div>{% endif %}\n      </div>\n      {% endfor %}\n    </div>\n  {% else %}\n    <div class="credits-empty">Credits will appear here — add them via the admin panel.</div>\n  {% endif %}\n</section>\n'
idx = idx.replace('\n<section class="section" data-reveal>\n  <div class="sec-hdr"><div class="sec-lbl">Services</div>', credits + '\n<section class="section" data-reveal>\n  <div class="sec-hdr"><div class="sec-lbl">Services</div>', 1)

# Remove placeholder beats
idx = re.sub(r'    \{% else %\}\n      <!-- Placeholder rows.*?\{% endif %\}', '    {% else %}\n      <div style="padding:20px 18px;font-family:Space Mono,monospace;font-size:9px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase">New beats dropping soon</div>\n    {% endif %}', idx, flags=re.DOTALL)

with open('templates/index.html', 'w') as f:
    f.write(idx)

print('After  - tip-hero:', idx.count('tip-hero-jar'), '| credits:', idx.count('credits-section'))
print('Midnight Cipher:', idx.count('Midnight Cipher'))
print('DONE')
