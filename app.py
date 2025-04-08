from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbk_udk.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class BBK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bbk_code = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)

class UDK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    udk_code = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.String(500), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    args = request.args.to_dict()
    query = args.get("q", str).split(' ')
    bbk_list = BBK.query.all()
    for m in query:
        bbk_list = (BBK.query.filter(
            BBK.keywords.like(f"%{m}%")
            ) if args else BBK.query.all())
    return render_template("bbk_index.html", bbk_list=bbk_list)

@app.route("/udk")
def udk_index():
    args = request.args.to_dict()
    query = args.get("q", str).split(' ')
    udk_list = UDK.query.all()
    for m in query:
        udk_list = (UDK.query.filter(
            UDK.keywords.like(f"%{m}%")
            ) if args else UDK.query.all())
    return render_template("udk.html", udk_list=udk_list)

@app.route("/add_bbk", methods=["GET", "POST"])
@login_required
def add_bbk():
    if request.method == "POST":
        bbk_code = request.form["bbk_code"]
        category = request.form["category"]
        keywords = request.form["keywords"]
        existing_bbk = BBK.query.filter_by(bbk_code=bbk_code).first()
        if existing_bbk:
            flash("ББК код уже существует!", "warning")
            return redirect(url_for("add_bbk"))
        new_bbk = BBK(bbk_code=bbk_code, category=category, keywords=keywords)
        db.session.add(new_bbk)
        db.session.commit()
        flash("Запись ББК успешно добавлена!", "success")
        return redirect(url_for("index"))

    return render_template("add_bbk.html")

@app.route("/add_udk", methods=["GET", "POST"])
@login_required
def add_udk():
    if request.method == "POST":
        udk_code = request.form["udk_code"]
        category = request.form["category"]
        keywords = request.form["keywords"]
        existing_udk = UDK.query.filter_by(udk_code=udk_code).first()
        if existing_udk:
            flash("УДК код уже существует!", "warning")
            return redirect(url_for("add_udk"))
        new_udk = UDK(udk_code=udk_code, category=category, keywords=keywords)
        db.session.add(new_udk)
        db.session.commit()
        flash("Запись УДК успешно добавлена!", "success")
        return redirect(url_for("udk_index"))
    return render_template("add_udk.html")

@app.route("/edit_bbk/<int:id>", methods=["GET", "POST"])
@login_required
def edit_bbk(id):
    bbk = BBK.query.get_or_404(id)
    if request.method == "POST":
        bbk.bbk_code = request.form["bbk_code"]
        bbk.category = request.form["category"]
        bbk.keywords = request.form["keywords"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_bbk.html", bbk=bbk)

@app.route("/edit_udk/<int:id>", methods=["GET", "POST"])
@login_required
def edit_udk(id):
    udk = UDK.query.get_or_404(id)
    if request.method == "POST":
        udk.udk_code = request.form["udk_code"]
        udk.category = request.form["category"]
        udk.keywords = request.form["keywords"]
        db.session.commit()
        return redirect(url_for("udk_index"))
    return render_template("edit_udk.html", udk=udk)

@app.route("/delete_bbk/<int:id>", methods=["POST"])
@login_required
def delete_bbk(id):
    bbk = BBK.query.get_or_404(id)
    db.session.delete(bbk)
    db.session.commit()
    flash("Запись ББК удалена!", "success")
    return redirect(url_for("index"))


@app.route("/delete_udk/<int:id>", methods=["POST"])
@login_required
def delete_udk(id):
    udk = UDK.query.get_or_404(id)
    db.session.delete(udk)
    db.session.commit()
    flash("Запись УДК удалена!", "success")
    return redirect(url_for("udk_index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Неверные данные", "danger")
    return render_template("login.html")

#@app.route("/register", methods=["GET", "POST"])
#def register():
#    if request.method == "POST":
#        username = request.form["username"]
#        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
#        new_user = User(username=username, password_hash=password)
#        db.session.add(new_user)
#        db.session.commit()
#        return redirect(url_for("login"))
#    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
