import os, re

BASE = os.path.expanduser('~/Desktop/macdylan')

with open(f'{BASE}/templates/index.html', 'r') as f:
    idx = f.read()

# ═══════════════════════════════════════════════════════════════
# STEP 1 — REPLACE ENTIRE EXTRA_STYLES BLOCK
# ═══════════════════════════════════════════════════════════════
new_styles = '''{% block extra_styles %}
/* ── HERO ──────────────────────────────────────────────── */
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 88px;position:relative}
.hero-eyebrow{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:20px;opacity:0;animation:burnIn 1s ease forwards .4s}
.hero-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(80px,16vw,210px);line-height:.84;letter-spacing:.01em;opacity:0;animation:burnIn 1s ease forwards .7s}
.hero-title .outline{color:var(--fire);display:block;text-shadow:0 0 80px rgba(232,114,12,.45),0 0 160px rgba(200,75,10,.2)}
.hero-desc{font-size:clamp(15px,2vw,21px);font-style:italic;color:var(--ash);margin-top:24px;max-width:540px;line-height:1.75;opacity:0;animation:burnIn 1s ease forwards 1s}
.hero-actions{margin-top:48px;opacity:0;animation:burnIn 1s ease forwards 1.3s}
/* ── BUTTONS ────────────────────────────────────────────── */
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.btn-fire{display:inline-block;padding:15px 38px;background:var(--ember);color:#f5f0e8 !important;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.3em;text-transform:uppercase;text-decoration:none !important;border:none;transition:background .25s,box-shadow .25s,transform .2s;position:relative;overflow:hidden}
.btn-fire::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.1),transparent);pointer-events:none}
.btn-fire:hover{background:var(--fire);box-shadow:0 0 40px rgba(200,75,10,.5);transform:translateY(-1px);color:#f5f0e8 !important}
.btn-ghost{display:inline-block;padding:14px 38px;background:transparent;color:#b8a898 !important;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.3em;text-transform:uppercase;text-decoration:none !important;border:1px solid rgba(200,75,10,.3);transition:all .25s}
.btn-ghost:hover{border-color:var(--ember);color:var(--fire) !important;transform:translateY(-1px)}
/* ── TIP JAR ────────────────────────────────────────────── */
.hero-sub-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:32px}
.hero-sep{width:1px;height:18px;background:rgba(200,75,10,.25);display:inline-block;flex-shrink:0}
.tip-jar{display:inline-flex;align-items:center;gap:10px;padding:10px 22px;background:rgba(200,75,10,.08);border:1px solid rgba(200,75,10,.3);text-decoration:none !important;color:#c84b0a !important;font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;text-transform:uppercase;transition:all .25s;position:relative;overflow:hidden}
.tip-jar::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(200,75,10,.08),transparent);opacity:0;transition:opacity .25s}
.tip-jar:hover{background:rgba(200,75,10,.16);border-color:var(--ember);box-shadow:0 0 20px rgba(200,75,10,.25);color:#c84b0a !important}
.tip-jar:hover::before{opacity:1}
.tip-jar-wrap{position:relative;display:inline-flex;align-items:center;gap:4px}
.tip-jar-emoji{font-size:18px;line-height:1;display:inline-block;animation:jarFloat 3s ease-in-out infinite}
.tip-coin{width:5px;height:5px;border-radius:50%;background:var(--flame);opacity:0;display:inline-block;animation:coinPop 2.2s ease-in-out infinite;position:absolute;top:0;left:8px}
.tip-coin:nth-child(2){animation-delay:.3s;left:14px}
.tip-coin:nth-child(3){animation-delay:.6s;left:20px}
.tip-jar-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;color:#c84b0a;text-transform:uppercase}
@keyframes jarFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-4px) rotate(2deg)}}
@keyframes coinPop{0%{opacity:0;transform:translateY(0) scale(0)}25%{opacity:1;transform:translateY(-10px) scale(1)}100%{opacity:0;transform:translateY(-28px) scale(.5)}}
/* ── EBOOK TRIGGER ──────────────────────────────────────── */
.ebook-trigger{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:transparent;border:1px solid rgba(200,75,10,.2);color:#6b5a4a !important;font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.22em;text-transform:uppercase;text-decoration:none !important;cursor:pointer;transition:all .25s}
.ebook-trigger:hover{border-color:rgba(200,75,10,.4);color:#b8a898 !important;background:rgba(200,75,10,.04)}
.ebook-trigger-icon{font-size:14px;line-height:1}
/* ── HERO STATS ─────────────────────────────────────────── */
.hero-stats{display:flex;align-items:center;gap:22px;padding-top:22px;border-top:1px solid rgba(200,75,10,.12);flex-wrap:wrap}
.hero-stat{text-align:left}
.hero-stat-n{font-family:'Bebas Neue',sans-serif;font-size:28px;color:var(--fire);line-height:1}
.hero-stat-l{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase;margin-top:3px}
.hero-stat-sep{width:1px;height:30px;background:rgba(200,75,10,.15);flex-shrink:0}
/* ── EBOOK MODAL ────────────────────────────────────────── */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.85);backdrop-filter:blur(8px);z-index:2000;opacity:0;pointer-events:none;transition:opacity .3s;display:flex;align-items:center;justify-content:center;padding:24px}
.modal-overlay.open{opacity:1;pointer-events:all}
.modal-box{background:#110d08;border:1px solid rgba(200,75,10,.35);max-width:600px;width:100%;position:relative;transform:translateY(24px);transition:transform .35s cubic-bezier(.4,0,.2,1);overflow:hidden}
.modal-overlay.open .modal-box{transform:translateY(0)}
.modal-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--ember),var(--flame),var(--ember));background-size:200% 100%;animation:shimmer 3s linear infinite}
@keyframes shimmer{0%{background-position:0% 50%}100%{background-position:200% 50%}}
.modal-close{position:absolute;top:16px;right:16px;background:none;border:1px solid rgba(200,75,10,.3);color:var(--muted);width:32px;height:32px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px;transition:all .2s;line-height:1;z-index:1}
.modal-close:hover{border-color:var(--ember);color:var(--fire)}
.modal-cover{background:linear-gradient(135deg,#0d0a07,#1e1008);padding:44px 48px;text-align:center;border-bottom:1px solid rgba(200,75,10,.2);position:relative;overflow:hidden}
.modal-cover::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 50%,rgba(200,75,10,.12),transparent)}
.modal-cover-the{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.5em;color:var(--ash);text-transform:uppercase;display:block;margin-bottom:8px;position:relative;z-index:1}
.modal-cover-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(44px,8vw,72px);line-height:.9;color:var(--white);position:relative;z-index:1}
.modal-cover-title em{color:var(--fire);font-style:normal;display:block;text-shadow:0 0 40px rgba(232,114,12,.4)}
.modal-cover-sub{font-family:'Cormorant Garamond',serif;font-size:16px;font-style:italic;color:var(--ash);margin-top:14px;position:relative;z-index:1}
.modal-body{padding:36px 40px}
.modal-desc{font-family:'Cormorant Garamond',serif;font-size:18px;line-height:1.8;color:var(--ash);margin-bottom:24px;font-style:italic}
.modal-features{list-style:none;margin-bottom:28px;display:grid;grid-template-columns:1fr 1fr;gap:8px}
.modal-features li{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.15em;color:var(--muted);text-transform:uppercase;display:flex;align-items:center;gap:8px}
.modal-features li::before{content:'→';color:var(--ember);flex-shrink:0}
.modal-footer{display:flex;align-items:center;justify-content:space-between;padding-top:20px;border-top:1px solid rgba(200,75,10,.15);flex-wrap:wrap;gap:16px}
.modal-price{font-family:'Bebas Neue',sans-serif;font-size:44px;color:var(--fire);line-height:1}
.modal-price-note{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase;margin-top:4px}
.modal-buy{display:inline-block;padding:14px 32px;background:var(--ember);color:#f5f0e8 !important;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.3em;text-transform:uppercase;text-decoration:none !important;border:none;cursor:pointer;transition:all .25s}
.modal-buy:hover{background:var(--fire);box-shadow:0 0 30px rgba(200,75,10,.4);color:#f5f0e8 !important}
/* ── ABOUT / SECTIONS ───────────────────────────────────── */
.about{padding:120px 48px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;border-top:1px solid var(--border)}
.about-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:18px}
.about-heading{font-family:'Bebas Neue',sans-serif;font-size:clamp(40px,6vw,72px);line-height:.95;margin-bottom:20px}.about-heading em{color:var(--fire);font-style:normal}
.about-text{font-size:17px;line-height:1.8;color:var(--ash);font-style:italic;margin-bottom:20px}
.about-contact{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--muted)}.about-contact a{color:var(--ember);text-decoration:none}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--border);border:1px solid var(--border)}
.stat{background:var(--card);padding:30px 22px;transition:background .2s}.stat:hover{background:var(--card2)}
.stat-num{font-family:'Bebas Neue',sans-serif;font-size:48px;color:var(--fire);line-height:1;margin-bottom:4px}
.stat-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--muted);text-transform:uppercase}
.section{padding:0 48px 100px}
.sec-hdr{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:32px}
.sec-lbl{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase}
.sec-link{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--muted);text-transform:uppercase;text-decoration:none;transition:color .2s}.sec-link:hover{color:var(--fire)}
.mini-playlist{background:var(--card);border:1px solid var(--border)}
.mini-row{display:flex;align-items:center;padding:12px 18px;border-bottom:1px solid var(--border);gap:12px;text-decoration:none;transition:background .2s;position:relative;overflow:hidden;color:inherit}
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
/* ── CREDITS ────────────────────────────────────────────── */
.credits-section{padding:0 48px 80px}
.credits-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:2px;background:var(--border);border:1px solid var(--border)}
.credit-card{background:var(--card);padding:18px 20px;transition:background .2s}
.credit-card:hover{background:var(--card2)}
.credit-artist{font-family:'Bebas Neue',sans-serif;font-size:17px;color:var(--white);letter-spacing:.04em;line-height:1}
.credit-role{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.28em;color:var(--ember);text-transform:uppercase;margin-top:4px}
.credit-track{font-size:12px;color:var(--muted);font-style:italic;margin-top:4px}
.credits-empty{padding:28px;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase;background:var(--card);text-align:center}
/* ── NEWSLETTER ─────────────────────────────────────────── */
.newsletter{padding:80px 48px;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.nl-heading{font-family:'Bebas Neue',sans-serif;font-size:clamp(36px,5vw,62px);line-height:.95;margin-bottom:12px}.nl-heading em{color:var(--fire);font-style:normal}
.nl-sub{font-size:15px;color:var(--ash);font-style:italic;line-height:1.7}
.nl-form-wrap{display:flex;gap:2px}
.nl-input{flex:1;padding:14px 16px;background:var(--card);border:1px solid var(--border);color:var(--white);font-family:'Cormorant Garamond',serif;font-size:16px;transition:border-color .2s}
.nl-input:focus{outline:none;border-color:var(--ember)}.nl-input::placeholder{color:var(--muted);font-style:italic}
.nl-btn{padding:14px 24px;background:var(--ember);border:none;color:var(--white);font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.28em;text-transform:uppercase;transition:background .2s;white-space:nowrap;cursor:pointer}.nl-btn:hover{background:var(--fire)}
.nl-note{font-family:'Space Mono',monospace;font-size:8px;color:var(--muted);letter-spacing:.14em;margin-top:8px}
.nl-ok{display:none;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--fire);text-transform:uppercase;padding:12px 0}
/* ── QUOTE ──────────────────────────────────────────────── */
.quote{padding:90px 48px;border-top:1px solid var(--border);border-bottom:1px solid var(--border);text-align:center;position:relative;overflow:hidden}
.quote::before{content:'"';position:absolute;top:-80px;left:50%;transform:translateX(-50%);font-family:'Bebas Neue',sans-serif;font-size:380px;color:rgba(200,75,10,.03);pointer-events:none;line-height:1}
.quote-text{font-family:'Cormorant Garamond',serif;font-size:clamp(20px,4vw,40px);font-style:italic;font-weight:300;color:var(--white);max-width:780px;margin:0 auto 18px;line-height:1.4;position:relative}.quote-text em{color:var(--fire);font-style:normal}
.quote-attr{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.4em;color:var(--muted);text-transform:uppercase}
/* ── SOCIAL ─────────────────────────────────────────────── */
.social-section{padding:0 48px 56px}
.social-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase;margin-bottom:20px;display:flex;align-items:center;gap:12px}
.social-label::after{content:'';flex:1;height:1px;background:var(--border)}
.social-circles{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.sb-btn{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid rgba(200,75,10,.4);background:rgba(200,75,10,.06);transition:all .2s;color:var(--ember);text-decoration:none;flex-shrink:0}
.sb-btn svg{width:12px;height:12px;fill:currentColor;transition:fill .2s}
.sb-btn:hover{background:var(--ember);border-color:var(--fire);box-shadow:0 0 12px rgba(200,75,10,.4)}
.sb-btn:hover svg{fill:#f5f0e8}
/* ── RESPONSIVE ─────────────────────────────────────────── */
@media(max-width:900px){
  .hero{padding:0 24px 64px}
  .about{grid-template-columns:1fr;padding:80px 24px;gap:44px}
  .section,.social-section,.credits-section{padding-left:24px;padding-right:24px}
  .svc-grid{grid-template-columns:1fr}
  .newsletter{grid-template-columns:1fr;padding:56px 24px;gap:28px}
  .nl-form-wrap{flex-direction:column}
  .quote{padding:68px 24px}
  .hero-stats{gap:14px}
  .hero-stat-n{font-size:22px}
  .modal-features{grid-template-columns:1fr}
  .modal-body{padding:24px}
  .modal-cover{padding:32px 24px}
}
{% endblock %}'''

