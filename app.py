import smtplib
from flask import Flask, render_template, request
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API #
response = requests.get(url="https://api.npoint.io/2aadaa023052ac694686")
response.raise_for_status()
data = response.json()

date = datetime.datetime.now()
today = date.strftime("%d/%m/20%y")

# Email #
user = os.getenv('USER')
password = os.getenv('PASSWORD')


@app.route('/')
def get_index():  # put application's code here
    return render_template('index.html', data=data, date=today)


@app.route('/about/')
def get_about():
    return render_template('about.html')


@app.route('/contact/', methods=["POST", "GET"])
def get_contact():
    if request.method == 'POST':
        title = "Successfully sent message."
        receive_data()
        return render_template('contact.html', title=title)
    else:
        return render_template('contact.html')


@app.route('/post/<int:id>')
def get_post(id):
    post = data[id - 1]
    return render_template("post.html", data=post, date=today)


def receive_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    print(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
    send_email(name, email, phone, message)


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=user, password=password)
        connection.sendmail(
            from_addr=user,
            to_addrs="nicolajlpedersen@gmail.com",
            msg=f"Subject:New message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )


if __name__ == '__main__':
    app.run(debug=True)
