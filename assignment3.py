from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , redirect , url_for
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Register125@localhost/Assignment3'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    password = db.Column('password', db.Unicode)
    token = db.Column('token', db.Unicode)

    def __init__(self,id,name,password,token):
        self.id = id
        self.name = name
        self.password = password
        self.token = token

# users = User.query.all()

# @app.route('/')
# def d():

#     output = []

#     for user in users:
#         user_data = {}
#         user_data['id'] = user.id
#         user_data['name']=user.name
#         user_data['pass']=user.password
#         user_data['token']=user.token
#         output.append(user_data)

#     return jsonify({'users':output})

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        toke = request.args.get('token')

        if not toke:
            return jsonify({'message' : 'Token is missing'}),403

        try:
            token = jwt.decode(toke, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}),403

        return f(*args,**kwargs)
    
    return decorated


@app.route('/login')
def login():
    

    auth = request.authorization

    if auth:
        user_1 = User.query.filter_by(name = auth.username).first()

        if user_1:
            if user_1.password == auth.password:   
                data = jwt.encode({'user' : auth.username , 'exp':datetime.utcnow() + timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
                
                if data :
                    update_token = User.query.filter_by(id = user_1.id).first()
                    update_token.token = str(data)
                    db.session.commit()
                return jsonify({'token': data })
           
            # return '<h1>We found login{} but incorrect password </h1>'.format(auth.username)
        
        # return '<h1>Could not found a user with login:{} </h1>'.format(auth.username) 
        
        
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})
    
# @app.route('/protected/<string:token>')
# def protected(token):
#     return 'The string value is :' + token

@app.route('/protected')
# @token_required
def query_example():


    token = request.args.get('token')

    user2= User.query.all()

    for user2 in user2:
        if token ==user2.token:
            return "correct"

    return jsonify({'message ' : 'this is correct'})


    # token = None

    # if 'x-access-token' in request.headers:
    #     token = request.headers['x-access-token']
    #     data = jwt.decode(token,app.config['SECRET_KEY'])
    #     current_user = User.query.filter_by(name=data['name']).first()



    # if key doesn't exist, returns None
    
    # return '''<h1>The token value is: {}</h1>'''.format(token)
    # return redirect(url_for('protected',token = str(tok)))







if __name__ == '__main__':
        app.run(debug=True)

# update_this = User.query.filter_by(id=user_data['id']).first()
# update_this.token = "ErsErs"

# new_ex = Example(5,"fifth entry")
# db.session.add(update_this)

# db.session.commit()
