import os
import hmac
from functools import wraps
from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify,current_app
from werkzeug.utils import secure_filename
from app import db
from models import Beat,Order,Product,Content

admin_bp = Blueprint("admin",__name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args,**kwargs)
    return decorated

@admin_bp.route("/login",methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        password=request.form.get("password","")
        expected=current_app.config.get("ADMIN_PASSWORD","")
        if hmac.compare_digest(password,expected):
            session["admin_logged_in"]=True
            return redirect(url_for("admin.dashboard"))
        error="Incorrect password"
    return render_template("admin/login.html",error=error)

@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in",None)
    return redirect(url_for("admin.login"))

@admin_bp.route("/")
@admin_required
def dashboard():
    rev=db.session.query(db.func.sum(Order.amount_paid)).filter_by(status="paid").scalar() or 0
    return render_template("admin/dashboard.html",
        revenue=rev/100,orders_count=Order.query.count(),
        beats_count=Beat.query.filter_by(is_active=True).count(),
        products_count=Product.query.filter_by(is_active=True).count(),
        recent_orders=Order.query.order_by(Order.created_at.desc()).limit(10).all(),
        beats=Beat.query.order_by(Beat.play_count.desc()).limit(10).all())

@admin_bp.route("/api/stats")
@admin_required
def api_stats():
    rev=db.session.query(db.func.sum(Order.amount_paid)).filter_by(status="paid").scalar() or 0
    return jsonify({"revenue":rev/100,"orders":Order.query.count(),
        "pending":Order.query.filter_by(status="pending").count(),
        "plays":db.session.query(db.func.sum(Beat.play_count)).scalar() or 0,
        "products":Product.query.filter_by(is_active=True).count(),
        "sessions":Order.query.filter_by(order_type="session").count()})

@admin_bp.route("/orders")
@admin_required
def orders():
    t=request.args.get("type","all")
    q=Order.query.order_by(Order.created_at.desc())
    if t!="all": q=q.filter_by(order_type=t)
    return render_template("admin/orders.html",orders=q.all(),filter=t)

@admin_bp.route("/orders/<int:oid>/complete",methods=["POST"])
@admin_required
def complete_order(oid):
    o=Order.query.get_or_404(oid);o.status="complete";db.session.commit()
    return jsonify({"status":"complete"})

@admin_bp.route("/orders/export")
@admin_required
def export_orders():
    import csv,io
    from flask import Response
    rows=Order.query.order_by(Order.created_at.desc()).all()
    out=io.StringIO();w=csv.writer(out)
    w.writerow(["ID","Type","Email","Name","Product","License","Total","Paid","Balance","Status","Date"])
    for o in rows:
        w.writerow([o.id,o.order_type,o.customer_email,o.customer_name,o.product_name,
            o.license_type,o.amount_total/100,o.amount_paid/100,o.amount_balance/100,
            o.status,o.created_at.strftime("%Y-%m-%d")])
    return Response(out.getvalue(),mimetype="text/csv",
        headers={"Content-Disposition":"attachment; filename=orders.csv"})

@admin_bp.route("/beats")
@admin_required
def beats():
    return render_template("admin/beats.html",beats=Beat.query.order_by(Beat.created_at.desc()).all())

@admin_bp.route("/beats/api/list")
@admin_required
def beats_api_list():
    return jsonify([{"id":b.id,"title":b.title,"bpm":b.bpm,"key":b.key,
        "genre":b.genre,"mood":b.mood,"tags":b.tags,
        "price_basic":b.price_basic,"price_premium":b.price_premium,
        "price_trackout":b.price_trackout,"price_exclusive":b.price_exclusive,
        "is_active":b.is_active,"is_featured":b.is_featured,
        "mp3_path":b.mp3_path or "","wav_path":b.wav_path or ""}
        for b in Beat.query.order_by(Beat.created_at.desc()).all()])

@admin_bp.route("/beats/upload",methods=["POST"])
@admin_required
def upload_beat():
    def sf(k,s,e):
        f=request.files.get(k)
        if not f or not f.filename: return None
        if f.filename.rsplit(".",1)[-1].lower() not in e: return None
        n=secure_filename(f.filename)
        p=os.path.join(current_app.config["UPLOAD_FOLDER"],s,n)
        os.makedirs(os.path.dirname(p),exist_ok=True);f.save(p)
        return os.path.join(s,n)
    b=Beat(title=request.form.get("title","").strip(),
        bpm=int(request.form.get("bpm",0) or 0),key=request.form.get("key","").strip(),
        genre=request.form.get("genre","").strip(),mood=request.form.get("mood","").strip(),
        tags=request.form.get("tags","").strip(),
        price_basic=int(request.form.get("price_basic",29) or 29),
        price_premium=int(request.form.get("price_premium",49) or 49),
        price_trackout=int(request.form.get("price_trackout",99) or 99),
        price_exclusive=int(request.form.get("price_exclusive",299) or 299),
        is_active=request.form.get("active")=="1",
        is_featured=request.form.get("featured")=="1",
        is_free=request.form.get("free")=="1",
        mp3_path=sf("mp3_preview","beats",{"mp3","wav"}),
        wav_path=sf("wav_file","beats",{"wav","aiff"}),
        stems_path=sf("stems_file","beats",{"zip"}),
        cover_path=sf("cover_art","covers",{"jpg","jpeg","png","webp"}))
    db.session.add(b);db.session.commit()
    return jsonify({"success":True,"beat_id":b.id})

@admin_bp.route("/beats/<int:bid>/toggle",methods=["POST"])
@admin_required
def toggle_beat(bid):
    b=Beat.query.get_or_404(bid);b.is_active=not b.is_active;db.session.commit()
    return jsonify({"is_active":b.is_active})

@admin_bp.route("/beats/<int:bid>/delete",methods=["POST"])
@admin_required
def delete_beat(bid):
    b=Beat.query.get_or_404(bid);db.session.delete(b);db.session.commit()
    return jsonify({"deleted":True})

@admin_bp.route("/beats/<int:bid>/edit",methods=["POST"])
@admin_required
def edit_beat(bid):
    b=Beat.query.get_or_404(bid);d=request.get_json() or {}
    try:
        b.title=d.get("title",b.title).strip();b.bpm=int(d.get("bpm",b.bpm) or 0)
        b.key=d.get("key",b.key or "").strip();b.genre=d.get("genre",b.genre or "").strip()
        b.mood=d.get("mood",b.mood or "").strip();b.tags=d.get("tags",b.tags or "").strip()
        b.price_basic=int(d.get("price_basic",b.price_basic) or 29)
        b.price_premium=int(d.get("price_premium",b.price_premium) or 49)
        b.price_trackout=int(d.get("price_trackout",b.price_trackout) or 99)
        b.price_exclusive=int(d.get("price_exclusive",b.price_exclusive) or 299)
        b.is_featured=bool(d.get("is_featured",b.is_featured))
        b.is_active=bool(d.get("is_active",b.is_active))
        db.session.commit();return jsonify({"success":True})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})

