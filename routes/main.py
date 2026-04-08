from flask import Blueprint, render_template
from models import Beat, Product, Content, Credit

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_beats = Beat.query.filter_by(is_active=True, is_featured=True).limit(3).all()
    credits = Credit.query.filter_by(is_active=True).order_by(Credit.sort_order.asc(), Credit.created_at.desc()).limit(12).all()
    return render_template('index.html', beats=featured_beats, credits=credits)

@main_bp.route('/success')
def success():
    return render_template('success.html')
