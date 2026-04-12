import os, re

with open('templates/base.html', 'r') as f:
    base = f.read()

base = re.sub(r'\s*<link rel="icon"[^>]*>\n?', '', base)
base = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>\n?', '', base)
base = re.sub(r'\s*<meta name="theme-color"[^>]*>\n?', '', base)

tags = '  <link rel="icon" type="image/x-icon" href="/static/favicon.ico">\n  <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">\n  <link rel="apple-touch-icon" sizes="180x180" href="/static/favicon-180.png">\n  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">\n  <meta name="theme-color" content="#0d0a07">'

base = base.replace('<title>', tags + '\n  <title>')

with open('templates/base.html', 'w') as f:
    f.write(base)

print('Favicon tags wired into base.html')
os.system('git add -A && git commit -m "wire favicon into base.html" && git push')
print('DONE - Railway deploys in 60 seconds')
