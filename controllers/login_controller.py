from flask import Blueprint, request, render_template, flash
from models.user.users import User
from models.user.roles import Role
import flask_login
from flask_login import logout_user
from models.user.users import User
from models.user.decorators import role_required

login = Blueprint("login", __name__, template_folder="views")

"""
@login.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.validate_user(email, password)
        if user is None:
            flash('Usuário e/ou senha incorreta!')
            return render_template('login.html')
        else:
            flask_login.login_user(user)
            return render_template('home.html')
    else:
        return render_template('login.html')
"""

@login.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.validate_user(email, password)
        if user is None:
            flash('Usuário e/ou senha incorreta!')
            return render_template('login.html')
        else:
            flask_login.login_user(user)
            user_role_id = User.get_user_role(user)
            return render_template('home.html', roles=user_role_id)
    else:
        return render_template('login.html')


@login.route('/logoff')
@flask_login.login_required
@role_required(1, 2, 3)  # Todos
def logoff():
    logout_user()
    return render_template("login.html")