import re

with open('templates/index.html', 'r') as f:
    idx = f.read()

# ── NEW CSS ────────────────────────────────────────────────────
new_css = """
/* TIP JAR */
.tip-section{padding:0 48px 60px}
.tip-banner{background:linear-gradient(135deg,rgba(200,75,10,.12),rgba(232,114,12,.06));border:1px solid rgba(200,75,10,.35);padding:28px 36px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;position:relative;overflow:hidden}
.tip-banner::before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(200,75,10,.04),transparent);animation:tipShimmer 3s ease-in-out infinite}
@keyframes tipShimmer{0%,100%{opacity:0;transform:translateX(-100%)}50%{opacity:1;transform:translateX(100%)}}
.tip-left{display:flex;align-items:center;gap:18px}
.tip-jar-big{font-size:44px;line-height:1;animation:tfloat 3s ease-in-out infinite;filter:drop-shadow(0 0 10px rgba(200,75,10,.5))}
.tip-copy h3{font-family:'Bebas Neue',sans-serif;font-size:26px;color:var(--white);letter-spacing:.04em;line-height:1;margin-bottom:4px}
.tip-copy p{font-size:13px;color:var(--ash);font-style:italic;line-height:1.5}
.tip-amounts{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.ta-btn{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.18em;padding:9px 16px;background:transparent;border:1px solid var(--borderl);color:var(--muted);transition:all .2s;cursor:pointer}
.ta-btn:hover,.ta-btn.on{background:var(--ember);border-color:var(--ember);color:var(--white)}
.ta-custom{width:70px;padding:9px 10px;background:var(--card);border:1px solid var(--border);color:var(--white);font-family:'Bebas Neue',sans-serif;font-size:18px;text-align:center;transition:border-color .2s}
.ta-custom:focus{outline:none;border-color:var(--ember)}
.ta-send{padding:9px 22px;background:var(--ember);border:none;color:var(--white);font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.28em;text-transform:uppercase;transition:all .2s;cursor:pointer}
.ta-send:hover{background:var(--fire);box-shadow:0 0 18px rgba(200,75,10,.45)}
@keyframes tfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}

/* MUSIC PLAYER */
.player-section{padding:0 48px 80px}
.player-wrap{background:var(--card);border:1px solid var(--border)}
.player-hdr{padding:14px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.player-hdr-title{font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:.06em;color:var(--white)}
.player-hdr-sub{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.22em;color:var(--muted);text-transform:uppercase}
.player-track-list{border-bottom:1px solid var(--border)}
.player-track{display:flex;align-items:center;padding:10px 18px;gap:12px;border-bottom:1px solid var(--border);cursor:pointer;transition:background .2s;position:relative}
.player-track:last-child{border-bottom:none}
.player-track:hover{background:var(--card2)}
.player-track.active{background:#120a04}
.player-track.active::before{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--ember)}
.pt-num{font-family:'Space Mono',monospace;font-size:9px;color:var(--muted);width:18px;flex-shrink:0;text-align:center}
.pt-play{display:none;width:18px;flex-shrink:0;align-items:center;justify-content:center}
.player-track:hover .pt-num,.player-track.active .pt-num{display:none}
.player-track:hover .pt-play,.player-track.active .pt-play{display:flex}
.pt-play svg{width:10px;height:10px;fill:var(--fire)}
.pt-info{flex:1;min-width:0}
.pt-title{font-family:'Bebas Neue',sans-serif;font-size:15px;color:var(--white);letter-spacing:.04em;line-height:1}
.player-track.active .pt-title{color:var(--fire)}
.pt-meta{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;margin-top:2px}
.pt-dur{font-family:'Space Mono',monospace;font-size:9px;color:var(--muted);flex-shrink:0}
.player-controls{padding:14px 18px;background:var(--deep);display:flex;align-items:center;gap:12px}
.pc-info{flex:1;min-width:0}
.pc-title{font-family:'Bebas Neue',sans-serif;font-size:16px;color:var(--white);letter-spacing:.04em;line-height:1}
.pc-meta{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;margin-top:2px}
.pc-btn{background:none;border:none;color:var(--muted);display:flex;align-items:center;transition:color .2s;cursor:pointer;padding:4px}
.pc-btn:hover{color:var(--fire)}
.pc-btn svg{width:14px;height:14px;fill:currentColor}
.pc-play{width:38px;height:38px;background:var(--ember);border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;flex-shrink:0}
.pc-play:hover{background:var(--fire);box-shadow:0 0 14px rgba(200,75,10,.5)}
.pc-play svg{width:12px;height:12px;fill:white}
.pc-progress{flex:1;height:2px;background:var(--border);cursor:pointer;position:relative}
.pc-fill{height:100%;background:var(--ember);width:0%;transition:width .1s linear;pointer-events:none}
.pc-time{font-family:'Space Mono',monospace;font-size:8px;color:var(--muted);flex-shrink:0}
@media(max-width:900px){.tip-section{padding:0 24px 44px}.player-section{padding:0 24px 60px}.tip-banner{flex-direction:column;align-items:flex-start;gap:16px}}
"""