idx = re.sub(r'{% block extra_styles %}.*?{% endblock %}', new_styles, idx, flags=re.DOTALL)

# ═══════════════════════════════════════════════════════════════
# STEP 2 — REBUILD CONTENT BLOCK (hero + modal)
# ═══════════════════════════════════════════════════════════════
new_content_open = '''{% block content %}
<!-- ══ EBOOK MODAL ══════════════════════════════════════════ -->
<div class="modal-overlay" id="ebook-modal" onclick="closeEbookModal(event)">
  <div class="modal-box">
    <button class="modal-close" onclick="closeEbookModal()" title="Close">&#x2715;</button>
    <div class="modal-cover">
      <span class="modal-cover-the">Mac Dylan Presents</span>
      <h2 class="modal-cover-title">The Artist<em>Is The Business</em></h2>
      <p class="modal-cover-sub">The complete independent artist blueprint</p>
    </div>
    <div class="modal-body">
      <p class="modal-desc">Everything the music industry won&#x27;t tell you — laid out in 9 chapters with real frameworks, income strategies, and a 90-day execution plan built for artists who are done waiting and ready to build.</p>
      <ul class="modal-features">
        <li>9 chapters of real-world strategy</li>
        <li>Income streams that actually work</li>
        <li>Brand building from scratch</li>
        <li>Organic growth without ads</li>
        <li>AI as a force multiplier</li>
        <li>90-day action checklist</li>
        <li>Interactive chapter navigation</li>
        <li>Instant digital download</li>
      </ul>
      <div class="modal-footer">
        <div>
          <div class="modal-price">$27</div>
          <div class="modal-price-note">One-time &middot; Instant download &middot; Yours forever</div>
        </div>
        <a href="{{ url_for('store.index') }}" class="modal-buy">Get The Blueprint &#x2192;</a>
      </div>
    </div>
  </div>
</div>

<!-- ══ HERO ══════════════════════════════════════════════════ -->
<section class="hero">
  <div>
    <div class="hero-eyebrow">Boise, Idaho &middot; Mix &middot; Record &middot; Develop</div>
    <h1 class="hero-title">Mac<span class="outline">Dylan</span></h1>
    <p class="hero-desc">Where independent artists come to sound like they mean it. Mix engineering, production, and artist development from someone who built from nothing.</p>
    <div class="hero-actions">
      <div class="hero-cta">
        <a href="{{ url_for('services.index') }}" class="btn-fire">Book a Session</a>
        <a href="{{ url_for('beats.index') }}" class="btn-ghost">Browse Beats</a>
      </div>
      <div class="hero-sub-row">
        <a class="tip-jar" href="#" onclick="openTip(event)">
          <span class="tip-jar-wrap">
            <span class="tip-jar-emoji">&#x1F9AB;</span>
            <span class="tip-coin"></span>
            <span class="tip-coin"></span>
            <span class="tip-coin"></span>
          </span>
          <span class="tip-jar-label">Leave a Tip</span>
        </a>
        <span class="hero-sep"></span>
        <button class="ebook-trigger" onclick="openEbookModal()">
          <span class="ebook-trigger-icon">&#x1F4D6;</span>
          The Blueprint
        </button>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-n">10+</div><div class="hero-stat-l">Years</div></div>
        <span class="hero-stat-sep"></span>
        <div class="hero-stat"><div class="hero-stat-n">500+</div><div class="hero-stat-l">Records Mixed</div></div>
        <span class="hero-stat-sep"></span>
        <div class="hero-stat"><div class="hero-stat-n">100%</div><div class="hero-stat-l">Independent</div></div>
        <span class="hero-stat-sep"></span>
        <div class="hero-stat"><div class="hero-stat-n">&#x221E;</div><div class="hero-stat-l">Artist First</div></div>
      </div>
    </div>
  </div>
</section>'''

