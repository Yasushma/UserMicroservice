import psycopg2

def get_connection():
    try:
        return psycopg2.connect(
            database="pythonpoc",
            user="postgres",
            password="root123",
            host="127.0.0.1",
            port=5432,
        )
    except:
        return False

conn = get_connection()

if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")

cur = conn.cursor()

#cur.execute("INSERT INTO USER_INFO (USER_ID,USER_NAME,AGE,ADDRESS,CONTACT_NUM) \
 #     VALUES (1, 'Paul', 32, '#123,sonata software', 9878909876 )");
'''cur.execute("SELECT user_id, user_name, address, contact_num  from USER_INFO")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.commit()
conn.close() '''


