from flask import Flask,jsonify,request
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import cross_origin
#from dbtest import get_connection
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, String, Column,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@postgres-service:5432/pythonpoc"
db = SQLAlchemy(app)
#app.app_context().push()

# creating the user model in flask shell execute db.create_all() to create the Users table in db
class Users(db.Model):
    __tablename__="Users"
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10))
    password = db.Column(db.String(50))
    confirm_password = db.Column(db.String(50))

    def __init__(self,user_id,name,email,age,address,phone,password,confirm_password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.address = address
        self.phone = phone
        self.password = password
        self.confirm_password = confirm_password

    def __repr__(self):
        return f"<User_id {self.user_id}, UserName {self.name}, Email {self.email}, Phone {self.phone},password {self.password}, confirm_password {self.confirm_password}>"

class Address(db.Model):
    __tablename__="Address"
    address_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('Users.user_id'))
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String)
    isDefault = db.Column(db.String)

    def __init__(self,address_id,user_id,address,city,state,country,postal_code,isDefault,phone):
        self.address_id = address_id
        self.user_id = user_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.isDefault = isDefault
        self.phone = phone

    def __repr__(self):
        return f"<user_id={self.user_id}, address={self.address} {self.city} {self.state} {self.country} {self.postal_code}, phone={self.phone}>"

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
     return jsonify(error=str(e))

#test api
@app.route('/',methods=['GET'])
def test():
    return "Welcome to flask application."


# adding a user data
@app.route('/adduser',methods=['POST'])
@cross_origin()
def adduser():
    try:
        userdata = request.get_json()
        #newUser = Users(userId=userdata.get("userId"),userName=userdata.get("userName"),email=userdata.get("email"),age=userdata.get("age"),address=userdata.get("address"),phone=userdata.get("phone"))
        #session.add(newUser)
        #session.commit()
        #print(userdata)
        #password=generate_password_hash(userdata['password'], method='sha256')
     
        #newUser = Users(user_id=userdata['user_id'],name=userdata['name'],email=userdata['email'],age=userdata['age'],address=userdata['address'],phone=userdata['phone'],password=userdata['password'],confirm_password=userdata['confirm_password'])
        
        password= userdata['password']
        newUser = Users(user_id=userdata['user_id'],name=userdata['name'],email=userdata['email'],age=userdata['age'],address=userdata['address'],phone=userdata['phone'],password=password,confirm_password=password)
        print(newUser)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": f"User {userdata.get('name')} has been created successfully.","error":False})
    except:
        return jsonify({"message": f"Error in creating user {userdata.get('name')}","error":True})

    return jsonify({"message": f"User {userdata.get('name')} has been created successfully.","error":False})

#retriveing the userdata
@app.route('/fetchuser',methods=['POST'])
def fetchuser():
    try:
        data = request.get_json()
        user = Users.query.all()

        cols = ['user_id', 'name', 'email','age','address','phone']
        result = [{col: getattr(d, col) for col in cols} for d in user]
    except:
         return jsonify({"message": f"Error in fetching the user details"})
    return jsonify(userData = result)

#updating the user data
@app.route('/updateuser',methods=['POST'])
def updateUser():
    try:
        data = request.get_json()
        if data.get('user_id') not in ("",[],None,0,False):
            user = Users.query.filter_by(user_id=data.get('user_id')).first()
            if data.get('name'):
                user.name = data.get('name')
            if data.get('age'):
                user.age = data.get('age')
            if data.get('email'):
                user.email = data.get('email')
            if data.get('address'):
                user.address = data.get('address')
            if data.get('phone'):
                user.phone = data.get('phone')

        else:
            return jsonify({"message": "Error in the request params"})
    except:
        return jsonify({"message": f"user with id {data.get('user_id')} doesn't exists."})

    db.session.commit()
    return jsonify({"message": f"Users with Id {user.user_id} has been updated successfully."})


