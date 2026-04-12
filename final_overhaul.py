import os, re, shutil

BASE = os.path.expanduser('~/Desktop/macdylan')
print("=" * 60)
print("MAC DYLAN SITE — FINAL OVERHAUL")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# 1. BASE.HTML — global link reset so no blue links ever
# ══════════════════════════════════════════════════════════════
with open(f'{BASE}/templates/base.html', 'r') as f:
    base = f.read()

if 'a{color:inherit' not in base:
    base = base.replace(
        'body{background:var(--black)',
        'a{color:inherit;text-decoration:none}\nbutton{cursor:pointer}\nbody{background:var(--black)'
    )
    with open(f'{BASE}/templates/base.html', 'w') as f:
        f.write(base)
    print('[1/5] base.html — global link reset added')
else:
    print('[1/5] base.html — already has link reset')

# ══════════════════════════════════════════════════════════════
# 2. INDEX.HTML — full rebuild
# ══════════════════════════════════════════════════════════════
with open(f'{BASE}/templates/index.html', 'r') as f:
    idx = f.read()

new_styles = """{% block extra_styles %}
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 88px;position:relative}
.hero-eyebrow{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:20px;opacity:0;animation:burnIn 1s ease forwards .4s}
.hero-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(80px,16vw,210px);line-height:.84;letter-spacing:.01em;opacity:0;animation:burnIn 1s ease forwards .7s}
.hero-title .outline{color:var(--fire);display:block;text-shadow:0 0 60px rgba(200,75,10,.35)}
.hero-desc{font-size:clamp(15px,2vw,21px);font-style:italic;color:var(--ash);margin-top:24px;max-width:520px;line-height:1.7;opacity:0;animation:burnIn 1s ease forwards 1s}
.hero-actions{margin-top:44px;opacity:0;animation:burnIn 1s ease forwards 1.3s}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.btn-fire{display:inline-block;padding:15px 36px;background:var(--ember);color:#f5f0e8;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.3em;text-transform:uppercase;text-decoration:none;border:none;transition:background .25s,box-shadow .25s}
.btn-fire:hover{background:var(--fire);box-shadow:0 0 36px rgba(200,75,10,.55);color:#f5f0e8}
.btn-ghost{display:inline-block;padding:14px 36px;background:transparent;color:#b8a898;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.3em;text-transform:uppercase;text-decoration:none;border:1px solid rgba(200,75,10,.25);transition:all .25s}
.btn-ghost:hover{border-color:var(--ember);color:var(--fire)}
.hero-sub-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:28px}
.hero-sep{width:1px;height:16px;background:rgba(200,75,10,.2);display:inline-block;flex-shrink:0}
.tip-jar{display:inline-flex;align-items:center;gap:8px;padding:9px 18px;background:rgba(200,75,10,.07);border:1px solid rgba(200,75,10,.22);color:#c84b0a;font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.28em;text-transform:uppercase;text-decoration:none;transition:all .22s}
.tip-jar:hover{background:rgba(200,75,10,.14);border-color:var(--ember);box-shadow:0 0 14px rgba(200,75,10,.2);color:#c84b0a}
.tip-jar-icon{font-size:15px;line-height:1;animation:tjf 3s ease-in-out infinite;display:inline-block}
.tip-coin{width:5px;height:5px;border-radius:50%;background:var(--flame);opacity:0;display:inline-block;animation:tjc 2.2s ease-in-out infinite}
.tip-coin:nth-child(2){animation-delay:.35s}.tip-coin:nth-child(3){animation-delay:.7s}
.btn-secondary{display:inline-block;padding:9px 18px;background:transparent;color:#6b5a4a;font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.2em;text-transform:uppercase;text-decoration:none;border:1px solid rgba(200,75,10,.14);transition:all .22s}
.btn-secondary:hover{border-color:rgba(200,75,10,.35);color:#b8a898}
.hero-stats{display:flex;align-items:center;gap:20px;padding-top:20px;border-top:1px solid rgba(200,75,10,.1);flex-wrap:wrap}
.hero-stat-n{font-family:'Bebas Neue',sans-serif;font-size:26px;color:#e8720c;line-height:1}
.hero-stat-l{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.2em;color:#6b5a4a;text-transform:uppercase;margin-top:2px}
.hero-stat-sep{width:1px;height:26px;background:rgba(200,75,10,.14);flex-shrink:0}
@keyframes tjf{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes tjc{0%{opacity:0;transform:translateY(0) scale(0)}20%{opacity:1;transform:translateY(-6px) scale(1)}100%{opacity:0;transform:translateY(-18px) scale(.4)}}
.about{padding:120px 48px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;border-top:1px solid var(--border)}
.about-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:18px}
.about-heading{font-family:'Bebas Neue',sans-serif;font-size:clamp(40px,6vw,72px);line-height:.95;margin-bottom:20px}.about-heading em{color:var(--fire);font-style:normal}
.about-text{font-size:17px;line-height:1.8;color:var(--ash);font-style:italic;margin-bottom:20px}
.about-contact{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--muted)}.about-contact a{color:var(--ember)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--border);border:1px solid var(--border)}
.stat{background:var(--card);padding:30px 22px;transition:background .2s}.stat:hover{background:var(--card2)}
.stat-num{font-family:'Bebas Neue',sans-serif;font-size:48px;color:var(--fire);line-height:1;margin-bottom:4px}
.stat-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--muted);text-transform:uppercase}
.section{padding:0 48px 100px}
.sec-hdr{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:32px}
.sec-lbl{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase}
.sec-link{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--muted);text-transform:uppercase;text-decoration:none;transition:color .2s}.sec-link:hover{color:var(--fire)}
.mini-playlist{background:var(--card);border:1px solid var(--border)}
.mini-row{display:flex;align-items:center;padding:12px 18px;border-bottom:1px solid var(--border);gap:12px;text-decoration:none;transition:background .2s;position:relative;overflow:hidden}
.mini-row:last-child{border-bottom:none}.mini-row:hover{background:var(--card2)}
.mini-row::before{content:'';position:absolute;left:0;top:0;bottom:0;width:0;background:var(--ember);transition:width .3s}.mini-row:hover::before{width:2px}
.mini-num{font-family:'Space Mono',monospace;font-size:9px;color:var(--muted);width:18px;flex-shrink:0}
.mini-ph{width:30px;height:30px;background:linear-gradient(135deg,#0d0a07,#1e1208);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:13px;color:rgba(200,75,10,.25);flex-shrink:0}
.mini-info{flex:1;min-width:0}
.mini-title{font-family:'Bebas Neue',sans-serif;font-size:15px;color:var(--white);letter-spacing:.04em;line-height:1}
.mini-meta{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase;margin-top:2px}
.mini-price{font-family:'Bebas Neue',sans-serif;font-size:17px;flex-shrink:0}
.mini-price.fire{color:var(--fire)}.mini-price.green{color:var(--green)}
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--border);border:1px solid var(--border)}
.svc-card{background:var(--card);padding:34px 26px;text-decoration:none;display:block;position:relative;overflow:hidden;transition:background .3s;color:inherit}
.svc-card:hover{background:var(--card2)}
.svc-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--ember),var(--flame));transform:scaleX(0);transform-origin:left;transition:transform .4s}.svc-card:hover::before{transform:scaleX(1)}
.svc-num{font-family:'Bebas Neue',sans-serif;font-size:48px;color:var(--border);line-height:1;margin-bottom:12px}
.svc-name{font-family:'Bebas Neue',sans-serif;font-size:21px;color:var(--white);letter-spacing:.04em;margin-bottom:8px;line-height:1}
.svc-desc{font-size:13px;color:var(--muted);font-style:italic;line-height:1.6;margin-bottom:16px}
.svc-price{font-family:'Bebas Neue',sans-serif;font-size:24px;color:var(--fire)}
.svc-price small{font-size:11px;color:var(--muted);font-family:'Space Mono',monospace;margin-left:4px}
.social-section{padding:0 48px 56px}
.social-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:20px;display:flex;align-items:center;gap:12px}
.social-label::after{content:'';flex:1;height:1px;background:var(--border)}
.social-circles{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.sb-btn{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid rgba(200,75,10,.4);background:rgba(200,75,10,.06);transition:all .2s;color:var(--ember);text-decoration:none;flex-shrink:0}
.sb-btn svg{width:12px;height:12px;fill:currentColor;transition:fill .2s}
.sb-btn:hover{background:var(--ember);border-color:var(--fire);box-shadow:0 0 12px rgba(200,75,10,.4)}
.sb-btn:hover svg{fill:#f5f0e8}
.newsletter{padding:80px 48px;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.nl-heading{font-family:'Bebas Neue',sans-serif;font-size:clamp(36px,5vw,62px);line-height:.95;margin-bottom:12px}.nl-heading em{color:var(--fire);font-style:normal}
.nl-sub{font-size:15px;color:var(--ash);font-style:italic;line-height:1.7}
.nl-form-wrap{display:flex;gap:2px}
.nl-input{flex:1;padding:14px 16px;background:var(--card);border:1px solid var(--border);color:var(--white);font-family:'Cormorant Garamond',serif;font-size:16px;transition:border-color .2s}
.nl-input:focus{outline:none;border-color:var(--ember)}.nl-input::placeholder{color:var(--muted);font-style:italic}
.nl-btn{padding:14px 24px;background:var(--ember);border:none;color:var(--white);font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.28em;text-transform:uppercase;transition:background .2s;white-space:nowrap}.nl-btn:hover{background:var(--fire)}
.nl-note{font-family:'Space Mono',monospace;font-size:8px;color:var(--muted);letter-spacing:.14em;margin-top:8px}
.nl-ok{display:none;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--fire);text-transform:uppercase;padding:12px 0}
.quote{padding:90px 48px;border-top:1px solid var(--border);border-bottom:1px solid var(--border);text-align:center;position:relative;overflow:hidden}
.quote::before{content:'"';position:absolute;top:-80px;left:50%;transform:translateX(-50%);font-family:'Bebas Neue',sans-serif;font-size:380px;color:rgba(200,75,10,.03);pointer-events:none;line-height:1}
.quote-text{font-family:'Cormorant Garamond',serif;font-size:clamp(20px,4vw,40px);font-style:italic;font-weight:300;color:var(--white);max-width:780px;margin:0 auto 18px;line-height:1.4;position:relative}.quote-text em{color:var(--fire);font-style:normal}
.quote-attr{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.4em;color:var(--muted);text-transform:uppercase}
@media(max-width:900px){.hero{padding:0 24px 64px}.about{grid-template-columns:1fr;padding:80px 24px;gap:44px}.section,.social-section{padding-left:24px;padding-right:24px}.svc-grid{grid-template-columns:1fr}.newsletter{grid-template-columns:1fr;padding:56px 24px;gap:28px}.nl-form-wrap{flex-direction:column}.quote{padding:68px 24px}.hero-stats{gap:12px}.hero-stat-n{font-size:20px}}
{% endblock %}"""

