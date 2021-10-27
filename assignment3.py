from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt

app = Flask(name)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kalamkas@localhost/python1'
db = SQLAlchemy(app)

class User(db.Model):
    tablename = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    password = db.Column('password', db.Unicode)
    token = db.Column('token', db.Unicode)

    def init(self,id,name,password,token):
        self.id = id
        self.name = name
        self.password = password
        self.token = token




# /output =[]

def data():
    users = User.query.all()

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name']=user.name
        user_data['pass']=user.password
        user_data['token']=user.token
    
    return user_data['name']


@app.route('/login')
def login():
    data()
    auth = request.authorization

    if auth and auth.username == user_data['name'] and auth.password == user_data['pass']:
        token = jwt.encode({'user' : auth.username , 'exp':datetime.utcnow() + timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
    
        return jsonify({'token': token })
        
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})

    

if name == 'main':
    app.run(debug=True)