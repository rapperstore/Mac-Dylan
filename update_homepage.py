import re

with open('templates/index.html', 'r') as f:
    idx = f.read()

idx = re.sub(r'\n<section class="tip-section".*?</section>', '', idx, flags=re.DOTALL)
idx = re.sub(r'<section class="social-section".*?</section>\n', '', idx, flags=re.DOTALL)
idx = re.sub(r'<!-- SOCIAL BAR -->.*?</div>\n', '', idx, flags=re.DOTALL)
idx = re.sub(r'<!-- FLOATING TIP JAR -->.*?</a>\n', '', idx, flags=re.DOTALL)

new_css = """
.tip-float{position:fixed;top:72px;right:20px;z-index:500;display:flex;flex-direction:column;align-items:center;gap:4px;cursor:pointer;text-decoration:none}
.tip-jar-wrap{position:relative;width:52px;height:52px}
.tip-jar-icon{font-size:36px;line-height:1;display:block;filter:drop-shadow(0 0 8px rgba(200,75,10,.6));animation:jarFloat 3s ease-in-out infinite}
.tip-float:hover .tip-jar-icon{filter:drop-shadow(0 0 16px rgba(232,114,12,.9))}
.tip-coins{position:absolute;top:-6px;right:-4px;display:flex;gap:2px}
.tip-coin{width:10px;height:10px;background:var(--flame);border-radius:50%;animation:coinFly 2.4s ease-in-out infinite;opacity:0}
.tip-coin:nth-child(2){animation-delay:.4s}.tip-coin:nth-child(3){animation-delay:.8s}
.tip-label{font-family:'Space Mono',monospace;font-size:7px;letter-spacing:.18em;color:var(--ember);text-transform:uppercase;background:rgba(5,4,3,.85);padding:2px 6px;border:1px solid var(--border)}
@keyframes jarFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes coinFly{0%{opacity:0;transform:translateY(0) scale(0)}20%{opacity:1;transform:translateY(-8px) scale(1)}60%{opacity:.6;transform:translateY(-18px) scale(.8)}100%{opacity:0;transform:translateY(-28px) scale(0)}}
.social-bar{padding:40px 48px 56px;border-top:1px solid var(--border);display:flex;flex-direction:column;align-items:center;gap:20px}
.social-bar-label{font-family:'Space Mono',monospace;font-size:8px;letter-spacing:.5em;color:var(--ember);text-transform:uppercase}
.social-bar-icons{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
.sb-icon{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid var(--ember);background:rgba(200,75,10,.08);transition:all .25s;color:var(--ember)}
.sb-icon svg{width:20px;height:20px;fill:currentColor;opacity:.8;transition:opacity .2s}
.sb-icon:hover{background:var(--ember);border-color:var(--fire);box-shadow:0 0 18px rgba(200,75,10,.5)}
.sb-icon:hover svg{opacity:1;fill:var(--white)}
@media(max-width:900px){.tip-float{top:64px;right:12px}.social-bar{padding:32px 24px 44px}}
"""

tip_float = """<!-- FLOATING TIP JAR -->
<a class="tip-float" href="#" onclick="sendTip(event)" title="Leave a tip">
  <div class="tip-jar-wrap">
    <span class="tip-jar-icon">🫙</span>
    <div class="tip-coins"><div class="tip-coin"></div><div class="tip-coin"></div><div class="tip-coin"></div></div>
  </div>
  <span class="tip-label">Tip Jar</span>
</a>
"""

