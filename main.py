from tinydb import TinyDB, Query
import random
from datetime import datetime

db_users = TinyDB('db_users.json')


def ifExists(name):
    q = Query()
    existing = db_users.search(q.participant == name)
    if existing:
        return True
    else:
        return False

def addUser(name):
    ifExists(name)
    if not ifExists(name):
        if name == "":
            return "Wprowadź nazwę uczestnika"
        elif name == "admin":
            max_id = max([entry.get('id', 0) for entry in db_users.all()], default=0)
            db_users.insert(
                {'participant': name, 'id': 0, 'password': 'admin2101',
                 'inLotteryPool': False, 'chosen': 'Yes'})
            return f'Uczestnik {name} został dodany do bazy'
        else:
            max_id = max([entry.get('id', 0) for entry in db_users.all()], default=0)
            db_users.insert({'participant': name, 'id': max_id+1, 'password': 'wigilia'+str(random.randint(1000, 9999)), 'inLotteryPool': True, 'chosen': ''})
            return f'Uczestnik {name} został dodany do bazy'
    else:
        return (f'ERROR: Uczestnik {name} istnieje już w bazie danych')


def removeUser(name):
    get = Query()
    if not ifExists(name):
        return "Brak wskazanego uczestnika"
    else:
        db_users.remove(get.participant == name)
        return f'Uczestnik {name} został usunięty z bazy danych'

def clearDatabase():
    db_users.truncate()
    db_users.insert(
        {'participant': 'admin', 'id': 0, 'password': 'admin2101',
         'rolled': True, 'chosen': 'Yes'})



def addedUsers():
    all = db_users.all()
    list = ''
    for n in all:
        list = list + str(n) + '\n'
    return list

def roll(user):
    get = Query()
    if db_users.get(get.participant == user)['chosen'] == '':
        lotteryPool = db_users.search(get.inLotteryPool == True)
        if len(lotteryPool) < 3:
            leftover = db_users.search((get.chosen == '') & (get.inLottery == True) & (get.participant != user))
            if len(leftover) > 0:
                chosenName = leftover[0]['participant']
                db_users.update({'chosen': chosenName}, get.participant == user)
                db_users.update({'inLotteryPool': False}, get.participant == chosenName)
                return chosenName
            else:
                random.shuffle(lotteryPool)
                chosen = lotteryPool[0]
                chosenName = chosen['participant']
                while chosenName == user:
                    random.shuffle(lotteryPool)
                    chosen = lotteryPool[0]
                    chosenName = chosen['participant']
                else:
                    db_users.update({'chosen': chosenName}, get.participant == user)
                    db_users.update({'inLotteryPool': False}, get.participant == chosenName)
                return chosenName
        else:
            random.shuffle(lotteryPool)
            chosen = lotteryPool[0]
            chosenName = chosen['participant']
            while chosenName == user:
                random.shuffle(lotteryPool)
                chosen = lotteryPool[0]
                chosenName = chosen['participant']
            else:
                db_users.update({'chosen': chosenName}, get.participant == user)
                db_users.update({'inLotteryPool': False}, get.participant == chosenName)
            return chosenName
    else:
        chosenName = db_users.get(get.participant == user)['chosen']
        return chosenName
roll('Szymon Pietrowski')

def tillChristmas():
    current_year = datetime.now().year
    christmas_time = datetime(current_year, 12, 24, 18, 0)
    now = datetime.now()
    time_difference = christmas_time - now
    return time_difference.days
