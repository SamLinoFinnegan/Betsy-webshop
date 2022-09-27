__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from db import *
from models import *
from hashlib import sha3_512
from flask import Flask, render_template, redirect, request, session, url_for, flash
import os
from difflib import get_close_matches




app = Flask(__name__)

app.secret_key = os.urandom(16)
session 

def hash_password(password):
    return sha3_512(password.encode("utf-8")).hexdigest()

def search(product):
    bg_ls_words =[]

    # find if the query has more then one word
    # if it does we will compare it against the full name of the products
    # if it doesnt we will break each product name to compare each one

    if len(product.split(" ")) > 1:
        bg_ls_words = [x.name for x in Product.select()]
    else:
        bg_ls_words = [word for sublist in Product.select() for word in sublist.name.split(" ")]
             
    close_word = get_close_matches("".join(product.split(" ")), bg_ls_words, n=1)
    
    items = Product.select().where(Product.name.contains(close_word[0]))
    my_list = []
    for item in items:
        item_str = "{}, {}".format(item.id, item.name.capitalize())
        my_list.append(item_str)
    return my_list

def list_user_products(user_name):
    my_products = []
    user_products= Product.select().join(User).where(User.name == get_close_matches("".join(user_name.split(" ")), [user.name for user in User.select()], n=1))
    for product in user_products:
        item_str = "{}, {}".format(product.id, product.name.capitalize())
        my_products.append(item_str)
    return my_products



def list_products_per_tag(tag_id):
    all_products = Product.select()
    my_list = []
    for item in all_products:
        for product_tag in item.tag:
            if product_tag.name == get_close_matches(tag_id, [tag.name for item in Product.select() for tag in item.tag], n=1)[0]:

                item_str = "{}, {}".format(item.id, item.name.capitalize())

                my_list.append(item_str)
    return my_list


def add_product_to_catalog(user_name, product, d, p, q, t):
    price = "{}".format(round(float(p), 2))
    user_obj = User.select().where(User.name == user_name.lower())
    item = Product.create(name=product, description=d, price=price, quant=q, user=user_obj)
    item.tag.add(Tag.get(Tag.name == t))

def update_stock(product_id, quantity):
    item = Product.get(Product.id == product_id)
    item.quant = quantity
    item.save() 
    if item.quant == 0:
        item.delete_instance()
    
    return item


def remove_product(product_id):
    product = Product.get(Product.id == product_id)
    product.delete_instance()

def purchase_product(product_id, buyer_id, quantity=0):
    product = Product.get(Product.id == product_id)
    buyer = User.get(User.id == buyer_id)
    quant = int(quantity)
    if product.quant >= quant:
        new_quant = product.quant - quant
        
        update_stock(product.id, new_quant)
        if product.quant == 0:
            remove_product(product.id)
        Transaction.create(user=buyer, product=product, quant=quantity)
        new_product = Product.create(name=product.name, description=product.description, price=product.price, quant=quant, user=buyer)
        new_product.tag.add([tag.id for tag in product.tag])
        new_product.save()
    else:
        error = "You dont have enought in your stock"
###############################################################
#flask app


@app.route("/signup", methods=["GET", "POST"])
def signup(name="sign up"):
    if request.method == "POST":
        user = request.form["new_user"]
        addre = request.form["address"]
        bill = request.form["billing"]
        password =request.form["new_password"]
        re_password = request.form["re_password"]
        if password == re_password:
            session["user"] = user

            hash_pass = hash_password(password)
            User.create(name=user.lower(), address=addre, billing=bill, password=hash_pass)
            return redirect(url_for("index"))
    return render_template("signup.html", title=name)


@app.route("/login", methods=["GET", "POST"])
def log_in(name="Log In"):
    error = None
    if request.method == "POST":
        try:
            user = request.form["user_name"]
            password = request.form["user_password"]
            
            if user.lower() in [user.name for user in User.select()]:
                
                for registered_user in User.select():
                    if registered_user.name == user and registered_user.password == hash_password(password):
                        flash('You were successfully logged in')
                        session["user"] = user
                        users = User.select()
                        return redirect(url_for("index"))
                        
                else:
                    flash("Invalid credentials")
                        
            else:
                flash("User not in our database")
                return redirect(url_for("signup"))
        except Exception as e:
            flash(e)
    return render_template("login.html", title=name)

