from flask_login import current_user, login_user, logout_user, login_required
import secrets
import util
import uuid
from flask import Flask, render_template, jsonify, json, request, redirect, url_for
import os
from sqlalchemy import create_engine, Column, Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config['SQLALCHEMY_DATABASE_URI'] = util.get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = util.get_uploads_path()
app.config['MAX_CONTENT_LENGTH'] = 120 * 1024 * 1024

login = LoginManager()
login.init_app(app)
login.login_view = 'login'

Base = declarative_base()

engine = create_engine(util.get_db_uri(), connect_args={'check_same_thread': False}, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True)
    category = Column(String(64))
    name = Column(String(64))
    description = Column(String(256))
    image = Column(String(64))

    def __repr__(self):
        return '<Item %r' % self.name


class UserModel(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True)
    username = Column(String(100))
    password_hash = Column(String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return session.query(UserModel).get(int(user_id))


Base.metadata.create_all(engine)


# plant1 = Plant(name="Better Boy Tomato", description="Indeterminant. Harvest in 90 days.", image="tomatoplant.jpg")
# plant2 = Plant(name="Better Boy Tomato", description="Indeterminant. Harvest in 90 days.", image="tomatoplant.jpg")
# plant3 = Plant(name="Better Boy Tomato", description="Indeterminant. Harvest in 90 days.", image="tomatoplant.jpg")
# plant4 = Plant(name="Better Boy Tomato", description="Indeterminant. Harvest in 90 days.", image="tomatoplant.jpg")
# plant5 = Plant(name="Better Boy Tomato", description="Indeterminant. Harvest in 90 days.", image="tomatoplant.jpg")
#
# session.add_all([plant1, plant2, plant3, plant4, plant5])
# session.commit()


@app.route('/', methods=['GET'])
def home():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username

    return render_template('home.html', username=username)


@app.route('/items', methods=['GET'])
def get_items():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    plants = session.query(Plant).all()
    return render_template('items.html', plants=plants, username=username)


@app.route('/plants', methods=['GET'])
def get_plants():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    plants = session.query(Plant).filter_by(category='Plant').all()
    return render_template('items.html', plants=plants, username=username)


@app.route('/seeds', methods=['GET'])
def get_seeds():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    plants = session.query(Plant).filter_by(category='Seed').all()
    return render_template('items.html', plants=plants, username=username)


@app.route('/produce', methods=['GET'])
def get_produce():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    plants = session.query(Plant).filter_by(category='Produce').all()
    return render_template('items.html', plants=plants, username=username)


@app.route('/item/<identifier>', methods=['GET'])
def get_item(identifier):
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    plant = session.query(Plant).get(int(identifier))
    return render_template('item.html', plant=plant, username=username)

@app.route('/createitem/<category>', methods=['GET'])
@login_required
def create_item(category):
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username

    plant_checked = ''
    seed_checked = ''
    produce_checked = ''

    if category == 'Plant':
        plant_checked = 'checked'
    if category == 'Seed':
        seed_checked = 'checked'
    if category == 'Produce':
        produce_checked = 'checked'

    return render_template('createitem.html', username=username, plant_checked=plant_checked, seed_checked=seed_checked, produce_checked=produce_checked)


@app.route('/additem', methods=['GET', 'POST'])
@login_required
def add_item():
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username

    #if request.method == 'POST':
    item_category = request.form['item_category']
    item_name = request.form['item_name']
    item_description = request.form['item_description']
    item_image = request.files['item_image']

    if item_image.filename == '':
        filename = '3ed16f28-7c43-4e92-8a53-cda059dbf47c.png' # no image available
    else:
        filename = '' + str(uuid.uuid4()) + '.' + item_image.filename.rsplit('.')[1]
        fullpath = util.get_uploads_path() + filename
        item_image.save(fullpath)

    new_item = Plant(category=item_category, name=item_name, description=item_description, image=filename)
    session.add_all([new_item])
    session.commit()
    message = 'Item published - ' + item_name
    username = ''

    return render_template('message.html', message=message, username=username)


@app.route('/articles', methods=['GET'])
def get_articles():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    return render_template('articles.html', username=username)


@app.route('/article', methods=['GET'])
def get_article():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    return render_template('article.html', username=username)


@app.route('/createarticle', methods=['GET','POST'])
@login_required
def create_article():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    return render_template('createarticle.html', username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        user = session.query(UserModel).filter_by(email=email).first()
        # user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)

            next = request.args.get('next')

            return redirect(next or url_for('home'))

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():

    if current_user.is_authenticated:
        return redirect('/createitem')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        count = session.query(func.count('*')).select_from(UserModel).filter_by(email=email).scalar()
        if count > 0:
            message = 'Email already exists'
            return render_template('message.html', message=message)

        user = UserModel(email=email, username=username)
        user.set_password(password)
        session.add_all([user])
        session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/search', methods=['POST', 'GET'])
def search():
    username = ''
    if current_user.is_authenticated:
        username = session.query(UserModel).get(current_user.get_id()).username
    name = request.form['search']
    results = session.query(Plant).filter(Plant.name.like('%' + name + '%')).all()

    return render_template('search_results.html', results=results, search=name, username=username)


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    port = 5000
    app.run(host=ip, port=port)
