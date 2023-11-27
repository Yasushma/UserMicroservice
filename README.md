# UserMicroservice
# DB configuration

userOperation.py 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/pythonpoc"
db = SQLAlchemy(app)

# Package Installation 
pip install flask
pip instll flask-sqlalchemy
pip install psycopg2-binary
pip install SQLAlchemy
pip install werkzeug




CREATE TABLE IF NOT EXISTS public."Address"
(
    address_id integer NOT NULL,
    user_id integer,
    address character varying COLLATE pg_catalog."default",
    city character varying COLLATE pg_catalog."default",
    state character varying COLLATE pg_catalog."default",
    country character varying COLLATE pg_catalog."default",
    postal_code character varying(10) COLLATE pg_catalog."default",
    phone character varying COLLATE pg_catalog."default",
    "isDefault" character varying COLLATE pg_catalog."default",
    CONSTRAINT "Address_pkey" PRIMARY KEY (address_id),
    CONSTRAINT "Address_user_id_fkey" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)



CREATE TABLE "Users"
(
    user_id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    email character varying(50) COLLATE pg_catalog."default",
    age integer,
    address character varying(200) COLLATE pg_catalog."default",
    phone character varying(10) COLLATE pg_catalog."default",
    password character varying COLLATE pg_catalog."default",
    confirm_password character varying COLLATE pg_catalog."default",
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id)
)

CREATE TABLE IF NOT EXISTS public."User_detail"
(
    id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    email character varying(50) COLLATE pg_catalog."default",
    age integer,
    address character varying(200) COLLATE pg_catalog."default",
    phone character varying(10) COLLATE pg_catalog."default",
    password character varying(50) COLLATE pg_catalog."default",
    confirm_password character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT "User_detail_pkey" PRIMARY KEY (id)
)



API
http://127.0.0.1:5000/create
{
  "user_id":"4",
  "user_name":"John",
  "age":"29",
  "address":"Global village",
  "contact_num":"7786789876"
}

http://127.0.0.1:5000/login
{
  "email":"Anil@gmail.com",
  "password":"654321"
}

http://127.0.0.1:5000/resetPassword
{
  "user_id":7,
  "old_password":"123456",
  "new_password":"654321"
}

http://127.0.0.1:5000/addAddress
{
  "user_id":2,
  "address_id":3,
  "address":"#465",
  "city":"Bangalore",
  "state":"Karnataka",
  "country":"India",
  "postal_code":"560060",
  "phone":"8798765678",
  "isDefault":"No"
}

http://127.0.0.1:5000/fetchAddress
{
  "user_id":1
}

http://127.0.0.1:5000/deleteAddress
{
  "user_id":2,
  "address_id":3
}

http://127.0.0.1:5000/displayuser
{
  
}

http://127.0.0.1:5000/updateuser
{
  "user_id":3,
  "name":"suchith1222",
  "age":"6"
}