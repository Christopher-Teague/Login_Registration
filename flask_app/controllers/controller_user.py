##### Rename controller_"name" to be in line with project #####

from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.model_user import User##### Rename to match model file #####
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user = User.get_by_email({'email' : request.form['email']})

    session['uuid'] = user.id

    return redirect ('/success')



# C *************

@app.route('/register', methods = ['POST'])
def register_user():
    if not User.validate_registration(request.form):    
    
        return redirect('/')

    hashword = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashword
    }
    
    user_id = User.create_user(data)
    session['uuid'] = user_id

    return redirect("/success")


# R *************

@app.route('/success')
def success():
    
    return render_template ('success.html', user = User.get_by_id({'id': session['uuid']}))


# U *************

# @app.route('/')
# def update():
#     pass

# D *************

# @app.route('/')
# def remove():
#     pass