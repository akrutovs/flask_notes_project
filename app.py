from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

db_name = 'database'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'db'
db_port = '5432'
# secret_password
app = Flask(__name__)
# db model
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'loooong_secret_key'
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_string

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # перенаправление на авторизацию

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Note id %r' % self.id

db.create_all()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('email')
        password = request.form.get('password')
        # поиск пользователя в базе
        user = db.session.query(User).filter(User.email == username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect('/users')
        else:
            message = "Wrong username or password"

    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# db model user
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/users')
@login_required  # должен проверять авторизацию
def show_users():
    # создание шаблона через который будем получать все записии из базы данных
    users = User.query.order_by(User.registration_date.desc()).all()  # обращение к базе данных
    # передача списка в шаблон
    return render_template('users.html', users=users)


@app.route('/current_user')
@login_required
def show_current_users():
    return render_template('current_user.html', current_user=current_user)


@app.route('/users/<int:user_id>')
def show_one_user(user_id):
    user = User.query.get(user_id)
    return render_template('detail_user.html', user=user)


@app.route('/notes')
def show_notes():
    # создание шаблона через который будем получать все записии из базы данных
    notes = Notes.query.order_by(Notes.date.desc()).all()  # обращение к базе данных
    # передача списка в шаблон
    return render_template('notes.html', notes=notes)


@app.route('/notes/<int:notes_id>')
def show_one_note(notes_id):
    note = Notes.query.get(notes_id)
    return render_template('detail_note.html', note=note)


@app.route('/notes/<int:notes_id>/delete')
def delete_one_note(notes_id):
    note = Notes.query.get_or_404(notes_id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes')
    except:
        return 'Error'


@app.route('/notes/<int:notes_id>/update', methods=['POST', "GET"])
def update_note(notes_id):
    note = Notes.query.get(notes_id)
    if request.method == 'POST':
        note.user_id = request.form['user_id']
        note.title = request.form['title']
        note.text = request.form['text']

        try:
            db.session.commit()  # save
            return redirect('/notes')
        except:
            return "Error"

    else:
        return render_template('update_note.html', note=note)


@app.route('/add_note', methods=['POST', "GET"])
def add_note():
    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        text = request.form['text']
        note = Notes(user_id=user_id, title=title, text=text)
        try:
            db.session.add(note)  # add
            db.session.commit()  # save
            return redirect('/notes')
        except:
            return "Error"

    else:
        return render_template('add_note.html')


@app.route('/registration', methods=['POST', "GET"])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, name=name)
        user.set_password(password)
        try:
            db.session.add(user)  # add
            db.session.commit()  # save
            return redirect('/users')
        except:
            return "Error"

    else:
        return render_template('create_user.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
