import re
import uuid
import json
import urllib.request
import urllib.parse
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, Response, current_app, make_response
from database import db
from models import Beat, Credit, Subscriber, PhoneLead, PromoLead, Album, Track, Post, PostLike

VISITOR_COOKIE = 'md_visitor'


def _visitor_token():
    """Anonymous per-browser id used to keep likes honest. No PII."""
    return request.cookies.get(VISITOR_COOKIE) or ''

main_bp = Blueprint('main', __name__)

# Videos from the "Mac Dylan Credits" YouTube playlist, in playlist order.
# To update: edit this list (id = the 11-char YouTube video ID).
CREDIT_VIDEOS = [
    {'id': 'NtY2Zs8azMM', 'title': 'On My Momma',                                      'duration': '2:38'},
    {'id': 'mMGLBQf75jg', 'title': 'LONDON — JWOKK ft. Uffy',                          'duration': '2:29'},
    {'id': 'NRIf3Tt0uSM', 'title': 'DIE RICH — JWOKK (Official Music Video)',          'duration': '2:16'},
    {'id': 'aHy8ke4QIo0', 'title': 'Legendary (Official Music Video)',                 'duration': '3:18'},
    {'id': 'v20DZI7VIs0', 'title': 'Reflect (Official Music Video)',                   'duration': '3:07'},
    {'id': 'DLIzWG9WBF4', 'title': 'Dreams',                                           'duration': '3:36'},
    {'id': '6eFsrzzbtUg', 'title': 'Regardless feat. Poontz',                          'duration': '2:47'},
    {'id': '7GKo-8kT65k', 'title': 'Red Flag',                                          'duration': '3:55'},
    {'id': 'y4ECD7uWz7k', 'title': 'Ishan Tha Alchemist — Optimal',                    'duration': '3:37'},
    {'id': 'fyoL2yBeSW8', 'title': 'sngcash — "Bad and Boujee" Remix',                 'duration': '3:59'},
    {'id': 'UrfwQ4GuwT8', 'title': 'Augi Raps — When Its Cold ft. Pharoh Mind',        'duration': '3:12'},
    {'id': 'wqqXJgRDp-E', 'title': 'Augi Raps — Future (Official Video)',              'duration': '2:47'},
    {'id': 'mA8_krpncAY', 'title': '"Where You Been" by J Dixon',                      'duration': '2:22'},
    {'id': 'cecqgW5VBEg', 'title': '"Sharpen My Craft"',                               'duration': '3:44'},
    {'id': 'CjDM3AO8neM', 'title': 'J Dixon — "Care Less" (Official Music Video)',     'duration': '3:18'},
    {'id': 'huiqS9Yw74M', 'title': 'B 4 I Blow 2 (Intro)',                             'duration': '3:03'},
    {'id': 'm-WIyY3gzmE', 'title': 'J Dixon — "In Dat Mode"',                          'duration': '2:40'},
]


@main_bp.route('/')
def index():
    beats = Beat.query.filter_by(is_active=True, is_featured=True).limit(3).all()
    if not beats:
        beats = Beat.query.filter_by(is_active=True).limit(3).all()
    credits = Credit.query.filter_by(is_active=True).order_by(
        Credit.sort_order.asc(), Credit.created_at.desc()
    ).limit(12).all()
    # New Release card — latest active album, links to /stream/
    new_release = Album.query.filter_by(is_active=True).order_by(
        Album.sort_order.asc(), Album.created_at.desc()).first()
    new_release_tracks = len([t for t in new_release.tracks if t.is_active]) if new_release else 0

    # Homepage shows a hand-picked 5 from the playlist; full set lives on YouTube
    home_ids = ['NtY2Zs8azMM',  # On My Momma
                'NRIf3Tt0uSM',  # DIE RICH
                'v20DZI7VIs0',  # Reflect
                'fyoL2yBeSW8',  # Bad and Boujee remix
                'cecqgW5VBEg']  # Sharpen My Craft
    by_id = {v['id']: v for v in CREDIT_VIDEOS}
    home_videos = [by_id[i] for i in home_ids if i in by_id]

    # Timeline — pinned first, then newest. Mark which ones this visitor liked.
    posts = Post.query.filter_by(is_published=True).order_by(
        Post.is_pinned.desc(), Post.created_at.desc()).limit(10).all()
    token = _visitor_token()
    liked_ids = set()
    if token and posts:
        liked_ids = {l.post_id for l in PostLike.query.filter(
            PostLike.visitor == token,
            PostLike.post_id.in_([p.id for p in posts])).all()}

    return render_template('index.html', beats=beats, credits=credits,
                           new_release=new_release, new_release_tracks=new_release_tracks,
                           videos=home_videos, posts=posts, liked_ids=liked_ids)


