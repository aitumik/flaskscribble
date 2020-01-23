##initialization
from flask import Flask,request,make_response,redirect
from flask_script import Manager
app = Flask(__name__)

manager = Manager(app)

@app.route("/")
def home():
    # browser = request.headers.get("User_Agent")
    # print(browser)
    # return "<h1>Your browser is {}</h1>".format(browser)

    # response = make_response("<h1>This doc contains cookie</h1>")
    # response.set_cookie("answ",'42')


    return "<h1>Home page</h1>"


@app.route("/user/<name>")
def user(name):
    return "Hello {}".format(name)

if __name__ == "__main__":
    manager.run()


