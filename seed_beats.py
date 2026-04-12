import os, re, shutil, sys
sys.path.insert(0, '.')

BASE = os.path.expanduser('~/Desktop/macdylan')
WAV_SRC = os.path.expanduser('~/Desktop/2026 Beats- Mac Dylan/WAV')
WAV_DEST = os.path.join(BASE, 'static', 'uploads', 'beats')
os.makedirs(WAV_DEST, exist_ok=True)

from app import create_app
from database import db
from models import Beat

app = create_app()

def parse_filename(filename):
    stem = os.path.splitext(filename)[0]
    # Extract BPM and key from [140BPM F Min] pattern
    match = re.search(r'\[(\d+)BPM\s+([A-G][#b]?)\s+(Maj|Min)\]', stem)
    if match:
        bpm = int(match.group(1))
        note = match.group(2)
        mode = match.group(3)
        key = f"{note} {mode}"
        # Clean title — remove the bracket part and any old BPM notes
        title = re.sub(r'\s*\[\d+BPM.*?\]', '', stem).strip()
        title = re.sub(r'\s+\d+\s+[A-G][#b]?\s*(minor|major|min|maj)', '', title, flags=re.IGNORECASE).strip()
        title = title.rstrip()
    else:
        title = stem.strip()
        bpm = 0
        key = ''
    return title, bpm, key

def guess_genre(title, bpm, key):
    title_lower = title.lower()
    if any(w in title_lower for w in ['backwoods','dirt road','pickup truck','gravel','wire transfer','outlaw','small town','ramen','waffle house']):
        return 'Country Rap'
    if any(w in title_lower for w in ['chicago','windy city','block','bodies','gang','guns','fraud','brick']):
        return 'Trap'
    if any(w in title_lower for w in ['love','baby','angels','heaven','lonely','always tired','insecur','emotional','lovin']):
        return 'R&B'
    if any(w in title_lower for w in ['graduation','lessons','diary','greatness','ambition','mission','vision','never give up','winners']):
        return 'Motivational'
    if any(w in title_lower for w in ['moonlight','venice','hollywood','la','tokyo','dnd','lexus','gps','flight','places']):
        return 'Melodic'
    if bpm >= 130:
        return 'Drill'
    if bpm <= 85:
        return 'Lo-Fi'
    return 'Hip-Hop'

with app.app_context():
    db.create_all()
    files = sorted([f for f in os.listdir(WAV_SRC) if f.lower().endswith('.wav')])
    added = 0
    skipped = 0

    for filename in files:
        title, bpm, key = parse_filename(filename)
        genre = guess_genre(title, bpm, key)

        # Copy WAV file
        src_path = os.path.join(WAV_SRC, filename)
        safe_name = re.sub(r'[^\w\s\-\.]', '', filename).strip().replace(' ', '_')
        dest_path = os.path.join(WAV_DEST, safe_name)
        shutil.copy2(src_path, dest_path)
        wav_rel = f'beats/{safe_name}'

        # Check if already exists
        existing = Beat.query.filter_by(title=title).first()
        if existing:
            # Update existing
            existing.bpm = bpm
            existing.key = key
            existing.genre = genre
            existing.wav_path = wav_rel
            existing.is_active = True
            skipped += 1
            continue

        beat = Beat(
            title           = title,
            bpm             = bpm,
            key             = key,
            genre           = genre,
            mood            = '',
            tags            = '',
            price_basic     = 29,
            price_premium   = 49,
            price_trackout  = 99,
            price_exclusive = 299,
            wav_path        = wav_rel,
            mp3_path        = None,
            cover_path      = None,
            is_active       = True,
            is_featured     = False,
            is_free         = False,
        )
        db.session.add(beat)
        added += 1

        if added % 20 == 0:
            db.session.commit()
            print(f'  Saved {added} beats so far...')

    db.session.commit()
    print(f'\nDone!')
    print(f'  Added:   {added} new beats')
    print(f'  Updated: {skipped} existing beats')
    print(f'  Total:   {Beat.query.count()} beats in database')
    print(f'\nAll beats visible in Admin > Beats')
    print(f'Edit genre, mood, tags, pricing, featured status from admin panel')
