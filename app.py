from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# db model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# db model user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'User %r' % self.id


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Note id %r' % self.id


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/users')
def show_users():
    # создание шаблона через который будем получать все записии из базы данных
    users = User.query.order_by(User.registration_date.desc()).all()  # обращение к базе данных
    # передача списка в шаблон
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def show_one_user(user_id):
    user = User.query.get(user_id)
    return render_template('detail_user.html', user=user)


@app.route('/registration', methods=['POST', "GET"])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password, name=name)
        try:
            db.session.add(user)  # add
            db.session.commit()  # save
            return redirect('/users')
        except:
            return "Error"

    else:
        return render_template('create_user.html')


if __name__ == '__main__':
    app.run(debug=True)
