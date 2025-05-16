import csv

with open('doc.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    expensive = list(reader)


def get(i):
    with open(i, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        lst = list(map(lambda x: tuple(x.values()), reader))

    return lst


if __name__ == "__main__":
    print(get("doc.csv"))