social_bar = """<!-- SOCIAL BAR -->
<div class="social-bar">
  <div class="social-bar-label">Follow the Movement</div>
  <div class="social-bar-icons">
    <a href="https://instagram.com/macdylan4ever" target="_blank" class="sb-icon" title="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
    <a href="https://facebook.com/macdylan4ever" target="_blank" class="sb-icon" title="Facebook"><svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
    <a href="https://youtube.com/@macdylan" target="_blank" class="sb-icon" title="YouTube"><svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
    <a href="https://open.spotify.com/artist/macdylan" target="_blank" class="sb-icon" title="Spotify"><svg viewBox="0 0 24 24"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg></a>
    <a href="https://music.apple.com/us/artist/macdylan" target="_blank" class="sb-icon" title="Apple Music"><svg viewBox="0 0 24 24"><path d="M23.994 6.124a9.23 9.23 0 00-.24-2.19c-.317-1.31-1.062-2.31-2.18-3.043a5.022 5.022 0 00-1.877-.726 10.496 10.496 0 00-1.564-.15H5.986c-.152.01-.303.017-.455.026C4.786.07 4.043.15 3.34.428 2.004.958 1.04 1.88.475 3.208A4.95 4.95 0 00.05 4.822c-.013.35-.018.7-.02 1.05V18.13c.003.35.008.7.02 1.05.1 1.55.58 2.79 1.53 3.73.95.94 2.1 1.37 3.42 1.49.33.03.67.04 1 .04h12.01c.34 0 .67-.01 1-.04 1.32-.12 2.47-.55 3.42-1.49.95-.94 1.43-2.18 1.53-3.73.013-.35.018-.7.02-1.05V5.872c-.002-.35-.007-.7-.02-1.05z"/><path d="M17.17 8.23l-5.72 1.06v5.19c-.51-.31-1.1-.49-1.73-.49-1.88 0-3.4 1.52-3.4 3.4s1.52 3.4 3.4 3.4 3.4-1.52 3.4-3.4V10.36l4.5-.84V8.23z" fill="white"/></svg></a>
    <a href="https://soundcloud.com/macdylan4ever" target="_blank" class="sb-icon" title="SoundCloud"><svg viewBox="0 0 24 24"><path d="M1.175 12.225c-.015 0-.023.01-.023.025l-.323 2.056.323 2.046c0 .016.008.025.023.025s.023-.009.023-.025l.366-2.046-.366-2.056c0-.015-.009-.025-.023-.025zm22.444-.09C22.08 9.28 19.722 7.5 17 7.5c-.678 0-1.33.114-1.938.322C14.18 5.129 11.584 3.5 8.6 3.5 5.06 3.5 2.2 6.36 2.2 9.9v.055C1.54 10.37 1 11.21 1 12.2c0 1.547 1.253 2.8 2.8 2.8H22c1.105 0 2-.895 2-2 0-1.018-.76-1.857-1.752-1.972l.527.331z"/></svg></a>
  </div>
</div>
"""

tip_js = """
window.sendTip = function(e) {
  if(e) e.preventDefault();
  var amt = prompt('How much would you like to tip Mac Dylan?\\n\\nEnter an amount (e.g. 5, 10, 25):', '10');
  if (!amt || isNaN(+amt) || +amt < 1) return;
  fetch('/payments/tip', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({amount: +amt, email: ''})
  }).then(function(r){return r.json()})
    .then(function(d){if(d.checkout_url) window.location.href=d.checkout_url;})
    .catch(function(){alert('Tip jar requires Stripe to be configured.');});
};
"""

# Inject CSS
if 'tip-float' not in idx:
    idx = idx.replace('{% endblock %}\n{% block content %}', new_css + '\n{% endblock %}\n{% block content %}', 1)

# Add floating tip jar after opening page div
if 'tip-float' not in idx:
    idx = idx.replace('<div class="page">', '<div class="page">\n' + tip_float, 1)

# Add social bar before quote section
if 'social-bar' not in idx:
    idx = idx.replace('<div class="quote"', social_bar + '\n<div class="quote"')

# Add tip JS
if 'sendTip' not in idx:
    idx = idx.replace('</script>\n{% endblock %}', tip_js + '\n</script>\n{% endblock %}')
else:
    idx = re.sub(r'window\.sendTip\s*=\s*function.*?\};\n', tip_js + '\n', idx, flags=re.DOTALL)

with open('templates/index.html', 'w') as f:
    f.write(idx)

print('done - all updates applied')
