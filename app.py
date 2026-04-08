import os
import stripe
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from database import db
    db.init_app(app)

    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    for folder in [app.config['UPLOAD_FOLDER'],
                   app.config['DOWNLOAD_FOLDER'],
                   os.path.join(app.config['UPLOAD_FOLDER'], 'beats'),
                   os.path.join(app.config['UPLOAD_FOLDER'], 'covers'),
                   os.path.join(app.config['UPLOAD_FOLDER'], 'products')]:
        os.makedirs(folder, exist_ok=True)

    from routes.main     import main_bp
    from routes.beats    import beats_bp
    from routes.services import services_bp
    from routes.store    import store_bp
    from routes.payments import payments_bp
    from routes.admin    import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(beats_bp,    url_prefix='/beats')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(store_bp,    url_prefix='/store')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(admin_bp,    url_prefix='/admin')

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
