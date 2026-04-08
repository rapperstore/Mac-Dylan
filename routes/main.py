from flask import Blueprint, render_template
from models import Beat, Product, Content

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    featured_beats   = Beat.query.filter_by(is_active=True, is_featured=True).limit(3).all()
    featured_content = Content.query.filter_by(is_published=True, is_featured=True).limit(2).all()
    return render_template('index.html',
                           beats=featured_beats,
                           content=featured_content)


@main_bp.route('/success')
def success():
    return render_template('success.html')
