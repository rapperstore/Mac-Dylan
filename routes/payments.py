import stripe
import json
from flask import Blueprint, request, jsonify, render_template, current_app, redirect, abort, url_for
from database import db
from models import Order, Beat, Product, Album, Track

payments_bp = Blueprint('payments', __name__)


def get_domain():
    return current_app.config.get('DOMAIN', 'http://localhost:5000')


def r2_presigned_url(key, bucket=None, ttl=None):
    """Short-lived download link for an object in a PRIVATE R2 bucket.

    Keeps paid products unreachable by URL-sharing: the link expires and is
    only ever minted after a purchase has been verified. Returns None when R2
    credentials aren't configured so callers can degrade gracefully.
    """
    cfg = current_app.config
    account = cfg.get('R2_ACCOUNT_ID')
    akid = cfg.get('R2_ACCESS_KEY_ID')
    secret = cfg.get('R2_SECRET_ACCESS_KEY')
    if not (account and akid and secret):
        return None
    try:
        import boto3
        from botocore.config import Config as BotoConfig
        client = boto3.client(
            's3',
            endpoint_url='https://%s.r2.cloudflarestorage.com' % account,
            aws_access_key_id=akid,
            aws_secret_access_key=secret,
            config=BotoConfig(signature_version='s3v4'),
            region_name='auto',
        )
        return client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket or cfg.get('R2_DOWNLOADS_BUCKET'), 'Key': key},
            ExpiresIn=int(ttl or cfg.get('R2_LINK_TTL', 900)),
        )
    except Exception as e:
        current_app.logger.error('R2 presign failed for %s: %s' % (key, e))
        return None


@payments_bp.route('/download/<session_id>')
def download(session_id):
    """Deliver a purchased digital product — only after verifying payment."""
    order = Order.query.filter_by(stripe_session_id=session_id).first()
    if not order:
        abort(404)

    # Re-check with Stripe rather than trusting our own row alone.
    paid = order.status == 'paid'
    if not paid:
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            paid = sess.get('payment_status') == 'paid'
            if paid:
                order.status = 'paid'
                order.amount_paid = order.amount_total
                order.amount_balance = 0
                db.session.commit()
        except Exception as e:
            current_app.logger.error('Download verify failed: %s' % e)
    if not paid:
        return render_template('download_error.html',
            message='This order has not been paid yet. If you just checked out, '
                    'give it a moment and refresh.'), 402

    product = None
    try:
        sess = stripe.checkout.Session.retrieve(session_id)
        pid = (sess.get('metadata') or {}).get('product_id')
        if pid:
            product = Product.query.get(int(pid))
    except Exception:
        pass
    if product is None and order.product_name:
        product = Product.query.filter_by(name=order.product_name).first()

    if not product or not product.file_path:
        return render_template('download_error.html',
            message='We could not locate your file. Email macdylan4ever@gmail.com '
                    'with your receipt and it will be sent straight over.'), 404

    # Full URL = public asset; bare key = object in the private R2 bucket.
    if product.file_path.startswith('http'):
        return redirect(product.file_path)
    url = r2_presigned_url(product.file_path)
    if not url:
        return render_template('download_error.html',
            message='Downloads are being set up. Email macdylan4ever@gmail.com '
                    'with your receipt and your file will be sent right away.'), 503
    return redirect(url)