idx = re.sub(r'{% block extra_styles %}.*?{% endblock %}', new_styles, idx, flags=re.DOTALL)

new_hero = """{% block content %}
<section class="hero">
  <div>
    <div class="hero-eyebrow">Boise, Idaho · Mix · Record · Develop</div>
    <h1 class="hero-title">Mac<span class="outline">Dylan</span></h1>
    <p class="hero-desc">Where independent artists come to sound like they mean it. Mix engineering, production, and artist development from someone who built from nothing.</p>
    <div class="hero-actions">
      <div class="hero-cta">
        <a href="{{ url_for('services.index') }}" class="btn-fire">Book a Session</a>
        <a href="{{ url_for('beats.index') }}" class="btn-ghost">Browse Beats</a>
      </div>
      <div class="hero-sub-row">
        <a class="tip-jar" href="#" onclick="openTip(event)">
          <span class="tip-jar-icon">&#x1F9AB;</span>
          <span class="tip-coin"></span><span class="tip-coin"></span><span class="tip-coin"></span>
          Leave a Tip
        </a>
        <span class="hero-sep"></span>
        <a href="{{ url_for('store.index') }}" class="btn-secondary">The Blueprint $27 &#x2192;</a>
      </div>
      <div class="hero-stats">
        <div><div class="hero-stat-n">10+</div><div class="hero-stat-l">Years</div></div>
        <span class="hero-stat-sep"></span>
        <div><div class="hero-stat-n">500+</div><div class="hero-stat-l">Records Mixed</div></div>
        <span class="hero-stat-sep"></span>
        <div><div class="hero-stat-n">100%</div><div class="hero-stat-l">Independent</div></div>
        <span class="hero-stat-sep"></span>
        <div><div class="hero-stat-n">&#x221E;</div><div class="hero-stat-l">Artist First</div></div>
      </div>
    </div>
  </div>
</section>"""

