from flask import Blueprint, render_template, jsonify, request
from database import db
from models import Beat

beats_bp = Blueprint('beats', __name__)


@beats_bp.route('/')
def index():
    beats = Beat.query.filter_by(is_active=True).order_by(Beat.is_free.desc(), Beat.created_at.desc()).all()
    return render_template('beats.html', beats=beats)


@beats_bp.route('/api/all')
def api_all():
    """Returns all active beats as JSON — used by the frontend JS player."""
    beats = Beat.query.filter_by(is_active=True).order_by(Beat.is_free.desc(), Beat.created_at.desc()).all()
    return jsonify([b.to_dict() for b in beats])


@beats_bp.route('/api/play/<int:beat_id>', methods=['POST'])
def track_play(beat_id):
    """Increments play count each time a beat is previewed."""
    beat = Beat.query.get_or_404(beat_id)
    beat.play_count += 1
    db.session.commit()
    return jsonify({'play_count': beat.play_count})
