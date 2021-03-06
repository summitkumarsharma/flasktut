from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.dialects import registry
# from sqlalchemy.dialects.mysql import mysqldb
from flask_mail import Mail
from flask import json
from datetime import datetime
local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
# engine = create_engine("mysql+pymysql://root:@localhost/codingthunder")
# print(engine)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False


class Contacts(db.Model):
    '''
    sno, name ,email, phone, msg, date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)


@app.route("/")
def home():
    return render_template("index.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/post")
def post():
    return render_template("post.html",params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, phone=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[params[' gmail-user ']],
                          body=msg + "\n" + phone
                          )
    return render_template('contact.html', params=params)


app.run(debug=True)
