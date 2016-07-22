from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def login(self):
        data = request.form
        check = self.models["User"].login(data)
        if check:
            session["id"] = check["id"]
            return self.load_view("in.html")
        else:
            flash("Email or password not found")
            return redirect("/")

    def register(self):
        data = request.form
        check = self.models["User"].register(data)
        if check["status"]:
            session["id"] = check["id"]
            return self.load_view("in.html")
        else:
            for message in check["errors"]:
                flash(message)
            return redirect("/")
