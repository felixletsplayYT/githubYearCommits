from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from hashlib import sha256
from connection.ConnectionManager import CommitConnection
from connection.ConnectionManager import DatabaseController
from datetime import datetime
import operator

app = Flask(__name__)
# not needed but I am afraid deleting it.
users = list()
timeUpdated = 0


@app.route('/', methods=['GET'], defaults={"reload": False})
@app.route('/force', methods=['GET'], defaults={"reload": True})
def main_page(reload):
    global timeUpdated
    global users
    year = datetime.now().strftime("%Y")
    if (reload and (DatabaseController.get_setting("allow-force") == "true" or
                    request.cookies.get("gyc_login") == DatabaseController.getPassword())) or\
            datetime.now().timestamp() - timeUpdated > DatabaseController.get_setting("cache"):
        users = list()
        timeUpdated = datetime.now().timestamp()
        user_contributions = {}
        for user in DatabaseController.get_user():
            user_contributions.update({user[0]: CommitConnection.getCommitsInYear(year, user[0])})
        sorted_contributions = sorted(user_contributions.items(), key=operator.itemgetter(1), reverse=True)
        for user in sorted_contributions:
            users.append({"name": user[0], "contributions": user[1]})

    # users.append({"name": user[0], "contributions": CommitConnection.getCommitsInYear(year, user[0])})
    # users.append(
    # users.append({"name": "robmroi03", "contributions": CommitConnection.getCommitsInYear(year, "robmroi03")})
    #    {"name": "felixletsplayyt", "contributions": CommitConnection.getCommitsInYear(year, "felixletsplayyt")})
    resp = make_response(render_template("index.html.twig", users=users, time=datetime.fromtimestamp(timeUpdated)
                                         .strftime('%H:%M:%S')))
    resp.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    resp.headers['Pragma'] = "no-cache"
    resp.headers['Expires'] = "0"
    return resp


@app.route('/login', methods=['GET'])
@app.route('/backend', methods=['GET', 'POST'])
def backend():
    if request.method == "GET":
        if request.cookies.get("gyc_login") == DatabaseController.getPassword():
            resp = make_response(render_template("backend.html.twig", users=DatabaseController.get_user()))
            return resp
        else:
            resp = make_response(render_template("login.html.twig"))
            resp.delete_cookie("gyc_login")
            return resp
    else:
        if request.cookies.get("gyc_login") == DatabaseController.getPassword():
            if request.form.get("delete") is not None:
                DatabaseController.remove_user(request.form.get("delete"))
            if request.form.get("username") is not None:
                DatabaseController.add_user(request.form.get("username"))
            if request.form.get("setting") is not None:
                if request.form.get("setting") == "password":
                    hashed = sha256(request.form.get("value").encode()).hexdigest()
                    DatabaseController.set_setting("password", hashed)
                else:
                    DatabaseController.set_setting(request.form.get("setting"), request.form.get("value"))
            return '<html><head><meta http-equiv="refresh" content="0; url=/login" /></head></html>'


if __name__ == '__main__':
    app.run()
