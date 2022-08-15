from flask import Flask, render_template
import requests
import datetime

app = Flask(__name__)

# API #
response = requests.get(url="https://api.npoint.io/2aadaa023052ac694686")
response.raise_for_status()
data = response.json()

date = datetime.datetime.now()
today = date.strftime("%d/%m/20%y")


@app.route('/')
def get_index():  # put application's code here
    return render_template('index.html', data=data, date=today)


@app.route('/about/')
def get_about():
    return render_template('about.html')


@app.route('/contact/')
def get_contact():
    return render_template('contact.html')


@app.route('/post/<int:id>')
def get_post(id):
    post = data[id - 1]
    return render_template("post.html", data=post, date=today)


if __name__ == '__main__':
    app.run()
