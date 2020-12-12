import logging
import threading
import time

C_SIZE = 100
timer = 0
_lambda = 5  # интенсивность прихода требования
_ksi = 8  # интенсивность обслуживания
served = False
checked = False
uptime = False

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

    def serving1(self, timerl, client):
        global served
        global checked
        global uptime
        while 1:
            event2.set()
            print('11 - ', timer, "\n")
            event1.wait()
            if (timer - timerl) % _ksi == 0 and (timer - timerl) != 0:
                client.time_on_the_first_chair = timer - timerl
                served = True
                print(client.time_on_the_first_chair)
                return
            event2.clear()


    def serving2(self, timerl, client):
        while 1:
            # event.wait()
            # print('2 - ', timer,"\n")
            if (timer - timerl) % _ksi == 0 and (timer - timerl) != 0:
                client.time_on_the_second_chair = timer - timerl
                return


class Chair_2:
    entrance_time = None
    exit_time = None
    is_busy = False

    def __init__(self):
        pass

    def serving(self, _timer):
        while 1:
            if _timer != 0 and _timer % _ksi == 0:
                self.exit_time = _timer
                return True
            return False


chair1 = Chair_1()
chair2 = Chair_1()

served = False
Added = False

clients = []
timer = 0
gl_id = 0
ex_time = 0
lock = threading.Lock()
cv = threading.Condition()
event1 = threading.Event()
event2 = threading.Event()

for timer in range(C_SIZE):
    print(timer)
    if timer != 0:
        event1.clear()
        event2.wait()
        checked = False
        event1.set()
    else:
        event1.set()

    if timer % _lambda == 0 and not chair1.is_busy:  # Поступление запроса Если занят первый стул то запрос отклоняется
        clients.append(Client(gl_id, timer))
        gl_id += 1

        if not chair1.is_busy:
            cur_clients['first chair'] = clients[len(clients) - 1]
            chair1.is_busy = True
            x = threading.Thread(target=chair1.serving1, args=(timer, cur_clients['first chair'],))
            x.start()
            if served and False:

                chair1.is_busy = False
                served = False

                if not chair2.is_busy and served:
                    cur_clients['second chair'] = cur_clients['first chair']
                    chair2.is_busy = True
                    y = threading.Thread(target=chair2.serving2, args=(timer, cur_clients['second chair'],))
                    y.start()
                    chair2.is_busy = False
                    cur_clients['second chair'].exit_time = timer
                    logger_list.append(cur_clients['second chair'])

                else:
                    chair1.is_busy = True
                    cur_clients['first chair'].time_in_queue += 1

for k in logger_list:
    print(k.give_info())
