from flask import Blueprint, render_template
from flask import current_app

services_bp = Blueprint('services', __name__)


@services_bp.route('/')
def index():
    stripe_pk = current_app.config.get('STRIPE_PUBLISHABLE_KEY', '')
    return render_template('services.html', stripe_pk=stripe_pk)
