import csv
import random
from random import choices, shuffle
import pprint
import os
import io

dicts = 'static/dicts'
names = 'static/names_of_dicts'

with open('static/dicts/fruits.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    expensive = list(reader)


def get(i):
    with open(i, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        lst = list(map(lambda x: tuple(x.values()), reader))

    return lst


def gt(i):
    i = i.replace("_", "\n")
    csvfile = io.StringIO(i)
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    lst = list(map(lambda x: tuple(x.values()), reader))
    return lst


def get_test(i):
    lst = get(i)
    retlst = []
    variants = list(map(lambda x: x[0], lst))
    newv = variants[::]
    for id, i in enumerate(lst):
        del newv[id]
        vars = [i[0]] + random.sample(newv, k=3)
        shuffle(vars)
        newv = variants[::]
        dct = {
            "id": "t" + str(id),
            "text": f"Выберете верный вариант перевода слова {i[1]}",
            "choices": vars,
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def get_writing(i):
    lst = get(i)
    retlst = []
    for id, i in enumerate(lst):
        dct = {
            "id": "t" + str(id),
            "text": f"Напишите перевод слова {i[1]}",
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def get_list(i):
    lst = get(i)
    retlst = []
    for id, i in enumerate(lst):
        dct = {
            "id": "t" + str(id),
            "text": i[1],
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def gtl(i):
    lst = gt(i)
    retlst = []
    for id, i in enumerate(lst):
        dct = {
            "id": "t" + str(id),
            "text": i[1],
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def gtw(i):
    lst = gt(i)
    retlst = []
    for id, i in enumerate(lst):
        dct = {
            "id": "t" + str(id),
            "text": f"Напишите перевод слова {i[1]}",
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def gtt(i):
    lst = gt(i)
    retlst = []
    variants = list(map(lambda x: x[0], lst))
    newv = variants[::]
    for id, i in enumerate(lst):
        del newv[id]
        vars = [i[0]] + random.sample(newv, k=3)
        shuffle(vars)
        newv = variants[::]
        dct = {
            "id": "t" + str(id),
            "text": f"Выберете верный вариант перевода слова {i[1]}",
            "choices": vars,
            "correct": i[0]
        }
        retlst.append(dct)
    return retlst


def check_answer(question, user_answer):
    correct = question['correct']
    return user_answer == correct


def render_dicts():
    lst_names = []
    uts = []
    for id, item in enumerate(os.listdir(names)):
        full_path = os.path.join(names, item)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                inf = f.read().split("\n")
                lst_names.append((inf[0], "\n".join(inf[1:])))

    for id, item in enumerate(os.listdir(dicts)):
        full_path = os.path.join(dicts, item)
        if os.path.isfile(full_path):
            uts.append((lst_names[id], full_path))
    return uts


if __name__ == "__main__":
    pprint.pprint(render_dicts())
