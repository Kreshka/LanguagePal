from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/tools")
def tools():
    return render_template('tools.html')


@app.route("/tools/training")
def training():
    return render_template('training1.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['pre-password'])
        print(request.form['name'])
        print(request.form['surname'])
        print(request.form['midname'])
        return "Форма отправлена"


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
