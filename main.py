from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3
from datetime import date

app = Flask('app')
app.debug = True
app.secret_key = "string"

usercart = []

@app.route('/home', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    username = request.form["user"] # email
    password = request.form["pass"]
    print(username + " " + password)
    session['username'] = request.form["user"] #wanna use session variables to store cart info
    session['cart'] = []

    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT email, password FROM users WHERE email  = \"" + username + "\" AND password = \"" + password + "\"")
    data = cursor.fetchall()
    print(data)
    if not data:
      session.pop('username', None)
      session.pop('cart', None)
      session.clear()
      return render_template("login.html", error = "This user is not in the database")
    else:
      if 'username' in session:
        connection1 = sqlite3.connect("myDatabase.db")
        cursor1 = connection1.cursor()
        cursor1.execute("SELECT * FROM product")
        product_data = cursor1.fetchall()
        return render_template("home.html", products = product_data)
      
  # Display the correct information for a logged in user 
  connection1 = sqlite3.connect("myDatabase.db")
  cursor1 = connection1.cursor()
  cursor1.execute("SELECT * FROM product")
  product_data = cursor1.fetchall()
  return render_template("home.html", products = product_data)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  if request.method == "POST":
    if request.form["checkout"] == "check out":
      total = 0
      # For giving any initial quantity errors
      for i in session['cart']:
        #grab user quantity of this specific item
        quantity1 = 0
        for j in session['cart']:
          if j[0] == i[0]:
            quantity1 += 1
        
        # Grab stock of specific item
        connection = sqlite3.connect("myDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT stock FROM product WHERE id = " + str(i[0]))
        quantity = cursor.fetchall()
        connection.close()

        #gives the error if quantity is 0
        if (quantity[0][0] - quantity1) < 0:
          return redirect("/carterror")
        
      #grab the most recent ID and increment it for a new order ID
      connection_id = sqlite3.connect("myDatabase.db")
      cursor_id = connection_id.cursor()
      cursor_id.execute("SELECT order_id FROM user_order ORDER BY order_id DESC")
      id_arr = cursor_id.fetchall()
      connection_id.close()
      new_id = id_arr[0][0] + 1

      for i in session['cart']:
        # Grab stock of specific item
        connection = sqlite3.connect("myDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT stock FROM product WHERE id = " + str(i[0]))
        quantity = cursor.fetchall()
        connection.close()

        #Update stock of product
        connection2 = sqlite3.connect("myDatabase.db")
        cursor2 = connection2.cursor()
        cursor2.execute("UPDATE product SET stock = " + str(quantity[0][0] - 1) + " WHERE id = " + str(i[0]))
        connection2.commit()
        connection2.close()
        
      previous_id = 0
      for i in session['cart']:
        if i[0] != previous_id:
          #grab user quantity of this specific item
          quantity1 = 0
          for j in session['cart']:
            if j[0] == i[0]:
              quantity1 += 1

          # Inserting order into database
          connection3 = sqlite3.connect("myDatabase.db")
          cursor3 = connection3.cursor()
          cursor3.execute("SELECT price FROM product WHERE id = " + str(i[0]))
          price = cursor3.fetchall()
          total += price[0][0] * quantity1
          connection3.close()

          connection5 = sqlite3.connect("myDatabase.db")
          cursor5 = connection5.cursor()
          cursor5.execute("INSERT INTO orderitem VALUES (" + str(new_id) + ", \'" + session['username'] + "\', \'" + str(date.today()) + "\', " + str(i[0]) + ", " + str(quantity1) + ")")
          connection5.commit()
          connection5.close()
          previous_id = i[0]
      
      # overall order and total price, add in at end
      connection4 = sqlite3.connect("myDatabase.db")
      cursor4 = connection4.cursor()
      cursor4.execute("INSERT INTO user_order VALUES (" + str(new_id) + ", \'" + session['username'] + "\', \'" + str(date.today()) + "\', " + str(total) + ")")
      connection4.commit()
      connection4.close()

      #clear cart after looping ?? idk if this works rn
      if 'cart' in session:
        session.pop('cart', None)
        session['cart'] = []
        usercart = []
  return render_template("checkout.html")

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    if request.form['logout'] == "log out":
      session.pop('username', None)
      session.pop('cart', None)
      session['cart'] = []
      session.clear()
      return redirect("/")
  connection1 = sqlite3.connect("myDatabase.db")
  cursor1 = connection1.cursor()
  cursor1.execute("SELECT * FROM product")
  product_data = cursor1.fetchall()
  return render_template("index.html", products = product_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
  #Make sure to find if the email alr exists
  if request.method == 'POST':
    new_email = request.form['email']
    new_name = request.form['name']
    new_pass = request.form['password']
    connection1 = sqlite3.connect("myDatabase.db")
    cursor1 = connection1.cursor()
    cursor1.execute("SELECT email FROM users WHERE email = \'" + new_email + "\'")
    data = cursor1.fetchall()
    connection1.close()
    if data:
      return render_template("login.html", error = "There is already an account with that email. Please try again.")

    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (\'" + new_email + "\', \'" + new_name + "\', \'" + new_pass + "\')")
    connection.commit()
    connection.close()
    return render_template("login.html", error = "Account created successfully")
  return render_template("login.html")

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
   return render_template("create_account.html")

# LOGGED OUT PAGES
@app.route('/switch', methods=['GET', 'POST'])
def switch():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'Nintendo Switch'")
  data = cursor.fetchall()
  print(data)
  return render_template("switch.html", products = data)

@app.route('/playstation', methods=['GET', 'POST'])
def playstation():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'PlayStation 5'")
  data = cursor.fetchall()
  print(data)
  return render_template("playstation.html", products = data)

@app.route('/pc', methods=['GET', 'POST'])
def pc():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'PC'")
  data = cursor.fetchall()
  print(data)
  return render_template("pc.html", products = data)

# LOGGED IN PAGES
@app.route('/switch_home', methods=['GET', 'POST'])
def switch_logged_in():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'Nintendo Switch'")
  data = cursor.fetchall()
  print(data)
  if 'username' in session:
    return render_template("switch_home.html", products = data)
  return render_template("switch.html", products = data)

@app.route('/playstation_home', methods=['GET', 'POST'])
def playstation_logged_in():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'PlayStation 5'")
  data = cursor.fetchall()
  print(data)
  if 'username' in session:
    return render_template("playstation_home.html", products = data)
  return render_template("playstation.html", products = data)

@app.route('/pc_home', methods=['GET', 'POST'])
def pc_logged_in():
  connection = sqlite3.connect("myDatabase.db")
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product WHERE cat = 'PC'")
  data = cursor.fetchall()
  print(data)
  if 'username' in session:
    return render_template("pc_home.html", products = data)
  return render_template("pc.html", products = data)

# CART
@app.route('/cart', methods=['GET', 'POST'])
def cart():
  if request.method == 'POST':
    if 'cart' in session:
      if 'username' in session:
        try:
          if request.form["add"]:
            usercart.append(request.form["add"])
            print(usercart)
        except KeyError:
          print("No")
        try:
          if request.form["delete"]:
            usercart.remove(request.form["delete"])
            print(usercart)
        except KeyError:
          print("No")
        data = []
        for i in usercart:
          connection = sqlite3.connect("myDatabase.db")
          cursor = connection.cursor()
          cursor.execute("SELECT * FROM product WHERE id = " + i)
          data += cursor.fetchall()
        session['cart'] = data
  return render_template("cart.html")

@app.route('/carterror', methods=['GET', 'POST'])
def carterror():
  return render_template("carterror.html")

#Searches
@app.route('/searchresult', methods=['GET', 'POST'])
def searchresult():
  if request.method == 'POST':
    searchquery = request.form["search"]
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product WHERE title LIKE \"%" + searchquery + "%\"")
    data = cursor.fetchall()
    if data:
      return render_template("searchresult.html", products = data)
  return render_template("searchresult.html", products = [])

@app.route('/search', methods=['GET', 'POST'])
def search():
  return render_template("search.html")

@app.route('/searchresult_notloggedin', methods=['GET', 'POST'])
def searchresult_notloggedin():
  if request.method == 'POST':
    searchquery = request.form["search"]
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product WHERE title LIKE \"%" + searchquery + "%\"")
    data = cursor.fetchall()
    if data:
      return render_template("searchresult_notloggedin.html", products = data)
  return render_template("searchresult_notloggedin.html", products = [])