@app.route("/logout")
def log_out():
    session.clear()
    flash("You have been successfuly logged out")
    return redirect(url_for("log_in"))


@app.route("/", methods=["GET", "POST"])
def index(name="Index"):
    if "user" in session:
        user = session["user"]
        user_name_list = []
        error = None
        for users in User.select():
            user_name_list.append(users.name.capitalize())
        if request.method == "POST":
            try:

                if request.form["option"] == "product":
                    product = request.form["item"]

                    error = "Havent found any products"


                    my_item = search(str(product))

                    return redirect(url_for("store", item=my_item))

                elif request.form["option"] == "user":
                    search_user = request.form["item"]

                    error = "Havent found user in database"

                    user_items = list_user_products(str(search_user))

                    

                    return redirect(url_for("store", item=user_items))
                elif request.form["option"] == "tag":
                    tag = request.form["item"]

                    error = "Havent found that tag"

                    list_pro_tag = list_products_per_tag(str(tag))
                    
                    return redirect(url_for("store", item=list_pro_tag))
            
            except Exception as e:
                flash(e)
                flash(error)

                return render_template("index.html", user_name=user, title=name, users=user_name_list)
    else:
        return redirect(url_for("signup"))
    
    
    return render_template("index.html", user_name=user, title=name, users=user_name_list)

@app.route("/store")
def store(name="Store"):
    if "user" in session:
        user = session["user"]
        try:
            str_item = request.args.getlist("item")
            item_list = []
            for each in str_item:

                item_list.append(list(each.split(", ")))
            return render_template("store.html", title=name, items=item_list)
        except Exception as e:
            flash(e)
            return redirect(url_for("index"))
    else:
        return redirect(url_for("signup"))

@app.route("/product_page/<id>", methods=["GET", "POST"])
def product_page(id):
    if "user" in session:
        user_str = session["user"]
        try:
            user_obj = User.get(User.name == user_str)
            product = Product.get(Product.id == id)
            if request.method == "POST":
                quant = request.form["product_buy_quantity"]
                purchase_product(product.id, user_obj.id, quant)
        except Exception as e:
            flash(e)
    else:
        return redirect(url_for("log_in"))
    return render_template("product_page.html", product=product, title="Product Page")

@app.route("/profile", methods=["GET", "POST"])
def user_profile(name="My Profile"):
    if "user" in session:
        user = session["user"]
        try:
            if request.method == "POST":
                prod_name = request.form["product_name"]
                desc = request.form["description"]
                pr = request.form["price"]
                quant = request.form["quantity"]
                tag = request.form["tag"]
                add_product_to_catalog(user, prod_name, desc, pr, quant, tag)
            
            user_object = User.get(User.name == user.lower())
            user_items = list_user_products(user.lower())
            item_list = []
            for each in user_items:

                item_list.append(list(each.split(", ")))
        except Exception as e:
            flash(e)
    return render_template("user_profile.html", title=name, user_obj=user_object, products=item_list)


@app.route("/my_product_page/<id>", methods=["GET", "POST"])
def my_product_page(id):
    if "user" in session:
        user = session["user"]
        
        product = Product.get(Product.id == id)
        if request.method == "POST":
            try:
                if "remove" in request.form:
                    remove_product(product.id)
                    flash("Your product has been successfully removed")
                    return render_template("my_product_page.html", title = product.name, my_product=product)
                if "quantity" in request.form:
                    quant = request.form["quantity"]
                    update_stock(product.id, quant)
                    flash("Your inventory has been updated")
                    return render_template("my_product_page.html", title = product.name, my_product=product)
            except Exception as e:  
                flash(e)
                        
        return render_template("my_product_page.html", title = product.name, my_product=product)

    else:
        return redirect(url_for("signup"))



betsy_db.close()

if __name__ == "__main__":
    app.run()