@main_bp.route('/stream/')
def stream():
    albums = Album.query.filter_by(is_active=True).order_by(
        Album.sort_order.asc(), Album.created_at.desc()
    ).all()
    singles = Track.query.filter_by(album_id=None, is_active=True).order_by(
        Track.created_at.desc()
    ).all()
    music = []
    music_data = []
    for a in albums:
        tracks = [t for t in sorted(a.tracks, key=lambda x: (x.track_number or 0)) if t.is_active]
        if tracks:
            music.append({'album': a, 'tracks': tracks})
            music_data.append({
                'id': a.id, 'title': a.title, 'year': a.year or '',
                'cover_url': a.cover_url or '', 'price': a.price or 0,
                'description': a.description or '',
                'tracks': [{
                    'id': t.id, 'title': t.title, 'audio_url': t.audio_url or '',
                    'cover_url': t.cover_url or a.cover_url or '', 'price': t.price or 0,
                    'duration': t.duration or '', 'album_title': a.title
                } for t in tracks]
            })
    return render_template('stream.html', music=music, music_data=music_data, singles=singles)


@main_bp.route('/timeline/<int:post_id>/like', methods=['POST'])
def toggle_like(post_id):
    """Like/unlike a post. Anonymous — identified only by a random cookie."""
    post = Post.query.get(post_id)
    if not post or not post.is_published:
        return jsonify({'ok': False, 'error': 'Post not found'}), 404

    token = _visitor_token()
    new_token = False
    if not token:
        token = uuid.uuid4().hex
        new_token = True

    existing = PostLike.query.filter_by(post_id=post_id, visitor=token).first()
    try:
        if existing:
            db.session.delete(existing)
            liked = False
        else:
            db.session.add(PostLike(post_id=post_id, visitor=token))
            liked = True
        db.session.commit()
    except Exception:
        db.session.rollback()
        liked = existing is None

    count = PostLike.query.filter_by(post_id=post_id).count()
    resp = make_response(jsonify({'ok': True, 'liked': liked, 'count': count}))
    if new_token:
        # 1 year, lax — enough to remember a like without tracking anyone
        resp.set_cookie(VISITOR_COOKIE, token, max_age=31536000,
                        samesite='Lax', secure=request.is_secure)
    return resp


@main_bp.route('/music/play/<int:track_id>', methods=['POST'])
def music_play(track_id):
    t = Track.query.get(track_id)
    if t:
        t.play_count = (t.play_count or 0) + 1
        db.session.commit()
    return jsonify({'ok': True})


@main_bp.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    if not email:
        return jsonify({'ok': False, 'error': 'Email required'}), 400

    # Save to local DB (handle duplicate gracefully)
    try:
        existing = Subscriber.query.filter_by(email=email).first()
        if not existing:
            sub = Subscriber(email=email, source='homepage')
            db.session.add(sub)
            db.session.commit()
    except Exception:
        db.session.rollback()

    # Post to Kit (formerly ConvertKit) via official v4 API
    ck_ok = False
    try:
        form_id = current_app.config.get('CONVERTKIT_FORM_ID')
        api_key = current_app.config.get('CONVERTKIT_API_KEY')
        if form_id and api_key:
            ck_payload = json.dumps({'email_address': email}).encode('utf-8')
            req = urllib.request.Request(
                f'https://api.kit.com/v4/forms/{form_id}/subscribers',
                data=ck_payload,
                headers={
                    'Content-Type': 'application/json',
                    'X-Kit-Api-Key': api_key
                }
            )
            with urllib.request.urlopen(req, timeout=5) as ck_resp:
                if ck_resp.status in (200, 201):
                    ck_ok = True
        else:
            current_app.logger.warning('Kit not configured: missing form_id or api_key')
    except Exception as e:
        current_app.logger.error(f'Kit subscribe failed: {e}')
        ck_error_debug = str(e)
    else:
        ck_error_debug = None

    return jsonify({
        'ok': True,
        'ck_ok': ck_ok,
        'ck_error_debug': locals().get('ck_error_debug'),
        'code': 'MACDYLAN15',
        'beat_url': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Afterlife%20%5B117BPM%20A%23%20Min%5D.mp3',
        'beat_title': 'Afterlife'
    })