@app.route('/search_notloggedin', methods=['GET', 'POST'])
def search_notloggedin():
  return render_template("search_notloggedin.html")

#Order History
@app.route('/orderhistory', methods=['GET', 'POST'])
def orderhistory():
  if 'username' in session:
    connection = sqlite3.connect("myDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_order WHERE customer_email = \'" + session['username'] + "\'")
    order_data = cursor.fetchall()
    connection.close()

    connection1 = sqlite3.connect("myDatabase.db")
    cursor1 = connection1.cursor()
    cursor1.execute("SELECT * FROM orderitem WHERE customer_email = \'" + session['username'] + "\'")
    temp = cursor1.fetchall()

    data2 = ""
    data = []
    datadata = []
    if temp:
      current_id = temp[0][0]
    i = 0
    while (i < len(temp)):
      if current_id == temp[i][0]:
        connection2 = sqlite3.connect("myDatabase.db")
        cursor2 = connection2.cursor()
        cursor2.execute("SELECT title FROM product WHERE id = " + str(temp[i][3]))
        temp_data = cursor2.fetchall()
        data2 += temp_data[0][0] + " (" + str(temp[i][4]) + ")"
        i += 1
        data.append(data2)
        data2 = ""
        if i == len(temp):
          i -= 1
          correct_array = []
          for j in order_data:
            if j[0] == current_id:
              correct_array = j
          new_arr = [data, temp[i][2], correct_array[3]]
          datadata.append(new_arr)
          data = []
          current_id = temp[i][0]
          i += 1
      else:
        correct_array = []
        for j in order_data:
          if j[0] == current_id:
            correct_array = j
        new_arr = [data, temp[i][2], correct_array[3]]
        datadata.append(new_arr)
        data = []
        current_id = temp[i][0]

    print(datadata)

    return render_template("orderhistory.html", orders = datadata)
  return render_template("orderhistory.html", orders = [])

app.run(host='0.0.0.0', port=8080)
