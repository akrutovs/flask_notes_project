from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'its about page'


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    string = name + str(id)
    return 'hi, ' + string


if __name__ == '__main__':
    app.run(debug=True)
