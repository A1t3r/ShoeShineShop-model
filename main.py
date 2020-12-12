C_SIZE = 100

_lambda = 5  # интенсивность прихода требования
_ksi = 8  # интенсивность обслуживания

logger_dict = {
    'Entrance time': [],
    'Exit time': [],
    'Time on the first chair': [],
    'Time in queue': [],
    'Time on the second chair': []
}

logger_list = []


class Client:
    id = None
    entrance_time = None
    exit_time = None
    time_on_the_first_chair = None
    time_on_the_second_chair = None
    time_in_queue = 0

    def __init__(self, _id, _entrance_time):
        self.id = _id
        self.entrance_time = _entrance_time

    def give_info(self):
        return [self.id, self.entrance_time, self.time_on_the_first_chair,
                self.time_on_the_second_chair, self.time_in_queue, self.exit_time]


cur_clients = {
    'first chair': Client,
    'second chair': Client
}


class Chair_1:
    entrance_time = None
    exit_time = None
    is_busy = False

    def __init__(self):
        pass

    def serving(self, timerl):
        if timerl != 0 and timerl % _ksi == 0:
            self.exit_time = timerl
            return True
        return False


class Chair_2:
    entrance_time = None
    exit_time = None
    is_busy = False

    def __init__(self):
        pass

    def serving(self, _timer):
        if _timer != 0 and _timer % _ksi == 0:
            self.exit_time = _timer
            return True
        return False


chair1 = Chair_1
chair2 = Chair_2
served = False
served2 = False
Added = False

clients = []
timer = 0
gl_id = 0
ex_time = 0

# while timer < C_SIZE:
for timer in range(C_SIZE):

    if timer % _lambda == 0 and not chair1.is_busy:  # Поступление запроса Если занят первый стул то запрос отклоняется
        clients.append(Client(gl_id, timer))
        Added = True
        gl_id += 1
    else:
        Added = False

    if len(clients) != 0:

        if not chair1.is_busy and Added:  # Иначе начинаем обслуживание
            chair1.is_busy = True
            chair1.entrance_time = timer
            cur_clients['first chair'] = clients[len(clients) - 1]  # Запоминаем кого посадили для логгирования

        if timer % _ksi == 0 and timer != 0 and chair1.is_busy:
            chair1.exit_time = timer
            ex_time = timer
            cur_clients['first chair'].time_on_the_first_chair = chair1.exit_time - chair1.entrance_time
            served = True
            chair1.is_busy = False

        if (timer - ex_time) % (_ksi-1) == 0 and chair2.is_busy:
            chair2.exit_time = timer
            cur_clients['second chair'].time_on_the_second_chair_chair = chair2.exit_time - chair2.entrance_time
            cur_clients['second chair'].exit_time = timer
            logger_list.append(cur_clients['second chair'])
            clients.remove(cur_clients['second chair'])
            cur_clients['second chair'] = None

        if chair2.is_busy and served:
            chair1.is_busy = True
            cur_clients['first chair'].time_in_queue += 1

        if not chair2.is_busy and served:  # Как только первый стул закончил работу начинает второй
            cur_clients['second chair'] = cur_clients['first chair']
            cur_clients['first chair'] = None
            chair2.is_busy = True
            chair2.entrance_time = timer
            served = False

    # timer += 1

for k in logger_list:
    print(k.give_info())
