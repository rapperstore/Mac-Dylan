from flask import Blueprint, render_template
from models import Product, Album

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    ebook = Product.query.filter_by(name="The Artist Is The Business", is_active=True).first()
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    # Physical formats aren't for sale yet — the album shows as "coming soon"
    # in the store and links to the on-site player for streaming now.
    album = Album.query.filter_by(is_active=True).order_by(
        Album.sort_order.asc(), Album.created_at.desc()).first()
    return render_template('store.html',
        products=products,
        ebook=ebook,
        ebook_id=ebook.id if ebook else 1,
        album=album,
        album_tracks=len([t for t in album.tracks if t.is_active]) if album else 0
    )

@store_bp.route('/api/products')
def api_products():
    products = Product.query.filter_by(is_active=True).all()
    return {'products': [{'id':p.id,'name':p.name,'price':p.price,'type':p.product_type} for p in products]}
