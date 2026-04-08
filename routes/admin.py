import os
import hmac
import hashlib
from functools import wraps
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, jsonify, current_app, Response)
from werkzeug.utils import secure_filename
from database import db
from models import Beat, Order, Product, Content

admin_bp = Blueprint('admin', __name__)


# ── AUTH ──────────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        expected = current_app.config.get('ADMIN_PASSWORD', '')
        if hmac.compare_digest(password, expected):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        error = 'Incorrect password'
    return render_template('admin/login.html', error=error)


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


# ── DASHBOARD ─────────────────────────────────────────────────
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    revenue    = (db.session.query(db.func.sum(Order.amount_paid))
                  .filter_by(status='paid').scalar() or 0) / 100
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    beats      = Beat.query.order_by(Beat.play_count.desc()).all()
    products   = Product.query.filter_by(is_active=True).all()

    # Check Stripe key looks valid
    sk = current_app.config.get('STRIPE_SECRET_KEY', '')
    stripe_ok = sk and (sk.startswith('sk_test_') or sk.startswith('sk_live_'))

    return render_template('admin/dashboard.html',
        revenue        = revenue,
        orders_count   = len(all_orders),
        beats_count    = Beat.query.filter_by(is_active=True).count(),
        products_count = len(products),
        recent_orders  = all_orders[:8],
        all_orders     = all_orders,
        beats          = beats,
        products       = products,
        stripe_ok      = stripe_ok,
        domain         = current_app.config.get('DOMAIN', 'http://localhost:5000'),
    )


# ── API STATS ─────────────────────────────────────────────────
@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    revenue  = (db.session.query(db.func.sum(Order.amount_paid))
                .filter_by(status='paid').scalar() or 0) / 100
    return jsonify({
        'revenue':  revenue,
        'orders':   Order.query.count(),
        'pending':  Order.query.filter_by(status='pending').count(),
        'plays':    db.session.query(db.func.sum(Beat.play_count)).scalar() or 0,
        'products': Product.query.filter_by(is_active=True).count(),
        'sessions': Order.query.filter_by(order_type='session').count(),
    })


# ── ORDERS ────────────────────────────────────────────────────
@admin_bp.route('/orders/<int:order_id>/complete', methods=['POST'])
@admin_required
def complete_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'complete'
    db.session.commit()
    return jsonify({'status': 'complete'})


@admin_bp.route('/orders/export')
@admin_required
def export_orders():
    import csv, io
    orders = Order.query.order_by(Order.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID','Date','Type','Email','Name','Product','License',
                     'Total','Paid','Balance','Status'])
    for o in orders:
        writer.writerow([
            o.id, o.created_at.strftime('%Y-%m-%d'), o.order_type,
            o.customer_email, o.customer_name, o.product_name, o.license_type,
            o.amount_total/100, o.amount_paid/100, o.amount_balance/100, o.status
        ])
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=orders.csv'}
    )


# ── BEATS ─────────────────────────────────────────────────────
def _save_file(file_key, subfolder, allowed_exts):
    """Save an uploaded file and return its relative path, or None."""
    f = request.files.get(file_key)
    if not f or not f.filename:
        return None
    ext = f.filename.rsplit('.', 1)[-1].lower()
    if ext not in allowed_exts:
        return None
    fname   = secure_filename(f.filename)
    dirpath = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(dirpath, exist_ok=True)
    f.save(os.path.join(dirpath, fname))
    return os.path.join(subfolder, fname)


@admin_bp.route('/beats/upload', methods=['POST'])
@admin_required
def upload_beat():
    try:
        is_free = 'free' in request.form
        beat = Beat(
            title           = request.form.get('title', '').strip(),
            bpm             = int(request.form.get('bpm', 0) or 0),
            key             = request.form.get('key', '').strip(),
            genre           = request.form.get('genre', '').strip(),
            mood            = request.form.get('mood', '').strip(),
            tags            = request.form.get('tags', '').strip(),
            price_basic     = int(request.form.get('price_basic',    29) or 29),
            price_premium   = int(request.form.get('price_premium',  49) or 49),
            price_trackout  = int(request.form.get('price_trackout', 99) or 99),
            price_exclusive = int(request.form.get('price_exclusive',299)or 299),
            is_active       = 'active'   in request.form,
            is_featured     = 'featured' in request.form,
            is_free         = is_free,
            mp3_path        = _save_file('mp3_preview','beats', {'mp3','wav'}),
            wav_path        = _save_file('wav_file',   'beats', {'wav','aiff'}),
            stems_path      = _save_file('stems_file', 'beats', {'zip'}),
            cover_path      = _save_file('cover_art',  'covers',{'jpg','jpeg','png','webp'}),
        )
        db.session.add(beat)
        db.session.commit()
        return jsonify({'success': True, 'beat_id': beat.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@admin_bp.route('/beats/<int:beat_id>/toggle', methods=['POST'])
@admin_required
def toggle_beat(beat_id):
    beat = Beat.query.get_or_404(beat_id)
    beat.is_active = not beat.is_active
    db.session.commit()
    return jsonify({'is_active': beat.is_active})


@admin_bp.route('/beats/<int:beat_id>/delete', methods=['POST'])
@admin_required
def delete_beat(beat_id):
    beat = Beat.query.get_or_404(beat_id)
    db.session.delete(beat)
    db.session.commit()
    return jsonify({'deleted': True})


# ── PRODUCTS ──────────────────────────────────────────────────
@admin_bp.route('/products/add', methods=['POST'])
@admin_required
def add_product():
    try:
        product = Product(
            product_type = request.form.get('type', 'digital'),
            name         = request.form.get('name', '').strip(),
            description  = request.form.get('description', '').strip(),
            price        = int(float(request.form.get('price', 0) or 0)),
            tags         = request.form.get('tags', '').strip(),
            is_active    = 'active' in request.form,
            is_new       = 'is_new' in request.form,
            file_path    = _save_file('file',  'products', {'zip','pdf','mp3','wav','aiff'}),
            image_path   = _save_file('image', 'products', {'jpg','jpeg','png','webp'}),
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'success': True, 'product_id': product.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'deleted': True})
