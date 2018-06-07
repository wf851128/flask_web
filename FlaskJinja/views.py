"""
Routes and views for the flask application.
"""

from datetime import datetime
from FlaskJinja import app
from flask import Flask, session, redirect, url_for, escape, request,render_template,make_response,jsonify,flash  
from FlaskJinja import model1
from flask_login import login_required, login_user, logout_user
import json

@app.route('/')


@app.route('/home')
@login_required
def home():
        return render_template('home.html')

@app.route('/index_v1')
def index_v1():
      return render_template('index.html')

@app.route('/about')
def about():
     return render_template('about.html',title='about',year=datetime.now().year,message='Your about page.')
  
@app.route('/contact')
def contact():
     return render_template('contact.html',title='about',year=datetime.now().year,message='Your contact page.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        abc = request.get_data()
        dict1 = json.loads(abc)
        username = dict1['username']
        password = dict1['password']

        #app.logger.debug(username)
        
        admin = model1.User.query.filter_by(user_name=username , pass_word=password).first()

        if admin is None:
              return jsonify({'status': '-1', 'errmsg': '用户名不存在！'})
        else:
              login_user(admin)
              flash('Logged in successfully.')
              #return redirect(url_for('index_v1'))
              return jsonify({'status': '0', 'url': 'home'})

    else:
        return render_template('login.html')