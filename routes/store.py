from flask import Blueprint, render_template
from database import db
from models import Product

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template('store.html', products=products)

@store_bp.route('/api/products')
def api_products():
    products = Product.query.filter_by(is_active=True).all()
    return {'products': [p.to_dict() for p in products]}