# Replace everything from {% block content %} up to and including </section>\n\n<section class="about"
idx = re.sub(
    r'{% block content %}.*?</section>\s*\n\s*\n\s*<section class="about"',
    new_content_open + '\n\n<section class="about"',
    idx, flags=re.DOTALL
)

# ═══════════════════════════════════════════════════════════════
# STEP 3 — REMOVE TIP SECTION (duplicate banner lower on page)
# ═══════════════════════════════════════════════════════════════
idx = re.sub(r'\n<!-- Tip Jar -->.*?</section>\n', '\n', idx, flags=re.DOTALL)
idx = re.sub(r'\n<section class="tip-section".*?</section>\n', '\n', idx, flags=re.DOTALL)

# ═══════════════════════════════════════════════════════════════
# STEP 4 — REMOVE PLAYER SECTION (empty, no tracks loaded)
# ═══════════════════════════════════════════════════════════════
idx = re.sub(r'\n<!-- Music Player -->.*?</section>\n', '\n', idx, flags=re.DOTALL)
idx = re.sub(r'\n<section class="player-section".*?</section>\n', '\n', idx, flags=re.DOTALL)

# ═══════════════════════════════════════════════════════════════
# STEP 5 — FIX QUOTE (remove phone number)
# ═══════════════════════════════════════════════════════════════
idx = re.sub(
    r'<div class="quote-attr">.*?</div>',
    '<div class="quote-attr">Mac Dylan &middot; Boise, Idaho</div>',
    idx
)