#deleting the user data
@app.route('/deleteuser',methods=['POST'])
def deleteUser():
    try:
        data = request.get_json()
        if data.get('user_id') not in ("",[],None,0,False):
            user = Users.query.filter_by(user_id=data.get('user_id')).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
            else:
                return jsonify({"message": f"No user with id {user.user_id}"})
        else:
             return jsonify({"message": f"Error in the request params"})
    except:
        return jsonify({"message": "No user with the given id"})

    return jsonify({"message": f"Users with Id {user.user_id} has been deleted successfully."})

# user login api
@app.route('/login',methods=['POST'])
@cross_origin()
def login():
    try :
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if not user or (user.password!= data['password']):
            return jsonify({"message":"Please check your login details and try again.","error":True})
    except:
        return jsonify({"message":"Please check your login details and try again.","error":True})

    return jsonify({"message":f"Login success with email id {data['email']}","error":False})

#resetting password
@app.route('/resetPassword',methods=['POST'])
def resetPassword():
    try:
        data = request.get_json()
        if data.get('user_id') not in ("",[],None,0,False):
            user = Users.query.filter_by(user_id=data['user_id']).first()
            if not user or not check_password_hash(user.password, data['old_password']):
                return jsonify({"message":"Please check your login details and try again."})
            else:
                new_password=generate_password_hash(data['new_password'], method='sha256')
                user.password = new_password
                user.confirm_password = new_password
                db.session.commit()
                return jsonify({"message":"Password updated successfully."})
    except:
         return jsonify({"message":"Please check your request params and pass correct user_id."})


#adding address
@app.route('/addAddress',methods=['POST'])
def addAddress():
    try:
        data = request.get_json()
        print(data)
        user = Users.query.filter_by(user_id=data.get('user_id')).first()
        if user:
            address = Address(address_id=data['address_id'],user_id=data['user_id'],address=data['address'],city=data['city'],state=data['state'],country=data['country'],postal_code=data['postal_code'],phone=data['phone'],isDefault=data['isDefault'])
            db.session.add(address)
            db.session.commit()
            return jsonify({"message":f"Address for the user with userId {data.get('user_id')} has been added."})
        else:
            return jsonify({"message":f"User with userId {data.get('user_id')} doesn't exists."})
    except:
        return jsonify({"message":f"User with userId {data.get('user_id')} doesn't exists."})

#displaying address
@app.route('/fetchAddress',methods=['POST'])
def fetchAddress():
    try:
        data = request.get_json()
        if data.get('user_id'):
            user = Users.query.filter_by(user_id=data.get('user_id')).first()
            if user:
                 address = Address.query.filter_by(user_id=data.get('user_id')).all()
                 cols = ['user_id', 'address', 'city','state','country','postal_code','phone','isDefault','address_id']
                 result = [{col: getattr(d, col) for col in cols} for d in address]
                 return jsonify({"address":result})
            else:
                return jsonify({"message":f"User with userId {data.get('user_id')} doesn't exists."})

        else:
            return jsonify({"message":"Please check the request params and pass the correct user_id"})
    except:
        return jsonify({"message":"Error in fetching the address"})

# deleting address
@app.route('/deleteAddress',methods=['POST'])
def deleteAddress():
    data = request.get_json()
    try:
        if data.get('user_id') and data.get('address_id'):
            user = Users.query.filter_by(user_id=data.get('user_id')).first()
            if user:
                address = Address.query.filter_by(address_id=data.get('address_id'),user_id=data.get('user_id')).first()
                print(address)
                if address:
                    db.session.delete(address)
                    db.session.commit()
                    return jsonify({"message":f"Address for the user with userId {data.get('user_id')} deleted."})
                else:
                    return jsonify({"message":"Address doesn't exists"})
            else:
                return jsonify({"message":f"User with userId {data.get('user_id')} doesn't exists."})
        else:
            return jsonify({"message":"Please check the request params or pass correct user id and address id"})
    except:
        return jsonify({"message":f"User with userId {data.get('user_id')} doesn't exists."})

if __name__ == '__main__':
   app.run(debug = True)