idx = re.sub(r'{% block content %}.*?</section>', new_hero, idx, count=1, flags=re.DOTALL)

# Fix quote — remove phone number
idx = idx.replace(
    '<div class="quote-attr">Mac Dylan · (208) 391-5292 · Boise, Idaho</div>',
    '<div class="quote-attr">Mac Dylan · Boise, Idaho</div>'
)

# Fix newsletter URL
idx = idx.replace(
    "fetch('https://app.convertkit.com/forms/9292507/subscriptions'",
    "fetch('https://mac-dylan.kit.com/b5923233e5/subscriptions'"
)

# Remove placeholder beats
idx = re.sub(
    r'\s*{% else %}\s*<!\-\- Placeholder.*?{% endif %}',
    "\n    {% else %}\n      <div style=\"padding:20px 18px;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase\">New beats dropping soon</div>\n    {% endif %}",
    idx, flags=re.DOTALL
)

with open(f'{BASE}/templates/index.html', 'w') as f:
    f.write(idx)
print('[2/5] index.html — hero rebuilt, tip jar, stats, newsletter fixed')

# ══════════════════════════════════════════════════════════════
# 3. ADMIN — add HTML to allowed product file types + list API
# ══════════════════════════════════════════════════════════════
with open(f'{BASE}/routes/admin.py', 'r') as f:
    admin = f.read()

