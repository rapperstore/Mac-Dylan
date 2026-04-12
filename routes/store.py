from flask import Blueprint, render_template
from models import Product

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    digital = Product.query.filter_by(is_active=True, product_type='digital').order_by(Product.created_at.desc()).all()
    merch   = Product.query.filter_by(is_active=True, product_type='merch').order_by(Product.created_at.desc()).all()
    courses = Product.query.filter_by(is_active=True, product_type='course').order_by(Product.created_at.desc()).all()
    return render_template('store.html', digital=digital, merch=merch, courses=courses)

@store_bp.route('/api/products')
def api_products():
    products = Product.query.filter_by(is_active=True).all()
    return {'products': [{'id':p.id,'name':p.name,'price':p.price,'type':p.product_type} for p in products]}
