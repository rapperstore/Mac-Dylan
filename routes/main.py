import urllib.request
import urllib.parse
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, Response
from database import db
from models import Beat, Credit, Subscriber

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    beats = Beat.query.filter_by(is_active=True, is_featured=True).limit(3).all()
    if not beats:
        beats = Beat.query.filter_by(is_active=True).limit(3).all()
    credits = Credit.query.filter_by(is_active=True).order_by(
        Credit.sort_order.asc(), Credit.created_at.desc()
    ).limit(12).all()
    return render_template('index.html', beats=beats, credits=credits)


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

    # Post to ConvertKit
    try:
        ck_data = urllib.parse.urlencode({'email_address': email}).encode('utf-8')
        req = urllib.request.Request(
            'https://mac-dylan.kit.com/b5923233e5/subscriptions',
            data=ck_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Don't fail the whole request if CK is down

    return jsonify({
        'ok': True,
        'code': 'MACDYLAN15',
        'beat_url': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Afterlife%20%5B117BPM%20A%23%20Min%5D.mp3',
        'beat_title': 'Afterlife'
    })


@main_bp.route('/sitemap.xml')
def sitemap():
    today = datetime.utcnow().strftime('%Y-%m-%d')
    pages = [
        ('https://www.macdylan.com/', '1.0', 'weekly'),
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