# ═══════════════════════════════════════════════════════════════
# STEP 6 — FIX NEWSLETTER URL
# ═══════════════════════════════════════════════════════════════
idx = idx.replace(
    "fetch('https://app.convertkit.com/forms/9292507/subscriptions'",
    "fetch('https://mac-dylan.kit.com/b5923233e5/subscriptions'"
)

# ═══════════════════════════════════════════════════════════════
# STEP 7 — REMOVE PLACEHOLDER BEATS
# ═══════════════════════════════════════════════════════════════
idx = re.sub(
    r'\s*\{% else %\}\s*(?:<!.*?-->)?\s*<a href.*?Midnight Cipher.*?</a>\s*<a href.*?Ember Season.*?</a>\s*<a href.*?Cinematic Chaos.*?</a>\s*\{% endif %\}',
    "\n    {% else %}\n      <div style=\"padding:20px 18px;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase\">New beats dropping soon</div>\n    {% endif %}",
    idx, flags=re.DOTALL
)

# ═══════════════════════════════════════════════════════════════
# STEP 8 — ADD MODAL JS TO EXTRA_SCRIPTS
# ═══════════════════════════════════════════════════════════════
modal_js = """
window.openEbookModal = function() {
  document.getElementById('ebook-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
};
window.closeEbookModal = function(e) {
  if (e && e.target !== document.getElementById('ebook-modal')) return;
  document.getElementById('ebook-modal').classList.remove('open');
  document.body.style.overflow = '';
};
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') window.closeEbookModal();
});
"""