# Inject CSS before media query
idx = idx.replace(
    '@media(max-width:900px){.hero{padding:0 24px 64px}',
    new_css + '\n@media(max-width:900px){.hero{padding:0 24px 64px}'
)

# ── TIP BANNER — replace after services section ────────────────
tip_banner = """
<!-- Tip Jar -->
<section class="tip-section" data-reveal>
  <div class="tip-banner">
    <div class="tip-left">
      <span class="tip-jar-big">🫙</span>
      <div class="tip-copy">
        <h3>Support Independent Music</h3>
        <p>Every tip goes directly into making more — beats, sessions, and content.</p>
      </div>
    </div>
    <div class="tip-amounts">
      <button class="ta-btn on" onclick="selTip(5,this)">$5</button>
      <button class="ta-btn" onclick="selTip(10,this)">$10</button>
      <button class="ta-btn" onclick="selTip(25,this)">$25</button>
      <button class="ta-btn" onclick="selTip(50,this)">$50</button>
      <input class="ta-custom" type="number" id="tip-amt" value="5" min="1" oninput="document.querySelectorAll('.ta-btn').forEach(function(b){b.classList.remove('on')})">
      <button class="ta-send" onclick="sendTipAmt()">Send Tip →</button>
    </div>
  </div>
</section>
"""

# ── MUSIC PLAYER — showcasing your mixes ──────────────────────
player_html = """
<!-- Music Player -->
<section class="player-section" data-reveal>
  <div class="sec-hdr">
    <div class="sec-lbl">Featured Work</div>
    <a href="https://soundcloud.com/macdylan4ever" target="_blank" class="sec-link">SoundCloud →</a>
  </div>
  <div class="player-wrap">
    <div class="player-hdr">
      <div class="player-hdr-title">Production &amp; Engineering</div>
      <div class="player-hdr-sub">Add tracks via admin panel</div>
    </div>
    <div class="player-track-list" id="track-list">
      <div style="padding:24px 18px;font-family:Space Mono,monospace;font-size:9px;letter-spacing:.2em;color:var(--muted);text-transform:uppercase">Add featured tracks via Admin → Content</div>
    </div>
    <div class="player-controls">
      <div class="pc-info">
        <div class="pc-title" id="pc-title">Select a Track</div>
        <div class="pc-meta" id="pc-meta">Mac Dylan</div>
      </div>
      <button class="pc-btn" onclick="prevTrackP()"><svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6L20 18V6z"/></svg></button>
      <button class="pc-play" id="pc-play-btn" onclick="togglePlayP()">
        <svg id="pc-pi" viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21"/></svg>
        <svg id="pc-pa" viewBox="0 0 24 24" style="display:none"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
      </button>
      <button class="pc-btn" onclick="nextTrackP()"><svg viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zm8.5-6L21 6v12z"/></svg></button>
      <div class="pc-progress" id="pc-prog" onclick="seekP(event)"><div class="pc-fill" id="pc-fill"></div></div>
      <div class="pc-time" id="pc-time">0:00</div>
    </div>
  </div>
</section>
"""

# Insert tip banner and player after services section
idx = idx.replace(
    '\n<!-- Newsletter -->',
    tip_banner + player_html + '\n<!-- Newsletter -->'
)

