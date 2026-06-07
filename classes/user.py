from flask_login import login_user, logout_user, login_required, current_user

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password