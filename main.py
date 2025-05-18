from flask import Flask, render_template, request, redirect, url_for
from check import *
from guessing_words import cdf_test, cdf_write, cdf_list
from login_and_signin_forms import LoginForm, SigninForm
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
import re
import edge_tts
import asyncio


async def generate_speech(text, output_file="voices/v.mp3"):
    voice = "ru-RU-SvetlanaNeural"  # русский голос
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/users.db")


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/tools")
def tools():
    return render_template('tools.html')


@app.route("/in_development")
def wordbook():
    return render_template('wordbooks.html')


@app.route("/choose_wordbook", methods=['GET', 'POST'])
def wbch():
    type = request.args.get('type')
    if request.method == "POST":
        f = request.files['file']
        print(f.content_type)
        if "text" in f.content_type or "csv" in f.content_type:
            file_data = f.read()
            f = str(file_data.decode('utf-8'))
            if f.split()[0] == "слово;перевод;тег":
                cleaned_data = re.sub(r'[\r\n]+', '_', f)
                return redirect(f"{type}?dct={cleaned_data}")

    return render_template('choose_wb.html', dct=render_dicts(), type=type)


@app.route('/test', methods=['GET', 'POST'])
def test():
    print(request.args.get('dct'))
    questions = get_test(request.args.get('dct')) if len(request.args.get('dct')) < 40 else gtt(request.args.get('dct'))
    them = "пользователя" if not (request.args.get('dct') in ("test", "writing")) else ""
    FormClass = cdf_test(questions)
    form = FormClass()

    if request.method == 'POST':
        # Проверка ответов
        results = []
        score = 0

        for question in questions:
            user_answer = getattr(form, question['id']).data
            is_correct = check_answer(question, user_answer)

            if is_correct:
                score += 1

            results.append({
                'question': question['text'],
                'user_answer': user_answer,
                'is_correct': is_correct,
                'correct_answer': question['correct']
            })

        return render_template('result.html',
                               results=results,
                               score=score,
                               total=len(questions),
                               title="Результаты теста",
                               goto=f"test?dct={request.args.get('dct')}")
    if request.method == 'GET':
        if not them:
            with open("static/names_of_dicts\\" + request.args.get('dct').split(".")[0].split("\\")[1] + ".txt", "r",
                      encoding="utf-8") as f:
                them = f.readline()
        return render_template('test.html', form=form, questions=questions, title="Тест", thema=them)


@app.route('/writing', methods=['GET', 'POST'])
def writing():
    questions = get_writing(request.args.get('dct')) if len(request.args.get('dct')) < 40 else gtw(
        request.args.get('dct'))
    them = "пользователя" if not (request.args.get('dct') in ("test", "writing")) else ""
    FormClass = cdf_write(questions)
    form = FormClass()

    if request.method == 'POST':
        # Проверка ответов
        results = []
        score = 0

        for question in questions:
            user_answer = getattr(form, question['id']).data
            is_correct = check_answer(question, user_answer)

            if is_correct:
                score += 1

            results.append({
                'question': question['text'],
                'user_answer': user_answer,
                'is_correct': is_correct,
                'correct_answer': question['correct']
            })

        return render_template('result.html',
                               results=results,
                               score=score,
                               total=len(questions),
                               title="Результаты теста",
                               goto=f"writing?dct={request.args.get('dct')}")
    if request.method == 'GET':
        if not them:
            with open("static/names_of_dicts\\" + request.args.get('dct').split(".")[0].split("\\")[1] + ".txt", "r",
                      encoding="utf-8") as f:
                them = f.readline()
        return render_template('writing.html', form=form, questions=questions, title="Тест", thema=them)

#
# @app.route('/listen', methods=['GET', 'POST'])
# def listen():
#     questions = get_list(request.args.get('dct')) if len(request.args.get('dct')) < 40 else gtl(
#         request.args.get('dct'))
#     them = "пользователя" if not (request.args.get('dct') in ("test", "writing")) else ""
#     FormClass = cdf_list(questions)
#     form = FormClass()
#     for i in questions:
#         asyncio.run(generate_speech(i["text"], output_file=f"static/voices/{i['correct']}.mp3"))
#
#     if form.validate_on_submit():
#         # Проверка ответов
#         results = []
#         score = 0
#
#         for question in questions:
#             user_answer = getattr(form, question['id']).data
#             is_correct = check_answer(question, user_answer)
#
#             if is_correct:
#                 score += 1
#
#             results.append({
#                 'question': question['text'],
#                 'user_answer': user_answer,
#                 'is_correct': is_correct,
#                 'correct_answer': question['correct']
#             })
#
#         return render_template('result.html',
#                                results=results,
#                                score=score,
#                                total=len(questions),
#                                title="Результаты теста",
#                                goto=f"writing?dct={request.args.get('dct')}")
#     if request.method == 'GET':
#         if not them:
#             with open("static/names_of_dicts\\" + request.args.get('dct').split(".")[0].split("\\")[1] + ".txt", "r",
#                       encoding="utf-8") as f:
#                 them = f.readline()
#         return render_template('listen.html', form=form, questions=questions, title="Тест", thema=them)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.mail.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.mail.data,
            surname=form.surname.data,
            patr=form.patr.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/signin')
    return render_template('login.html', title='Регистрация', form=form)


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.mail.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('signin.html', title='Вход', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
