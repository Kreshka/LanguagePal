import csv
import random

with open('doc.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    expensive = list(reader)


def dictation_eng(tegs=(), all_words=len(expensive)):
    if not tegs:
        score = 0
        wrong_words = []
        random.shuffle(expensive)
        for record in expensive[:all_words]:
            i = input(record["перевод"] + "\n")
            if i == record["слово"]:
                score += 1
            else:
                wrong_words.append((i, record["слово"]))
        print(score, "\nWrong answers:")
        if wrong_words:
            for i in wrong_words:
                print(f"You write: {i[0]}\nRight answer: {i[1]}")
        else:
            print("All's correct!! Very good")
    else:
        score = 0
        wrong_words = []
        random.shuffle(expensive)
        ex = list(filter(lambda x: x["тег"] in tegs, expensive))
        for record in ex[:all_words]:
            i = input(record["перевод"] + "\n")
            if i == record["слово"]:
                score += 1
            else:
                wrong_words.append((i, record["слово"]))
        print(score, "\nWrong answers:")
        if wrong_words:
            for i in wrong_words:
                print(f"You write: {i[0]}\nRight answer: {i[1]}")
        else:
            print("All's correct!! Very good")


dictation_eng(tegs=("фрукты"), all_words=5)