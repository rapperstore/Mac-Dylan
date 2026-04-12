import os
import stripe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]
    for folder in [app.config["UPLOAD_FOLDER"],app.config["DOWNLOAD_FOLDER"],
                   os.path.join(app.config["UPLOAD_FOLDER"],"beats"),
                   os.path.join(app.config["UPLOAD_FOLDER"],"covers"),
                   os.path.join(app.config["UPLOAD_FOLDER"],"products")]:
        os.makedirs(folder,exist_ok=True)
    from routes.main     import main_bp
    from routes.beats    import beats_bp
    from routes.services import services_bp
    from routes.store    import store_bp
    from routes.payments import payments_bp
    from routes.admin    import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(beats_bp,url_prefix="/beats")
    app.register_blueprint(services_bp,url_prefix="/services")
    app.register_blueprint(store_bp,url_prefix="/store")
    app.register_blueprint(payments_bp,url_prefix="/payments")
    app.register_blueprint(admin_bp,url_prefix="/admin")
    with app.app_context():
        db.create_all()
        from models import Product
        try:
            if not Product.query.filter_by(name="The Artist Is The Business").first():
                db.session.add(Product(product_type="digital",
                    name="The Artist Is The Business",
                    description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan.",
                    price=27,tags="ebook,artist development,strategy",
                    file_path="uploads/products/artist-is-the-business-v2.html",
                    is_active=True,is_new=True))
                db.session.commit()
        except Exception:
            db.session.rollback()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,port=5000)