@payments_bp.route('/beat-checkout', methods=['POST'])
def beat_checkout():
    data = request.get_json()
    beat_id = data.get('beat_id')
    license = data.get('license', 'basic')
    beat = Beat.query.get_or_404(beat_id)
    price_map = {
        'basic': beat.price_basic,
        'premium': beat.price_premium,
        'trackout': beat.price_trackout,
        'exclusive': beat.price_exclusive
    }
    amount = price_map.get(license, beat.price_basic)
    license_labels = {
        'basic': 'Basic Lease (MP3 only)',
        'premium': 'Premium Lease (WAV + MP3)',
        'trackout': 'Trackout Lease (WAV + Stems)',
        'exclusive': 'Exclusive Rights (WAV + Stems + Full Ownership)'
    }
    domain = get_domain()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_creation='always',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': beat.title + ' - ' + license_labels.get(license, 'Beat License'),
                        'description': 'Producer: Mac Dylan | ' + str(beat.bpm) + ' BPM | ' + (beat.key or ''),
                    },
                    'unit_amount': amount * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/beats/',
            metadata={
                'order_type': 'beat',
                'beat_id': str(beat_id),
                'beat_title': beat.title,
                'license': license,
                'mp3_url': beat.mp3_path or '',
            }
        )
        order = Order(
            order_type='beat',
            product_name=beat.title + ' - ' + license,
            license_type=license,
            amount_total=amount * 100,
            amount_paid=0,
            amount_balance=amount * 100,
            status='pending',
            stripe_session_id=session.id
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    service = data.get('service', 'Service')
    amount = int(data.get('amount', 0))
    order_type = data.get('order_type', 'session')
    domain = get_domain()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            billing_address_collection='required',
            customer_creation='always',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': service,
                        'description': 'Mac Dylan Professional Services',
                    },
                    'unit_amount': amount * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/services/',
            metadata={
                'order_type': order_type,
                'service': service,
            }
        )
        order = Order(
            order_type=order_type,
            product_name=service,
            amount_total=amount * 100,
            amount_paid=0,
            amount_balance=amount * 100,
            status='pending',
            stripe_session_id=session.id
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/store-checkout', methods=['POST'])
def store_checkout():
    data = request.get_json()
    product_id = data.get('product_id')
    product_name = data.get('product_name', 'Digital Product')
    price = int(data.get('price', 0))
    domain = get_domain()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_creation='always',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name,
                        'description': 'Mac Dylan Digital Product - Instant delivery after purchase',
                    },
                    'unit_amount': price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/store/',
            metadata={
                'order_type': 'digital',
                'product_id': str(product_id) if product_id else '',
                'product_name': product_name,
            }
        )
        order = Order(
            order_type='digital',
            product_name=product_name,
            amount_total=price * 100,
            amount_paid=0,
            amount_balance=price * 100,
            status='pending',
            stripe_session_id=session.id
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/music-checkout', methods=['POST'])
def music_checkout():
    data = request.get_json() or {}
    kind = data.get('kind')  # 'track' or 'album'
    item_id = data.get('id')
    domain = get_domain()
    try:
        if kind == 'album':
            item = Album.query.get(item_id)
            if not item or not item.price:
                return jsonify({'error': 'Album not available for purchase'}), 400
            name = item.title + ' (Full Album)'
            price = item.price
            desc = 'Mac Dylan — full album download. Delivered after purchase.'
        else:
            item = Track.query.get(item_id)
            if not item or not item.price:
                return jsonify({'error': 'Track not available for purchase'}), 400
            name = item.title + ' (Single)'
            price = item.price
            desc = 'Mac Dylan — track download. Delivered after purchase.'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_creation='always',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': name, 'description': desc},
                    'unit_amount': price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/#music',
            metadata={'order_type': 'music', 'music_kind': kind, 'item_id': str(item_id), 'item_name': name}
        )
        order = Order(order_type='music', product_name=name,
            amount_total=price * 100, amount_paid=0, amount_balance=price * 100,
            status='pending', stripe_session_id=session.id)
        db.session.add(order); db.session.commit()
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/tip', methods=['POST'])
def tip():
    data = request.get_json()
    amount = int(data.get('amount', 5))
    domain = get_domain()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_creation='always',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Tip for Mac Dylan - Thank you!'},
                    'unit_amount': amount * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/',
            metadata={'order_type': 'tip'}
        )
        order = Order(
            order_type='tip',
            product_name='Tip - $' + str(amount),
            amount_total=amount * 100,
            amount_paid=0,
            amount_balance=amount * 100,
            status='pending',
            stripe_session_id=session.id
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'checkout_url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/success')
def success():
    session_id = request.args.get('session_id')
    customer_email = ''
    product_name = ''
    download_url = None
    order_type = ''
    beat_mp3 = None
    license_type = ''
    order = None
    if session_id:
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            customer_email = (sess.get('customer_details') or {}).get('email', '') or ''
            meta = sess.get('metadata') or {}
            order_type = meta.get('order_type', '')
            product_name = meta.get('beat_title') or meta.get('service') or meta.get('product_name', 'Your Purchase')
            license_type = meta.get('license', '')
            beat_mp3 = meta.get('mp3_url', '')
            order = Order.query.filter_by(stripe_session_id=session_id).first()
            if order and sess.get('payment_status') == 'paid':
                order.status = 'paid'
                order.customer_email = customer_email
                order.amount_paid = order.amount_total
                order.amount_balance = 0
                db.session.commit()
                if customer_email:
                    try:
                        from models import Subscriber
                        existing = Subscriber.query.filter_by(email=customer_email).first()
                        if not existing:
                            sub = Subscriber(email=customer_email, source=order_type + '_purchase')
                            db.session.add(sub)
                            db.session.commit()
                    except Exception:
                        db.session.rollback()
            if order_type in ('digital', 'music') and meta.get('product_id'):
                p = Product.query.get(int(meta['product_id']))
                if p and p.file_path:
                    # Always route through the verified-download endpoint so the
                    # underlying file (private R2 object) is never exposed directly.
                    download_url = url_for('payments.download', session_id=session_id)
        except Exception as e:
            current_app.logger.error('Success page error: ' + str(e))
    return render_template('success.html',
        order=order,
        customer_email=customer_email,
        product_name=product_name,
        order_type=order_type,
        download_url=download_url,
        beat_mp3=beat_mp3,
        license_type=license_type
    )


@payments_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET', '')
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = json.loads(payload)
        if event['type'] == 'checkout.session.completed':
            sess = event['data']['object']
            order = Order.query.filter_by(stripe_session_id=sess['id']).first()
            if order:
                order.status = 'paid'
                order.customer_email = (sess.get('customer_details') or {}).get('email', '')
                order.amount_paid = order.amount_total
                order.amount_balance = 0
                db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'status': 'ok'})
