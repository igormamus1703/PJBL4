from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role_id in roles:
                return func(*args, **kwargs)
            return redirect(url_for('login.logoff'))
        return decorated_view
    return decorator