admin = admin.replace(
    "file_path     = save_file('file', 'products', {'zip', 'pdf', 'mp3', 'wav'}),",
    "file_path     = save_file('file', 'products', {'zip', 'pdf', 'mp3', 'wav', 'html'}),",
)

if '/products/list' not in admin:
    admin = admin.replace(
        "# ─── CONTENT ──────────────────────────────────────────────",
        """@admin_bp.route('/products/list')
@admin_required
def list_products():
    prods = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'price': p.price,
        'product_type': p.product_type, 'is_active': p.is_active,
        'is_new': p.is_new, 'tags': p.tags or '',
        'file_path': p.file_path or ''
    } for p in prods])


# ─── CONTENT ──────────────────────────────────────────────"""
    )

with open(f'{BASE}/routes/admin.py', 'w') as f:
    f.write(admin)
print('[3/5] admin.py — products list route + HTML file support added')

# ══════════════════════════════════════════════════════════════
# 4. SEED EBOOK INTO DATABASE
# ══════════════════════════════════════════════════════════════
products_dir = f'{BASE}/static/uploads/products'
os.makedirs(products_dir, exist_ok=True)

# Copy ebook from uploads if available
ebook_sources = [
    '/mnt/user-data/uploads/artist-is-the-business-v2.html',
    os.path.expanduser('~/Downloads/artist-is-the-business-v2.html'),
    os.path.expanduser('~/Desktop/artist-is-the-business-v2.html'),
]
copied = False
for src in ebook_sources:
    if os.path.exists(src):
        shutil.copy2(src, f'{products_dir}/artist-is-the-business-v2.html')
        print(f'[4/5] Ebook copied from {src}')
        copied = True
        break
if not copied:
    print('[4/5] NOTE: ebook HTML not found — add manually via Admin > Products')

seed = '''import sys
sys.path.insert(0, '.')
from app import create_app
from database import db
from models import Product
app = create_app()
with app.app_context():
    db.create_all()
    e = Product.query.filter_by(name="The Artist Is The Business").first()
    if e:
        e.price=27; e.is_active=True; e.is_new=True
        e.product_type="digital"
        e.file_path="uploads/products/artist-is-the-business-v2.html"
        e.description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan. Interactive e-book with animated visuals and built-in action checklist."
        e.tags="ebook,artist development,branding,income,strategy"
        db.session.commit(); print("Updated — ID:", e.id)
    else:
        p=Product(product_type="digital",
            name="The Artist Is The Business",
            description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan. Interactive e-book with animated visuals and built-in action checklist.",
            price=27, tags="ebook,artist development,branding,income,strategy",
            file_path="uploads/products/artist-is-the-business-v2.html",
            is_active=True, is_new=True)
        db.session.add(p); db.session.commit(); print("Created — ID:", p.id)
    print("Done — visible in Admin > Products")
'''
with open(f'{BASE}/seed_ebook.py', 'w') as f:
    f.write(seed)

# ══════════════════════════════════════════════════════════════
# 5. PUSH + SEED
# ══════════════════════════════════════════════════════════════
print('[5/5] Pushing to GitHub...')
os.system(f'cd {BASE} && git add -A && git commit -m "final overhaul: hero, tip jar, admin, link reset, ebook" && git push')
os.system(f'cd {BASE} && python3 seed_ebook.py')
print('')
print('=' * 60)
print('DONE — Railway deploys in ~60 seconds')
print('=' * 60)
