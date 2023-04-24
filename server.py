from flask import Flask, render_template, redirect, flash, request
import melons as melonScript
import jinja2

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined # for debugging purposes

## Flask Routes ##
@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/melons')
def all_melons():
    return render_template('melons.html', melon_list=melonScript.get_all_melons())

@app.route('/melon/<melon_id>')
def show_melon():
    return render_template('melon.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/add_to_cart/<melon_id>')
def add_melon_to_cart():
    return ('added melon to cart')

if __name__ == '__main__':
    app.env = 'development'
    app.run(debug = True, port = 8000, host = 'localhost')