from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required , logout_user, current_user
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__ , static_folder = 'static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = basedir+'\\static\\photo'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class emp(UserMixin,db.Model):
    __tablename__ = 'emp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable= False, unique = True)
    phone = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(250), nullable= False)
    state = db.Column(db.String(250), nullable= False)
    skill = db.Column(db.String(250), nullable= False)
    username = db.Column(db.String(100), unique= True)
    charge = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable = False)
    exp = db.Column(db.String(10), nullable = False)
    cover = db.Column(db.String(255), default='cover.jpg')
    profile = db.Column(db.String(255), default='user.jpg')

class cmp(UserMixin,db.Model):
    __tablename__ = 'cmp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable= False, unique = True)
    telephone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(250), nullable= False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(250), nullable= False)
    category = db.Column(db.String(250), nullable= False)
    established = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(255), default='cover.jpg')
    profile = db.Column(db.String(255), default='user.jpg')

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140))
    quali = db.Column(db.String(140))
    exp = db.Column(db.String(140))
    summary = db.Column(db.Text)
    email = db.Column(db.String(140))

@login_manager.user_loader
def load_user(user_id):
    if session['table_name'] == 'emp':
        return emp.query.get(int(user_id))
    if session['table_name'] == 'cmp':
        return cmp.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup_emp', methods=["POST","GET"])
def signup_emp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        address = request.form['address']
        state = request.form['state']
        skill = request.form['skill']
        username = request.form['username']
        charge = request.form['charge']
        password = request.form['password']
        gender = request.form['gender']
        exp = request.form['exp']
        user = emp(name = name, email = email, phone = phone, city = city, state = state, address = address, skill = skill, username = username, charge = charge, password = password, gender = gender, exp = exp)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_emp'))
    return render_template('signup_emp.html')


@app.route('/login_emp',methods=["POST","GET"])
def login_emp():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = emp.query.filter_by(email = email).first()
        if user:
            if password == user.password:
                session['table_name'] = 'emp'
                login_user(user)
                return redirect(url_for('profile_emp',p = user.id))
    return render_template('login_emp.html')

@app.route('/sigup_cmp',methods=["POST","GET"])
def signup_cmp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        city = request.form['city']
        address = request.form['address']
        state = request.form['state']
        category = request.form['category']
        established = request.form['established']
        password = request.form['password']
        user = cmp(name = name, email = email, telephone = telephone, city = city, state = state, address = address, category = category, established = established, password = password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_cmp'))
    return render_template('signup_cmp.html')

    return render_template('signup_cmp.html')

@app.route('/login_cmp',methods=["POST","GET"])
def login_cmp():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = cmp.query.filter_by(email = email).first()
        if user:
            if password == user.password:
                session['table_name'] = 'cmp'
                login_user(user)
                return redirect(url_for('profile_cmp',p = user.id))
    return render_template('login_cmp.html')

@app.route('/profile_emp/<p>',methods=["POST","GET"])
@login_required
def profile_emp(p):
    emp = load_user(p)
    if request.method == 'POST':
        if 'cover' in request.files:
            cover = request.files['cover']       
            emp.cover = cover.filename
            db.session.commit()
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(cover.filename)))
            return render_template('profile_emp.html',emp = emp, image = emp.profile, cover = emp.cover )
        if 'profile' in request.files:
            profile = request.files['profile']       
            emp.profile = profile.filename
            db.session.commit()
            profile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profile.filename)))
            return render_template('profile_emp.html',emp = emp, image = emp.profile, cover = emp.cover )
    return render_template('profile_emp.html',emp = emp, image = emp.profile , cover = emp.cover)

@app.route('/profile_cmp/<p>',methods=["POST","GET"])
@login_required
def profile_cmp(p):
    cmp = load_user(p)
    if request.method == 'POST':
        if 'cover' in request.files:
            cover = request.files['cover']       
            cmp.cover = cover.filename
            db.session.commit()
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(cover.filename)))
            return render_template('profile_cmp.html',cmp = cmp, image = cmp.profile, cover = cmp.cover )
        if 'profile' in request.files:
            profile = request.files['profile']       
            cmp.profile = profile.filename
            db.session.commit()
            profile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profile.filename)))
            return render_template('profile_cmp.html',cmp =cmp, image = cmp.profile, cover = cmp.cover )
        title = request.form['title']
        quali = request.form['quali']
        exp = request.form['exp']
        summary = request.form['summary']
        email = cmp.email
        user = Post(title = title, quali = quali, exp = exp, summary = summary, email = email)
        db.session.add(user)
        db.session.commit()
        return 'success'
    return render_template('profile_cmp.html',cmp = cmp, image = cmp.profile , cover = cmp.cover)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)