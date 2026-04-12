import sys
sys.path.insert(0, '.')
from app import create_app
from database import db
from models import Product
app = create_app()
with app.app_context():
    db.create_all()
    e = Product.query.filter_by(name="The Artist Is The Business").first()
    if e:
        e.price=27;e.is_active=True;e.is_new=True;e.product_type="digital"
        e.file_path="uploads/products/artist-is-the-business-v2.html"
        e.description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan. Interactive e-book with animated visuals and built-in action checklist."
        e.tags="ebook,artist development,branding,income,strategy"
        db.session.commit();print("Updated ID:",e.id)
    else:
        p=Product(product_type="digital",name="The Artist Is The Business",
            description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan. Interactive e-book with animated visuals and built-in action checklist.",
            price=27,tags="ebook,artist development,branding,income,strategy",
            file_path="uploads/products/artist-is-the-business-v2.html",
            is_active=True,is_new=True)
        db.session.add(p);db.session.commit();print("Created ID:",p.id)
    total=Product.query.filter_by(is_active=True,product_type='digital').count()
    print(f"Active digital products: {total}")
