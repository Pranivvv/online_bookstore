from flask import Flask, render_template, jsonify, request, session
from database import load_books, Login, register_db, cart_data, add_to_cart, Update
import pandas as pd

app = Flask(__name__)
app.secret_key="bookstore"

# load_books()

@app.route('/')
def start():
    return render_template("login.html")

@app.route('/home')
def home():
    books = load_books()
    var = "False"
    return render_template("home.html", books = books)

@app.route('/login', methods = ['GET','POST'] )
def login():
    if request.method == 'POST':
        data = request.form
        res = Login(data)
        print(res)
        if res:
            session['loggedin'] = True
            session['id'] = res[0]
            id = session['id']
            session['email'] = res[2]
            session['name'] = res[1]
            result = cart_data(id)
            res_count = len(result)
            session['items_in_cart'] = res_count
            type = res[4]
            if type == 'admin':
                var = "True"
                return render_template("admin_page.html", name = session['name'], email = session['email'], items_cart = session['items_in_cart'], no_of_items_in_cart = session['items_in_cart'] )
            else:
                var = "True"
                return render_template("home.html",name = session['name'], email = session['email'], books = load_books(), no_of_items_in_cart = session['items_in_cart'] )
        else:
            return render_template("login.html",bol = 'Invalid Email or Password', name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )
    else:
        return render_template("login.html", bol = "")

@app.route('/logout')
def logout():
    books = load_books()
    return render_template("login.html", bol = "")

@app.route('/Register')
def Register():
    return render_template("register.html", bol='', name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/register', methods = ['post'])
def register():
    data = request.form
    res = register_db(data)
    return render_template('register.html',bol = res, name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/orders')
def orders():
    return render_template("orders.html", name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/search_page')
def search_page():
    return render_template("search_page.html", name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/cart')
def cart():
    id = session['id']
    carts = cart_data(id)
    res_count = len(carts)
    session['items_in_cart'] = res_count
    total = 0
    for cart in carts:
        total = total + cart[3] * cart[4]
    return render_template("cart.html",carts = carts, total = total, name = session['name'], email = session['email'],no_of_items_in_cart = session['items_in_cart'] )

@app.route('/about')
def about():
    return render_template("about.html", name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/contact')
def contact():
    return render_template("contact.html", name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/shop')
def shop():
    books = load_books()
    return render_template("shop.html", books = books, name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/add_cart', methods = ['GET', 'POST'])
def add_cart():
    book_to_add = request.form
    id = session['id']
    res = add_to_cart(book_to_add, id)
    if res:
        carts = cart_data(id)
        res_count = len(carts)
        session['items_in_cart'] = res_count
        total = 0
        for cart in carts:
            total = total + cart[3] * cart[4] 
        return render_template("cart.html",carts = carts, total = total, name = session['name'], email = session['email'],no_of_items_in_cart = session['items_in_cart'] )
    else:
        books = load_books()
        return render_template("shop.html", books = books, name = session['name'], email = session['email'], no_of_items_in_cart = session['items_in_cart'] )

@app.route('/update', methods = ['POST'])
def update():
    book_to_add = request.form
    res = Update(book_to_add) 
    if res:
        carts = cart_data(id)
        res_count = len(carts)
        session['items_in_cart'] = res_count
        total = 0
        for cart in carts:
            total = total + cart[3] * cart[4] 
        return render_template("cart.html",carts = carts, total = total, name = session['name'], email = session['email'],no_of_items_in_cart = session['items_in_cart'] )
    else:
        carts = cart_data(id)
        res_count = len(carts)
        session['items_in_cart'] = res_count
        total = 0
        for cart in carts:
            total = total + cart[3] * cart[4] 
        return render_template("cart.html",carts = carts, total = total, name = session['name'], email = session['email'],no_of_items_in_cart = session['items_in_cart'] )

@app.route('/admin_page')
def admin_page():
    return render_template("admin_page.html")

@app.route('/admin_products')
def admin_products():
    return render_template("admin_products.html")

@app.route('/admin_orders')
def admin_orders():
    return render_template("orders.html")

@app.route('/admin_users')
def admin_users():
    return render_template("admin_users.html")

@app.route('/admin_contacts')
def admin_contacts():
    return render_template("admin_contact.html")

# @app.route('/admin_page')
# def admin_page():
#     return render_template("admin_page.html")

# @app.route('/admin_page')
# def admin_page():
#     return render_template("admin_page.html")
if __name__ == "__main__":
    app.run(debug=True, port=3000)  

