from flask import Blueprint, render_template
from models import Product

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    ebook = Product.query.filter_by(name="The Artist Is The Business", is_active=True).first()
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template('store.html',
        products=products,
        ebook=ebook,
        ebook_id=ebook.id if ebook else 1
    )

@store_bp.route('/api/products')
def api_products():
    products = Product.query.filter_by(is_active=True).all()
    return {'products': [{'id':p.id,'name':p.name,'price':p.price,'type':p.product_type} for p in products]}
