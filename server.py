from flask import Flask, render_template, redirect, flash, request, session
from forms import LoginForm
import melons as melonScript
import customers as customerScript
import jinja2


app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined # for debugging purposes
app.secret_key = 'dev'

## Flask Routes ##
@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/melons')
def all_melons():
    return render_template('melons.html', melon_list=melonScript.get_all_melons())

@app.route('/melon/<melon_id>')
def show_melon(melon_id):
    return render_template('melon.html', melon=melonScript.get_melon_by_id(melon_id))

@app.route('/cart')
def show_cart():
    order_total = 0
    cart_melons = []
    
    # get cart dict from session (or an empty one if none exists yet)
    cart = session.get('cart', {})
    
    for melon_id, quantity in cart.items():
        melon = melonScript.get_melon_by_id(melon_id)
        
        total_cost = quantity * melon.price
        order_total += total_cost
        
        melon.quantity = quantity
        melon.total_cost = total_cost
        
        cart_melons.append(melon)
    
    return render_template('cart.html', cart_melons=cart_melons, order_total=order_total)

@app.route('/add_to_cart/<melon_id>')
def add_melon_to_cart(melon_id):
    if 'username' not in session:
        return redirect('/login')
    
    session.setdefault('cart', {}).setdefault(melon_id, 0)
    session['cart'][melon_id] += 1
    cart = session['cart']
    session.modified = True
    flash(f'Melon {melon_id} successfully added to cart.')
    return redirect('/cart')

@app.route('/empty_cart')
def empty_cart():
    session['cart'] = {}
    
    return redirect('/cart')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        # user input data
        username = form.username.data
        password = form.password.data
        
        user = customerScript.get_by_username(username)
        
        if not user or user['password'] != password:
            flash('Incorrect password')
            return redirect('/login')
        
        # store username in session to keep track of loggin in user
        session['username'] = user['username']
        flash('Successfully Loggedn In!')
        return redirect('/melons')
    
    # form has not been submitted or data was not valid
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    del session['username']
    flash('Successfully Logged Out!')
    return redirect('/login')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.env = 'development'
    app.run(debug=True, port=8000, host='localhost')