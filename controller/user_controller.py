from flask import render_template
from model.user import User

class UserController:
    @staticmethod
    def show_user():
        user = User(2, "Redis Grace")
        user.save()
        retrieved_user = User.get_by_id(1)
        return render_template("index.html", user=retrieved_user)
