import stripe
import json
import hmac
import hashlib
from flask import Blueprint, request, jsonify, render_template, redirect, current_app
from database import db
from models import Order, Beat, Product

payments_bp = Blueprint('payments', __name__)


def get_domain():
    return current_app.config.get('DOMAIN', 'http://localhost:5000')


@payments_bp.route('/beat-checkout', methods=['POST'])
def beat_checkout():
    data    = request.get_json()
    beat_id = data.get('beat_id')
    license = data.get('license', 'basic')
    email   = data.get('email', '').strip()
    beat    = Beat.query.get_or_404(beat_id)
    price_map = {'basic': beat.price_basic, 'premium': beat.price_premium,
                 'trackout': beat.price_trackout, 'exclusive': beat.price_exclusive}
    amount = price_map.get(license, beat.price_basic)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=email or None,
        line_items=[{'price_data': {'currency': 'usd', 'unit_amount': amount * 100,
            'product_data': {'name': f'{beat.title} — {license.title()} Lease'}},
            'quantity': 1}],
        mode='payment',
        success_url=get_domain() + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=get_domain() + '/beats/',
        metadata={'order_type': 'beat', 'beat_id': str(beat_id),
                  'beat_title': beat.title, 'license': license}
    )
    return jsonify({'checkout_url': session.url})


@payments_bp.route('/checkout', methods=['POST'])
def service_checkout():
    data   = request.get_json()
    email  = data.get('email', '').strip()
    name   = data.get('name', '').strip()
    items  = data.get('items', [])
    total  = data.get('total', 0)
    is_dep = data.get('is_deposit', False)
    balance = round(total - data.get('charge', total), 2) if is_dep else 0
    line_items = [{'price_data': {'currency': 'usd',
        'unit_amount': int(float(i['price']) * 100),
        'product_data': {'name': i['name']}}, 'quantity': 1} for i in items]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=email or None,
        line_items=line_items,
        mode='payment',
        success_url=get_domain() + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=get_domain() + '/services',
        metadata={'order_type': 'session', 'customer_name': name,
                  'is_deposit': str(is_dep), 'balance_due': str(balance), 'total': str(total)}
    )
    return jsonify({'checkout_url': session.url})


@payments_bp.route('/store-checkout', methods=['POST'])
def store_checkout():
    data  = request.get_json()
    email = data.get('email', '').strip()
    items = data.get('items', [])
    line_items = [{'price_data': {'currency': 'usd',
        'unit_amount': int(float(i['price']) * 100),
        'product_data': {'name': i['name'], 'description': 'Digital download'}},
        'quantity': int(i.get('qty', 1))} for i in items]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=email or None,
        line_items=line_items,
        mode='payment',
        success_url=get_domain() + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=get_domain() + '/store',
        metadata={'order_type': 'store', 'items_count': str(len(items))}
    )
    return jsonify({'checkout_url': session.url})


@payments_bp.route('/tip', methods=['POST'])
def tip():
    data   = request.get_json()
    amount = int(float(data.get('amount', 5)))
    email  = data.get('email', '').strip()
    if amount < 1:
        return jsonify({'error': 'Invalid amount'}), 400
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=email or None,
        line_items=[{'price_data': {'currency': 'usd', 'unit_amount': amount * 100,
            'product_data': {'name': 'Tip — Mac Dylan',
            'description': 'Support independent music. Thank you.'}},
            'quantity': 1}],
        mode='payment',
        success_url=get_domain() + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=get_domain() + '/',
        metadata={'order_type': 'tip', 'amount': str(amount)}
    )
    return jsonify({'checkout_url': session.url})


@payments_bp.route('/success')
def success():
    session_id   = request.args.get('session_id', '')
    session_data = None
    if session_id:
        try:
            session_data = stripe.checkout.Session.retrieve(session_id)
        except Exception:
            pass
    return render_template('success.html', session=session_data)


@payments_bp.route('/webhook', methods=['POST'])
def webhook():
    payload    = request.data
    sig_header = request.headers.get('Stripe-Signature', '')
    secret     = current_app.config.get('STRIPE_WEBHOOK_SECRET', '')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return '', 400
    if event['type'] == 'checkout.session.completed':
        s    = event['data']['object']
        meta = s.get('metadata', {})
        order = Order(
            order_type=meta.get('order_type', 'unknown'),
            customer_email=s.get('customer_email', ''),
            customer_name=meta.get('customer_name', ''),
            product_name=meta.get('beat_title') or f"Order ({meta.get('order_type','')})",
            license_type=meta.get('license', ''),
            amount_total=s.get('amount_total', 0),
            amount_paid=s.get('amount_total', 0),
            stripe_session_id=s.get('id'),
            status='paid',
        )
        db.session.add(order)
        db.session.commit()
        print(f"\nPAYMENT: {order.customer_email} — {order.product_name}\n")
    return '', 200
