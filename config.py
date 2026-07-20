import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Flask ──
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-insecure-fallback-change-this')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

    # ── Database ──
    # SQLite locally, PostgreSQL on Railway (DATABASE_URL auto-set by Railway)
    raw_db = os.environ.get('DATABASE_URL', '')
    if raw_db.startswith('postgres://'):
        raw_db = raw_db.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = raw_db or 'sqlite:////tmp/macdylan.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Static asset caching (30 days) ──
    SEND_FILE_MAX_AGE_DEFAULT = 2592000

    # ── Analytics ──
    GA_MEASUREMENT_ID = os.environ.get('GA_MEASUREMENT_ID')  # e.g. G-XXXXXXXXXX

    # ── Stripe ──
    STRIPE_SECRET_KEY      = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET  = os.environ.get('STRIPE_WEBHOOK_SECRET')

    # ── Printful ──
    PRINTFUL_API_KEY = os.environ.get('PRINTFUL_API_KEY')

    # ── ConvertKit ──
    CONVERTKIT_FORM_ID = os.environ.get('CONVERTKIT_FORM_ID', '9292507')

    # ── Cloudflare R2 (private buckets → presigned download URLs) ──
    R2_ACCOUNT_ID        = os.environ.get('R2_ACCOUNT_ID')
    R2_ACCESS_KEY_ID     = os.environ.get('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    R2_DOWNLOADS_BUCKET  = os.environ.get('R2_DOWNLOADS_BUCKET', 'digitaldownloads')
    R2_LINK_TTL          = int(os.environ.get('R2_LINK_TTL', 900))  # seconds

    # ── Twilio (SMS) ──
    TWILIO_ACCOUNT_SID  = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN   = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_FROM_NUMBER  = os.environ.get('TWILIO_FROM_NUMBER')  # e.g. +12085551234

    # ── Domain (used in Stripe success/cancel URLs) ──
    DOMAIN = os.environ.get('DOMAIN', 'http://localhost:5000')

    # ── File uploads ──
    UPLOAD_FOLDER   = os.path.join('static', 'uploads')
    DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB

    ALLOWED_AUDIO = {'mp3', 'wav', 'aiff', 'flac'}
    ALLOWED_IMAGE = {'jpg', 'jpeg', 'png', 'webp'}
    ALLOWED_FILE  = {'zip', 'pdf', 'mp3', 'wav', 'aiff'}
