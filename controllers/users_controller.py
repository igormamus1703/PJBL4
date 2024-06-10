from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user.users import User
from models.user.roles import Role
from models.db import db
import flask_login
from models.user.decorators import role_required

user = Blueprint("user",__name__, template_folder="views")

@user.route('/register_user')
@flask_login.login_required
@role_required(1)  # Somente Admin
def register_user():
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user.route('/add_user', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def add_user():
    global users
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        User.save_user(role_name, username, email,password)
        return render_template("home.html")
    
@user.route('/list_users')
@flask_login.login_required
@role_required(1)  # Somente Admin
def list_users():
    users = User.get_users()
    return render_template("users.html", users=users)

@user.route('/edit_user')
@flask_login.login_required
@role_required(1)  # Somente Admin
def edit_user():
    user_id = request.args.get('user_id', None)
    user = User.query.get(user_id)
    roles = Role.get_role()
    return render_template('update_user.html', user=user, roles=roles)

@user.route('/update_user', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def update_user():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    user.username = request.form['username']
    user.email = request.form['email']
    user.role_id = request.form['role_type_']
    db.session.commit()
    users = User.get_users()
    return render_template("users.html", users=users)

@user.route('/delete_user', methods=['GET'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def delete_user():
    user_id = request.args.get('user_id', None)
    user = User.query.get(user_id)
    if user.role_id == 1:  # Verifica se o usuário é Admin
        users = User.get_users()
        return render_template("users.html", users=users, error="Admin users cannot be deleted.")
    db.session.delete(user)
    db.session.commit()
    users = User.get_users()
    return render_template("users.html", users=users)