@main_bp.route('/free-beat', methods=['POST'])
def free_beat():
    data = request.get_json() or {}
    raw_phone = (data.get('phone') or '').strip()
    beat_id   = data.get('beat_id')

    # Normalize to digits only, then E.164
    digits = re.sub(r'\D', '', raw_phone)
    if len(digits) == 10:
        digits = '1' + digits
    if len(digits) != 11 or digits[0] != '1':
        return jsonify({'ok': False, 'error': 'Enter a valid US phone number'}), 400
    phone = '+' + digits

    # One free beat per phone number
    if PhoneLead.query.filter_by(phone=phone).first():
        return jsonify({'ok': False, 'error': 'This number has already claimed a free beat'}), 400

    # Look up the beat
    beat = Beat.query.get(beat_id) if beat_id else None
    if not beat or not beat.is_active:
        return jsonify({'ok': False, 'error': 'Beat not found'}), 400

    lead = PhoneLead(
        phone=phone,
        beat_id=beat.id,
        beat_title=beat.title,
        beat_url=beat.mp3_path,
    )
    db.session.add(lead)

    sms_sent = False
    sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_num = current_app.config.get('TWILIO_FROM_NUMBER')

    if sid and token and from_num:
        try:
            from twilio.rest import Client
            msg = (
                f"Mac Dylan here! Your free beat is ready:\n\n"
                f"🎵 {beat.title}\n"
                f"{beat.mp3_path}\n\n"
                f"License it at macdylan.com/beats 🔥"
            )
            Client(sid, token).messages.create(body=msg, from_=from_num, to=phone)
            lead.sms_sent = True
            sms_sent = True
        except Exception as e:
            current_app.logger.error(f'Twilio error: {e}')

    db.session.commit()

    return jsonify({
        'ok': True,
        'sms_sent': sms_sent,
        'beat_title': beat.title,
        'beat_url': beat.mp3_path,
    })


@main_bp.route('/promo/bogo-signup', methods=['POST'])
def bogo_signup():
    data = request.get_json() or {}
    raw_phone = (data.get('phone') or '').strip()

    digits = re.sub(r'\D', '', raw_phone)
    if len(digits) == 10:
        digits = '1' + digits
    if len(digits) != 11 or digits[0] != '1':
        return jsonify({'ok': False, 'error': 'Enter a valid US phone number'}), 400
    phone = '+' + digits

    existing = PromoLead.query.filter_by(phone=phone).first()
    if existing:
        return jsonify({'ok': False, 'error': 'This number has already claimed the BOGO deal'}), 400

    lead = PromoLead(phone=phone, promo_code='BOGO2026')
    db.session.add(lead)

    sms_sent = False
    sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_num = current_app.config.get('TWILIO_FROM_NUMBER')

    if sid and token and from_num:
        try:
            from twilio.rest import Client
            msg = (
                f"Mac Dylan here! You're locked in for the BOGO deal \u2014 "
                f"buy one mix and master, get your second one FREE.\n\n"
                f"Your code: BOGO2026\n\n"
                f"Mention this code when you book at macdylan.com/services \ud83d\udd25"
            )
            Client(sid, token).messages.create(body=msg, from_=from_num, to=phone)
            lead.sms_sent = True
            sms_sent = True
        except Exception as e:
            current_app.logger.error(f'Twilio error: {e}')

    db.session.commit()

    return jsonify({
        'ok': True,
        'sms_sent': sms_sent,
        'promo_code': lead.promo_code,
    })


@main_bp.route('/debug-ck-key')
def debug_ck_key():
    api_key = current_app.config.get('CONVERTKIT_API_KEY') or ''
    form_id = current_app.config.get('CONVERTKIT_FORM_ID') or ''
    info = {
        'key_len': len(api_key),
        'key_first4': api_key[:4],
        'key_last4': api_key[-4:] if len(api_key) >= 4 else api_key,
        'has_whitespace': api_key != api_key.strip(),
        'form_id': form_id
    }
    try:
        req = urllib.request.Request(
            'https://api.kit.com/v4/account',
            headers={'X-Kit-Api-Key': api_key.strip()}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            info['account_check_status'] = resp.status
            info['account_check_body'] = resp.read().decode('utf-8')[:300]
    except Exception as e:
        info['account_check_error'] = str(e)
    return jsonify(info)


@main_bp.route('/sitemap.xml')
def sitemap():
    today = datetime.utcnow().strftime('%Y-%m-%d')
    pages = [
        ('https://www.macdylan.com/', '1.0', 'weekly'),
        ('https://www.macdylan.com/stream/', '0.9', 'weekly'),
        ('https://www.macdylan.com/beats/', '0.9', 'daily'),
        ('https://www.macdylan.com/services/', '0.9', 'monthly'),
        ('https://www.macdylan.com/store/', '0.9', 'weekly'),
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority, freq in pages:
        xml += f'  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{freq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')


@main_bp.route('/google35cbc8a6f0798c76.html')
def google_verify():
    return Response('google-site-verification: google35cbc8a6f0798c76.html', mimetype='text/html')


@main_bp.route('/robots.txt')
def robots():
    txt = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /admin/\n'
        'Disallow: /payments/\n'
        '\n'
        'Sitemap: https://www.macdylan.com/sitemap.xml\n'
    )
    return Response(txt, mimetype='text/plain')


