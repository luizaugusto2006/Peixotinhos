import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.utils import secure_filename
from config import Config
from models import db, Admin, Event, Photo, AboutTopic


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, int(user_id))

    def admin_required(f):
        @wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            return f(*args, **kwargs)
        return decorated

    def allowed_file(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in app.config["ALLOWED_EXTENSIONS"]
        )

    # ── Public routes ──────────────────────────────────────────

    @app.route("/")
    def index():
        events = (
            Event.query
            .filter_by(is_published=True)
            .order_by(Event.date.desc())
            .all()
        )
        years = sorted(set(e.date.year for e in events), reverse=True)
        return render_template("index.html", events=events, years=years)

    @app.route("/sobre")
    def about():
        topics = AboutTopic.query.order_by(AboutTopic.order, AboutTopic.id).all()
        return render_template("about.html", topics=topics)

    @app.route("/evento/<int:event_id>")
    def event_detail(event_id):
        event = Event.query.get_or_404(event_id)
        if not event.is_published and not current_user.is_authenticated:
            abort(404)
        photos = Photo.query.filter_by(event_id=event.id).order_by(Photo.order, Photo.id).all()
        return render_template("event_detail.html", event=event, photos=photos)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # ── Auth routes ────────────────────────────────────────────

    @app.route("/admin/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("admin_dashboard"))
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = Admin.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash("Login realizado com sucesso!", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("admin_dashboard"))
            flash("Usuário ou senha inválidos.", "danger")
        return render_template("login.html")

    @app.route("/admin/logout")
    @login_required
    def logout():
        logout_user()
        flash("Você saiu do painel.", "info")
        return redirect(url_for("index"))

    # ── Admin routes ───────────────────────────────────────────

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        events = Event.query.order_by(Event.date.desc()).all()
        total_photos = Photo.query.count()
        return render_template(
            "admin/dashboard.html", events=events, total_photos=total_photos
        )

    @app.route("/admin/evento/novo", methods=["GET", "POST"])
    @admin_required
    def admin_event_new():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            date_str = request.form.get("date", "")
            is_published = "is_published" in request.form

            if not title or not date_str:
                flash("Título e data são obrigatórios.", "danger")
                return render_template("admin/event_form.html", event=None)

            from datetime import datetime as dt
            event_date = dt.strptime(date_str, "%Y-%m-%d").date()

            cover_photo = ""
            if "cover" in request.files:
                file = request.files["cover"]
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(
                        f"cover_{event_date}_{file.filename}"
                    )
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    cover_photo = filename

            event = Event(
                title=title,
                description=description,
                date=event_date,
                cover_photo=cover_photo,
                is_published=is_published,
            )
            db.session.add(event)
            db.session.commit()
            flash("Evento criado com sucesso!", "success")
            return redirect(url_for("admin_event_photos", event_id=event.id))

        return render_template("admin/event_form.html", event=None)

    @app.route("/admin/evento/<int:event_id>/editar", methods=["GET", "POST"])
    @admin_required
    def admin_event_edit(event_id):
        event = Event.query.get_or_404(event_id)
        if request.method == "POST":
            event.title = request.form.get("title", "").strip()
            event.description = request.form.get("description", "").strip()
            event.is_published = "is_published" in request.form

            date_str = request.form.get("date", "")
            if date_str:
                from datetime import datetime as dt
                event.date = dt.strptime(date_str, "%Y-%m-%d").date()

            if "cover" in request.files:
                file = request.files["cover"]
                if file and file.filename and allowed_file(file.filename):
                    if event.cover_photo:
                        old_path = os.path.join(app.config["UPLOAD_FOLDER"], event.cover_photo)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    filename = secure_filename(f"cover_{event.date}_{file.filename}")
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    event.cover_photo = filename

            db.session.commit()
            flash("Evento atualizado!", "success")
            return redirect(url_for("admin_dashboard"))

        return render_template("admin/event_form.html", event=event)

    @app.route("/admin/evento/<int:event_id>/excluir", methods=["POST"])
    @admin_required
    def admin_event_delete(event_id):
        event = Event.query.get_or_404(event_id)
        for photo in event.photos:
            path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
            if os.path.exists(path):
                os.remove(path)
        if event.cover_photo:
            path = os.path.join(app.config["UPLOAD_FOLDER"], event.cover_photo)
            if os.path.exists(path):
                os.remove(path)
        db.session.delete(event)
        db.session.commit()
        flash("Evento excluído.", "info")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/evento/<int:event_id>/fotos", methods=["GET", "POST"])
    @admin_required
    def admin_event_photos(event_id):
        event = Event.query.get_or_404(event_id)
        if request.method == "POST":
            files = request.files.getlist("photos")
            caption = request.form.get("caption", "").strip()
            count = 0
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"evt{event.id}_{file.filename}")
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    photo = Photo(
                        event_id=event.id,
                        filename=filename,
                        caption=caption,
                    )
                    db.session.add(photo)
                    count += 1
            db.session.commit()
            flash(f"{count} foto(s) adicionada(s)!", "success")
            return redirect(url_for("admin_event_photos", event_id=event.id))

        photos = Photo.query.filter_by(event_id=event.id).order_by(Photo.order, Photo.id).all()
        return render_template("admin/event_photos.html", event=event, photos=photos)

    @app.route("/admin/foto/<int:photo_id>/excluir", methods=["POST"])
    @admin_required
    def admin_photo_delete(photo_id):
        photo = Photo.query.get_or_404(photo_id)
        event_id = photo.event_id
        path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        if os.path.exists(path):
            os.remove(path)
        db.session.delete(photo)
        db.session.commit()
        flash("Foto excluída.", "info")
        return redirect(url_for("admin_event_photos", event_id=event_id))

    @app.route("/admin/foto/<int:photo_id>/legenda", methods=["POST"])
    @admin_required
    def admin_photo_caption(photo_id):
        photo = Photo.query.get_or_404(photo_id)
        photo.caption = request.form.get("caption", "").strip()
        db.session.commit()
        flash("Legenda atualizada.", "success")
        return redirect(url_for("admin_event_photos", event_id=photo.event_id))

    # ── Admin management routes ─────────────────────────────────

    ALLOWED_MANAGERS = ("admin", "luiz")

    def manager_required(f):
        @wraps(f)
        @admin_required
        def decorated(*args, **kwargs):
            if current_user.username.lower() not in ALLOWED_MANAGERS:
                abort(403)
            return f(*args, **kwargs)
        return decorated

    @app.route("/admin/usuarios")
    @manager_required
    def admin_users():
        users = Admin.query.order_by(Admin.id).all()
        return render_template("admin/users.html", users=users)

    @app.route("/admin/usuarios/novo", methods=["GET", "POST"])
    @manager_required
    def admin_user_new():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                flash("Usuário e senha são obrigatórios.", "danger")
                return render_template("admin/user_form.html", user=None)
            if Admin.query.filter_by(username=username).first():
                flash("Este nome de usuário já existe.", "danger")
                return render_template("admin/user_form.html", user=None)
            user = Admin(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash(f"Administrador '{username}' criado com sucesso!", "success")
            return redirect(url_for("admin_users"))
        return render_template("admin/user_form.html", user=None)

    @app.route("/admin/usuarios/<int:user_id>/excluir", methods=["POST"])
    @manager_required
    def admin_user_delete(user_id):
        user = Admin.query.get_or_404(user_id)
        if user.id == current_user.id:
            flash("Você não pode excluir seu próprio usuário.", "danger")
            return redirect(url_for("admin_users"))
        if user.username.lower() in ALLOWED_MANAGERS:
            flash("Não é possível excluir um administrador principal.", "danger")
            return redirect(url_for("admin_users"))
        db.session.delete(user)
        db.session.commit()
        flash(f"Administrador '{user.username}' excluído.", "info")
        return redirect(url_for("admin_users"))

    @app.route("/admin/usuarios/<int:user_id>/senha", methods=["POST"])
    @manager_required
    def admin_user_password(user_id):
        user = Admin.query.get_or_404(user_id)
        new_password = request.form.get("password", "").strip()
        if not new_password:
            flash("A senha não pode estar vazia.", "danger")
            return redirect(url_for("admin_users"))
        user.set_password(new_password)
        db.session.commit()
        flash(f"Senha de '{user.username}' alterada com sucesso!", "success")
        return redirect(url_for("admin_users"))

    # ── About topics management ────────────────────────────────

    @app.route("/admin/sobre")
    @admin_required
    def admin_about():
        topics = AboutTopic.query.order_by(AboutTopic.order, AboutTopic.id).all()
        return render_template("admin/about_topics.html", topics=topics)

    @app.route("/admin/sobre/novo", methods=["GET", "POST"])
    @admin_required
    def admin_about_new():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()
            order = request.form.get("order", 0, type=int)
            if not title or not content:
                flash("Título e conteúdo são obrigatórios.", "danger")
                return render_template("admin/about_form.html", topic=None)
            topic = AboutTopic(title=title, content=content, order=order)
            db.session.add(topic)
            db.session.commit()
            flash("Tópico criado com sucesso!", "success")
            return redirect(url_for("admin_about"))
        return render_template("admin/about_form.html", topic=None)

    @app.route("/admin/sobre/<int:topic_id>/editar", methods=["GET", "POST"])
    @admin_required
    def admin_about_edit(topic_id):
        topic = AboutTopic.query.get_or_404(topic_id)
        if request.method == "POST":
            topic.title = request.form.get("title", "").strip()
            topic.content = request.form.get("content", "").strip()
            topic.order = request.form.get("order", 0, type=int)
            if not topic.title or not topic.content:
                flash("Título e conteúdo são obrigatórios.", "danger")
                return render_template("admin/about_form.html", topic=topic)
            db.session.commit()
            flash("Tópico atualizado com sucesso!", "success")
            return redirect(url_for("admin_about"))
        return render_template("admin/about_form.html", topic=topic)

    @app.route("/admin/sobre/<int:topic_id>/excluir", methods=["POST"])
    @admin_required
    def admin_about_delete(topic_id):
        topic = AboutTopic.query.get_or_404(topic_id)
        db.session.delete(topic)
        db.session.commit()
        flash("Tópico excluído.", "info")
        return redirect(url_for("admin_about"))

    # ── Create tables ──────────────────────────────────────────

    with app.app_context():
        db.create_all()
        if not Admin.query.first():
            admin = Admin(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
