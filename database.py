import mysql.connector
import hashlib

db = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'shop_db')
curs = db.cursor()

def load_books():
    q = "select * from products"
    curs.execute(q)
    books = curs.fetchall()
    return books

def Login(data):
    email = data['email']
    password = hashlib.md5(data['password'].encode()).hexdigest()
    # password = password
    
    if email and password :
        q = 'SELECT * FROM users WHERE email = %s AND password = %s' 
        curs.execute(q, (email, password, ))
        res = curs.fetchone()

    if res:
        return res
    else:
        return False
    
def register_db(data):
    bol = 'Registration failed try again'
    name = data['name']
    email = data['email']
    password = hashlib.md5(data['password'].encode()).hexdigest()
    cpassword = hashlib.md5(data['cpassword'].encode()).hexdigest()
    type = data['user_type']

    if password == cpassword:
        if name and email and password and cpassword:
            q = 'SELECT * FROM users WHERE email = %s AND password = %s' 
            curs.execute(q, (email, password, ))
            res = curs.fetchone()
            if res:
                bol = 'You are already registered'
                
            else:
                q = 'INSERT INTO users (name, email, password, user_type) VALUES( %s, %s, %s, %s)'
                curs.execute(q, (name,email,cpassword,type))
                db.commit()
                bol = 'Registration successful'

    return bol

def cart_data(id):
    q = 'SELECT * FROM cart WHERE user_id = ' + str(id)
    curs.execute(q)
    res = curs.fetchall()
    if res:
        return res
    else:
        return 'cart is empty'
    
def add_to_cart(book_to_add, id):
    book_name = book_to_add['product_name']
    book_price = book_to_add['product_price']
    book_image = book_to_add['product_image']
    book_quantity = book_to_add['product_quantity']
    qu = "select * from cart where user_id = %s and name = %s"
    val = (id, book_name)
    curs.execute(qu,val)
    res = curs.fetchall()
    if res:
        c_id = res[0]
        c_id = str(c_id[0])
        q = 'UPDATE cart SET quantity = '+ book_quantity +' WHERE id = '+ c_id
        curs.execute(q)
        db.commit()
    else:
        q = "INSERT INTO cart (user_id, name, price, quantity, image) VALUES(%s, %s, %s, %s, %s)" 
        curs.execute(q,(id, book_name, book_price, book_quantity, book_image))
        db.commit()
    return True

def Update(book_to_add):
    book_id = book_to_add['cart_id']
    book_quantity = book_to_add['cart_quantity']
    q = 'UPDATE cart SET quantity = '+ book_quantity +' WHERE id = '+ book_id
    curs.execute(q)
    db.commit()
    return True