@admin_bp.route("/products")
@admin_required
def products():
    return render_template("admin/products.html",products=Product.query.order_by(Product.created_at.desc()).all())

@admin_bp.route("/products/list")
@admin_required
def list_products():
    return jsonify([{"id":p.id,"name":p.name,"price":p.price,
        "product_type":p.product_type,"is_active":p.is_active,
        "is_new":p.is_new,"file_path":p.file_path or ""}
        for p in Product.query.order_by(Product.created_at.desc()).all()])

@admin_bp.route("/products/add",methods=["POST"])
@admin_required
def add_product():
    def sf(k,s,e):
        f=request.files.get(k)
        if not f or not f.filename: return None
        if f.filename.rsplit(".",1)[-1].lower() not in e: return None
        n=secure_filename(f.filename)
        p=os.path.join(current_app.config["UPLOAD_FOLDER"],s,n)
        os.makedirs(os.path.dirname(p),exist_ok=True);f.save(p)
        return os.path.join(s,n)
    p=Product(product_type=request.form.get("type","digital"),
        name=request.form.get("name","").strip(),
        description=request.form.get("description","").strip(),
        price=int(float(request.form.get("price",0) or 0)),
        tags=request.form.get("tags","").strip(),
        printful_id=request.form.get("printful_id","").strip(),
        sizes=request.form.get("sizes","").strip(),
        is_active=request.form.get("active")=="on",
        is_new=request.form.get("is_new")=="on",
        file_path=sf("file","products",{"zip","pdf","mp3","wav","html"}),
        image_path=sf("image","products",{"jpg","jpeg","png","webp"}))
    db.session.add(p);db.session.commit()
    return jsonify({"success":True,"product_id":p.id})

@admin_bp.route("/products/<int:pid>/delete",methods=["POST"])
@admin_required
def delete_product(pid):
    p=Product.query.get_or_404(pid);db.session.delete(p);db.session.commit()
    return jsonify({"deleted":True})

@admin_bp.route("/products/<int:pid>/edit",methods=["POST"])
@admin_required
def edit_product(pid):
    p=Product.query.get_or_404(pid);d=request.get_json() or {}
    try:
        p.name=d.get("name",p.name).strip()
        p.description=d.get("description",p.description or "").strip()
        p.price=int(d.get("price",p.price) or 0)
        p.product_type=d.get("product_type",p.product_type)
        p.tags=d.get("tags",p.tags or "").strip()
        p.is_active=bool(d.get("is_active",p.is_active))
        p.is_new=bool(d.get("is_new",p.is_new))
        db.session.commit();return jsonify({"success":True})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})

@admin_bp.route("/content")
@admin_required
def content():
    return render_template("admin/content.html",content=Content.query.order_by(Content.created_at.desc()).all())

@admin_bp.route("/content/list")
@admin_required
def content_list_api():
    return jsonify([{"id":c.id,"title":c.title,"content_type":c.content_type,
        "is_published":c.is_published,"is_featured":c.is_featured}
        for c in Content.query.order_by(Content.created_at.desc()).all()])

@admin_bp.route("/content/add",methods=["POST"])
@admin_required
def add_content():
    c=Content(content_type=request.form.get("type","video"),
        title=request.form.get("title","").strip(),
        body=request.form.get("body","").strip(),
        embed_url=request.form.get("embed_url","").strip(),
        is_published=request.form.get("published")=="on",
        is_featured=request.form.get("featured")=="on")
    db.session.add(c);db.session.commit()
    return jsonify({"success":True,"content_id":c.id})

@admin_bp.route("/content/<int:cid>/delete",methods=["POST"])
@admin_required
def delete_content(cid):
    c=Content.query.get_or_404(cid);db.session.delete(c);db.session.commit()
    return jsonify({"deleted":True})
