import csv
import codecs
def add_csv(path, data):
    with open(path, 'a', encoding='cp1251', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def check_user_register(user_id) -> bool:
    with open('PersonalData.csv', encoding='cp1251') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 0:
                break
            if row[0] == str(user_id):
                return True
        return False


def try_counter(user_id):
    with open('PersonalData.csv', 'r', encoding='cp1251') as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        #header = ("tg_id","фамилия имя","компания","должность","email","кол-во ост. попыток", "попытка 1", "попытка 2", "попытка 3")
        rows = []
        found = False

        for row in reader:
            if row[0] == str(user_id):
                attempts = int(row[5]) - 1
                row[5] = str(attempts)
                found = True
            rows.append(row)

    if found:
        with open('PersonalData.csv', 'w', newline="", encoding='cp1251') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header)
            writer.writerows(rows)

def give_attemp_index(user_id):
    with open('PersonalData.csv', encoding='cp1251') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == str(user_id):
                if row[5] == "2":
                    return "6"
                elif row[5] == "1":
                    return "7"
                elif row[5] == "0":
                    return "8"

def record_attempt(user_id, idx_attempt, attempt):
    with open('PersonalData.csv', encoding='cp1251') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            if row[0] == str(user_id):
                row[int(idx_attempt)] = str(attempt)
            rows.append(row)
    with open('PersonalData.csv', 'w', newline="", encoding='cp1251') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)
        writer.writerows(rows)

def counter_attempt(user_id):
    with open('PersonalData.csv', encoding='cp1251') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == str(user_id):
                return int(row[5])
