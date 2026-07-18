from datetime import datetime
from database import db


class Beat(db.Model):
    __tablename__ = 'beats'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(120), nullable=False)
    bpm             = db.Column(db.Integer)
    key             = db.Column(db.String(20))
    genre           = db.Column(db.String(50))
    mood            = db.Column(db.String(50))
    tags            = db.Column(db.String(200))

    # Pricing — all start at $29 basic
    price_basic     = db.Column(db.Integer, default=29)   # dollars
    price_premium   = db.Column(db.Integer, default=49)
    price_trackout  = db.Column(db.Integer, default=99)
    price_exclusive = db.Column(db.Integer, default=299)

    # File paths (relative to static/)
    mp3_path        = db.Column(db.String(300))   # preview
    wav_path        = db.Column(db.String(300))   # premium + trackout
    stems_path      = db.Column(db.String(300))   # trackout + exclusive (zip)
    cover_path      = db.Column(db.String(300))   # cover art

    # Stats
    play_count      = db.Column(db.Integer, default=0)
    sale_count      = db.Column(db.Integer, default=0)

    # Flags
    is_active       = db.Column(db.Boolean, default=True)
    is_featured     = db.Column(db.Boolean, default=False)
    is_free         = db.Column(db.Boolean, default=False)

    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':              self.id,
            'title':           self.title,
            'bpm':             self.bpm,
            'key':             self.key,
            'genre':           self.genre,
            'mood':            self.mood,
            'tags':            self.tags,
            'price_basic':     self.price_basic,
            'price_premium':   self.price_premium,
            'price_trackout':  self.price_trackout,
            'price_exclusive': self.price_exclusive,
            'mp3_path':        self.mp3_path,
            'cover_path':      self.cover_path,
            'play_count':      self.play_count,
            'sale_count':      self.sale_count,
            'is_active':       self.is_active,
            'is_featured':     self.is_featured,
            'is_free':         self.is_free,
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id                = db.Column(db.Integer, primary_key=True)
    order_type        = db.Column(db.String(20))     # 'beat', 'session', 'store'
    customer_email    = db.Column(db.String(120))
    customer_name     = db.Column(db.String(120))
    product_name      = db.Column(db.String(300))
    license_type      = db.Column(db.String(50))     # beat orders only
    amount_total      = db.Column(db.Integer)        # cents
    amount_paid       = db.Column(db.Integer)        # cents
    amount_balance    = db.Column(db.Integer, default=0)  # session balance due
    stripe_session_id = db.Column(db.String(200))
    status            = db.Column(db.String(30), default='pending')
    # 'pending' → 'paid' → 'complete' / 'refunded'
    notes             = db.Column(db.Text)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':             self.id,
            'order_type':     self.order_type,
            'email':          self.customer_email,
            'name':           self.customer_name,
            'product':        self.product_name,
            'license':        self.license_type,
            'total':          self.amount_total,
            'paid':           self.amount_paid,
            'balance':        self.amount_balance,
            'status':         self.status,
            'date':           self.created_at.strftime('%Y-%m-%d'),
        }


class Product(db.Model):
    __tablename__ = 'products'

    id            = db.Column(db.Integer, primary_key=True)
    product_type  = db.Column(db.String(20))   # 'digital', 'merch', 'course'
    name          = db.Column(db.String(200),  nullable=False)
    description   = db.Column(db.Text)
    price         = db.Column(db.Integer)       # dollars
    tags          = db.Column(db.String(200))
    image_path    = db.Column(db.String(300))
    file_path     = db.Column(db.String(300))  # digital download
    printful_id   = db.Column(db.String(100))  # Printful variant ID (merch)
    sizes         = db.Column(db.String(100))  # e.g. "S,M,L,XL,2XL"
    is_active     = db.Column(db.Boolean, default=True)
    is_new        = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'type':         self.product_type,
            'name':         self.name,
            'description':  self.description,
            'price':        self.price,
            'tags':         self.tags.split(',') if self.tags else [],
            'image_path':   self.image_path,
            'file_path':    self.file_path,
            'printful_id':  self.printful_id,
            'sizes':        self.sizes.split(',') if self.sizes else [],
            'is_active':    self.is_active,
            'is_new':       self.is_new,
        }


class Content(db.Model):
    __tablename__ = 'content'

    id           = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20))   # 'video', 'post', 'announcement'
    title        = db.Column(db.String(200),  nullable=False)
    body         = db.Column(db.Text)
    embed_url    = db.Column(db.String(500))  # YouTube/SoundCloud embed src
    thumb_path   = db.Column(db.String(300))
    video_path   = db.Column(db.String(300))
    is_published = db.Column(db.Boolean, default=True)
    is_featured  = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

class Credit(db.Model):
    __tablename__ = 'credits'
    id         = db.Column(db.Integer, primary_key=True)
    artist     = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(100))
    track_name = db.Column(db.String(200))
    year       = db.Column(db.String(10))
    is_active  = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    source      = db.Column(db.String(50), default='homepage')  # 'homepage', 'beat_purchase', 'ebook_purchase'
    reward_sent = db.Column(db.Boolean, default=False)
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class PhoneLead(db.Model):
    __tablename__ = 'phone_leads'
    id         = db.Column(db.Integer, primary_key=True)
    phone      = db.Column(db.String(20), unique=True, nullable=False)
    beat_id    = db.Column(db.Integer, db.ForeignKey('beats.id'), nullable=True)
    beat_title = db.Column(db.String(120))
    beat_url   = db.Column(db.String(500))
    sms_sent   = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
