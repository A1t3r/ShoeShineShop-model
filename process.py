import threading
import time
import random

C_SIZE = 15
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
    entrance_time_first = None
    entrance_time_second = None
    exit_time = None
    time_on_the_first_chair = None
    time_on_the_second_chair = None
    time_in_queue = 0

    def __init__(self, _id, _entrance_time):
        self.id = _id
        self.entrance_time = _entrance_time

    def give_info(self):
        return [self.id, self.entrance_time_first, self.time_on_the_first_chair,
                self.time_in_queue, self.entrance_time_second,
                self.time_on_the_second_chair, self.exit_time]


cur_clients = {
    'first chair': Client,
    'second chair': Client
}


def serving(client, chair1, chair2):
    chair1.serving1(client)

    if chair2.is_busy:
        print("client", client.id, "is waiting for second chair")
        start = time.time()
        ###
        e.wait()
        end = time.time()
        client.time_in_queue = end - start
        print("client - {}, time in queue {}".format(client.id, client.time_in_queue))

    e.clear()
    chair1.is_busy = False
    chair2.serving2(client)
    client.exit_time = client.entrance_time_second + client.time_on_the_second_chair
    logger_list.append(client)
    e.set()
    return


class Chair:
    entrance_time = None
    exit_time = None
    is_busy = False

    def __init__(self):
        pass

    def serving1(self, client):
        self.is_busy = True
        print('start serving client', client.id, 'on first', " in ", client.entrance_time_first, "\n")
        time.sleep(_ksi1)
        client.time_on_the_first_chair = _ksi1
        served = True
        print("client {} is served on first, total time - {}".format(client.id, client.time_on_the_first_chair))
        # self.is_busy = False
        return

    def serving2(self, client):
        self.is_busy = True
        client.entrance_time_second = client.entrance_time_first + client.time_on_the_first_chair + client.time_in_queue
        print('start serving client', client.id, ' on second', " in ", client.entrance_time_second)
        time.sleep(_ksi2)
        client.time_on_the_second_chair = _ksi2
        print("client {} is served on second, total time - {}".format(client.id, client.time_on_the_second_chair))
        self.is_busy = False
        return


chair1 = Chair()
chair2 = Chair()

Added = False

clients = []
timer = 0
gl_id = 1
e = threading.Event()

### init vars

lmb = 1 / 2

_lambda = random.expovariate(lmb)
_ksi1 = random.expovariate(lmb)
_ksi2 = random.expovariate(lmb)

print('интенсивность поступления заявок - {}, интенсивность обслуживания(1 стул) - {},'
      ' интенсивность обслуживания(2 стул) - {}'.format(_lambda, _ksi1, _ksi2))

num_of_rejected = 0
num_of_served = 0

for c in range(C_SIZE):
    if c != 0:
        time.sleep(_lambda)  # waiting for client
    print("got new client! cur time = ", c * _lambda)
    if chair1.is_busy:
        num_of_rejected += 1
        print("client rejected chair is busy")
    else:
        num_of_served += 1
        clients.append(Client(gl_id, timer))
        gl_id += 1
        cur_clients['first chair'] = clients[len(clients) - 1]  # remove?
        cur_clients['first chair'].entrance_time_first = c * _lambda
        x = threading.Thread(target=serving, args=(cur_clients['first chair'], chair1, chair2,))
        x.start()

x.join()
print("всего клиентов - {}, отклонено - {}, обслужено - {}".format(num_of_served + num_of_rejected,
                                                                   num_of_rejected, num_of_served))
print(
    "id| entrance_time_first | time_on_the_first_chair |  time_in_queue | "
    "entrance_time_second | time_on_the_second_chair | exit_time")
for k in logger_list:
    print(k.give_info())
