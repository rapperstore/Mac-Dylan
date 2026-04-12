import os
from PIL import Image, ImageDraw

def make_frame(size):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,size,size], fill=(13,10,7,255))
    s = size / 64
    def p(pts): return [(x*s, y*s) for x,y in pts]
    # Outer flame
    d.polygon(p([(18,56),(14,48),(12,38),(16,26),(20,20),(19,28),(22,32),(24,24),(28,14),(27,24),(31,30),(34,22),(34,14),(34,14),(40,24),(40,32),(44,24),(46,18),(46,18),(50,28),(49,36),(52,30),(54,24),(54,24),(57,34),(55,42),(52,48),(48,54),(44,58),(40,58)]), fill=(150,35,5,255))
    # Mid flame
    d.polygon(p([(22,56),(18,46),(16,36),(20,24),(23,18),(22,27),(25,32),(27,22),(30,12),(30,22),(33,29),(36,20),(37,14),(38,22),(41,30),(44,22),(45,17),(46,26),(48,34),(50,28),(52,22),(53,30),(52,40),(49,50),(46,56),(42,58),(36,58)]), fill=(220,90,12,255))
    # Inner hot
    d.polygon(p([(26,56),(23,48),(22,38),(25,28),(28,22),(27,30),(30,35),(32,26),(34,16),(34,26),(37,33),(40,24),(40,18),(41,26),(43,33),(46,25),(46,20),(47,29),(48,37),(50,31),(51,26),(52,33),(51,42),(48,51),(45,56),(41,58),(35,58)]), fill=(248,185,66,255))
    # Bright core tip
    d.polygon(p([(30,56),(28,48),(28,38),(31,30),(34,24),(33,31),(35,36),(37,28),(38,20),(39,28),(41,34),(43,27),(44,22),(44,30),(45,36),(47,30),(47,25),(48,32),(48,40),(49,35),(50,30),(51,36),(50,44),(48,51),(46,56),(42,58),(36,58)]), fill=(253,214,138,255))
    return img

print('Generating favicons...')
make_frame(180).save('static/favicon-180.png', 'PNG')
make_frame(32).save('static/favicon-32.png', 'PNG')
imgs = [make_frame(16), make_frame(32)]
imgs[0].save('static/favicon.ico', format='ICO', sizes=[(16,16),(32,32)], append_images=[imgs[1]])

svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0d0a07"/><path d="M18 56 C14 48 12 38 16 26 C20 20 19 28 22 32 C24 24 28 14 27 24 C31 30 34 22 34 14 C40 24 40 32 44 24 C46 18 50 28 49 36 C52 30 54 24 57 34 C55 42 52 48 48 54 C44 58 40 58 18 56Z" fill="#961f05"/><path d="M22 56 C18 46 16 36 20 24 C23 18 22 27 25 32 C27 22 30 12 30 22 C33 29 36 20 37 14 C38 22 41 30 44 22 C45 17 46 26 48 34 C50 28 52 22 53 30 C52 40 49 50 46 56 C42 58 36 58 22 56Z" fill="#dc5a0c"/><path d="M26 56 C23 48 22 38 25 28 C28 22 27 30 30 35 C32 26 34 16 34 26 C37 33 40 24 40 18 C41 26 43 33 46 25 C46 20 47 29 48 37 C50 31 51 26 52 33 C51 42 48 51 45 56 C41 58 35 58 26 56Z" fill="#f8b942"/><path d="M30 56 C28 48 28 38 31 30 C34 24 33 31 35 36 C37 28 38 20 39 28 C41 34 43 27 44 22 C44 30 45 36 47 30 C47 25 48 32 48 40 C49 35 50 30 51 36 C50 44 48 51 46 56 C42 58 36 58 30 56Z" fill="#fdd68a"/></svg>'
with open('static/favicon.svg', 'w') as f:
    f.write(svg)

with open('templates/base.html', 'r') as f:
    base = f.read()

import re
base = re.sub(r'<link rel="icon"[^>]*>\s*', '', base)
base = re.sub(r'<link rel="apple-touch-icon"[^>]*>\s*', '', base)
base = re.sub(r'<meta name="theme-color"[^>]*>\s*', '', base)

tags = '  <link rel="icon" type="image/x-icon" href="/static/favicon.ico">\n  <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32.png">\n  <link rel="apple-touch-icon" sizes="180x180" href="/static/favicon-180.png">\n  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">\n  <meta name="theme-color" content="#0d0a07">'
base = base.replace('<title>', tags + '\n  <title>')

with open('templates/base.html', 'w') as f:
    f.write(base)

print('Favicon wired into base.html')
os.system('git add -A && git commit -m "add wide flame favicon" && git push')
print('DONE - Railway deploys in 60 seconds')