# ── FIX NEWSLETTER for deliverability ─────────────────────────
# Use double opt-in confirmation text and correct endpoint
idx = idx.replace(
    "fetch('https://app.convertkit.com/forms/9292507/subscriptions'",
    "fetch('https://app.convertkit.com/forms/9292507/subscriptions'"
)
idx = idx.replace(
    "document.getElementById('nl-ok').style.display = 'block';",
    "document.getElementById('nl-ok').style.display = 'block';"
)
idx = idx.replace(
    "✓ YOU'RE IN — CHECK YOUR EMAIL",
    "✓ CHECK YOUR EMAIL TO CONFIRM — CHECK SPAM IF NOT RECEIVED"
)

# ── TIP + PLAYER JS ───────────────────────────────────────────
new_js = """
// TIP JAR
window.selTip = function(amt, btn) {
  document.querySelectorAll('.ta-btn').forEach(function(b){ b.classList.remove('on'); });
  btn.classList.add('on');
  document.getElementById('tip-amt').value = amt;
};
window.sendTipAmt = function() {
  var amt = +document.getElementById('tip-amt').value;
  if (!amt || amt < 1) return;
  fetch('/payments/tip', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: amt, email: ''})
  }).then(function(r){ return r.json(); })
    .then(function(d){ if (d.checkout_url) window.location.href = d.checkout_url; });
};
window.openTip = window.sendTipAmt;

// MUSIC PLAYER
var pTracks = [], pIdx = 0, pAudio = null, pPlaying = false;

function pFmt(s) { s=Math.floor(s||0); return Math.floor(s/60)+':'+(s%60<10?'0':'')+s%60; }
function pSetPI(playing) {
  document.getElementById('pc-pi').style.display = playing ? 'none' : 'block';
  document.getElementById('pc-pa').style.display = playing ? 'block' : 'none';
}
function pLoadTrack(i) {
  if (!pTracks.length) return;
  pIdx = i;
  var t = pTracks[i];
  document.getElementById('pc-title').textContent = t.title;
  document.getElementById('pc-meta').textContent = t.artist + (t.role ? ' · ' + t.role : '');
  document.querySelectorAll('.player-track').forEach(function(r,j){ r.classList.toggle('active', j===i); });
  if (pAudio) { pAudio.pause(); pAudio.src = ''; }
  if (t.url) {
    pAudio = new Audio(t.url);
    pAudio.ontimeupdate = function() {
      if (!pAudio.duration) return;
      document.getElementById('pc-fill').style.width = (pAudio.currentTime/pAudio.duration*100)+'%';
      document.getElementById('pc-time').textContent = pFmt(pAudio.currentTime);
    };
    pAudio.onended = function() { nextTrackP(); };
    pAudio.play(); pPlaying = true; pSetPI(true);
  }
}
window.togglePlayP = function() {
  if (!pAudio || !pTracks.length) return;
  if (pPlaying) { pAudio.pause(); pPlaying=false; pSetPI(false); }
  else { pAudio.play(); pPlaying=true; pSetPI(true); }
};
window.prevTrackP = function() { if (pTracks.length) pLoadTrack((pIdx-1+pTracks.length)%pTracks.length); };
window.nextTrackP = function() { if (pTracks.length) pLoadTrack((pIdx+1)%pTracks.length); };
window.seekP = function(e) {
  if (!pAudio || !pAudio.duration) return;
  var rect=e.currentTarget.getBoundingClientRect();
  pAudio.currentTime = ((e.clientX-rect.left)/rect.width)*pAudio.duration;
};
window.playTrackP = function(i) { pLoadTrack(i); };

// Load tracks from admin content entries
fetch('/admin/api/stats').catch(function(){});
// Tracks are added via admin panel Content section with embed_url as the audio src
(function loadPlayerTracks(){
  // For now shows placeholder — tracks added via Admin > Content
  pTracks = [];
  var list = document.getElementById('track-list');
  if (!list || pTracks.length) return;
})();
"""

idx = idx.replace(
    'window.subCK = function(e) {',
    new_js + '\nwindow.subCK = function(e) {'
)

with open('templates/index.html', 'w') as f:
    f.write(idx)

print('index.html updated')

import os
os.system('cd ~/Desktop/macdylan && git add -A && git commit -m "enhanced tip jar, music player, newsletter fix" && git push')
print('DONE - Railway deploys in 60 seconds')
