from flask import Flask
from controller.account_controller import UserController

app = Flask(__name__, template_folder="view")

@app.route('/')
def home():
    return UserController.show_user()

if __name__ == '__main__':
    app.run(debug=True)