idx = idx.replace(
    'window.subCK = function(e) {',
    modal_js + '\nwindow.subCK = function(e) {'
)

with open(f'{BASE}/templates/index.html', 'w') as f:
    f.write(idx)
print('[1/3] index.html rebuilt')

# ═══════════════════════════════════════════════════════════════
# STEP 9 — BASE.HTML global link reset
# ═══════════════════════════════════════════════════════════════
with open(f'{BASE}/templates/base.html', 'r') as f:
    base = f.read()

if 'a{color:inherit' not in base:
    base = base.replace(
        'body{background:var(--black)',
        'a{color:inherit;text-decoration:none}\nbutton{cursor:pointer}\nbody{background:var(--black)'
    )
    with open(f'{BASE}/templates/base.html', 'w') as f:
        f.write(base)
    print('[2/3] base.html global link reset added')
else:
    print('[2/3] base.html already has link reset')

# ═══════════════════════════════════════════════════════════════
# STEP 10 — PUSH
# ═══════════════════════════════════════════════════════════════
print('[3/3] Pushing to GitHub...')
os.system(f'cd {BASE} && git add -A && git commit -m "full homepage enhancement: tip jar, ebook modal, hero rebuilt" && git push')
print('')
print('=' * 60)
print('DONE - Railway deploys in ~60 seconds')
print('Homepage changes:')
print('  - Hero: rebuilt with proper animations and enhanced DYLAN glow')
print('  - Buttons: orange/ghost with no blue link issues ever')
print('  - Tip jar: fixed emoji, floating animation, coin burst')
print('  - Blueprint: now opens a full ebook modal (closeable)')
print('  - Stats row: 10+ / 500+ / 100% / infinity')
print('  - Duplicate tip banner: removed')
print('  - Empty player section: removed')
print('  - Placeholder beats: removed')
print('  - Quote phone number: removed')
print('  - Newsletter: correct Kit URL')
print('=' * 60)
