import threading
import time
import random
import speedx_accurasy as sa

C_SIZE = 1000
served = False
checked = False
uptime = False

# settings
speed_x = 100
print_steps = False

logger_dict = {
    'Entrance time': [],
    'Exit time': [],
    'Time on the first chair': [],
    'Time in queue': [],
    'Time on the second chair': []
}

logger_list = []

message = ""
if speed_x:
    message = "hello"

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
        self.entrance_time_first = _entrance_time

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

    # if chair2.is_busy:
    #    print("client", client.id, "is waiting for second chair")
    #    start = time.time()
    ###
    #     e.wait()
    #     print("client", client.id, "is no longer waiting")
    #     end = time.time()
    #     client.time_in_queue = end - start
    #      print("client - {}, time in queue {}".format(client.id, client.time_in_queue))
    start = time.time()
    e.wait()
    end = time.time()
    client.time_in_queue = end - start
    e.clear()
    if print_steps:
        print("client - {}, time in queue {}".format(client.id, client.time_in_queue))
    chair1.is_busy = False
    chair2.serving2(client)
    # client.exit_time = client.entrance_time_second + client.time_on_the_second_chair
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
        if print_steps:
            print('start serving client', client.id, 'on first', " in ", client.entrance_time_first, "\n")
        time.sleep(_ksi1)
        client.time_on_the_first_chair = _ksi1
        if print_steps:
            print("client {} is served on first, total time - {}".format(client.id, client.time_on_the_first_chair))
        # self.is_busy = False
        return

    def serving2(self, client):
        self.is_busy = True
        client.entrance_time_second = client.entrance_time_first + client.time_on_the_first_chair + client.time_in_queue
        if print_steps:
            print('start serving client', client.id, ' on second', " in ", client.entrance_time_second)
        time.sleep(_ksi2)
        client.time_on_the_second_chair = _ksi2
        if print_steps:
            print("client {} is served on second, total time - {}".format(client.id, client.time_on_the_second_chair))
        client.exit_time = client.entrance_time_second + client.time_on_the_second_chair
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

_lambda = 0.5 / speed_x
_ksi1 = 0.7 / speed_x
_ksi2 = 1.4 / speed_x

print('интенсивность поступления заявок - {}, интенсивность обслуживания(1 стул) - {},'
      ' интенсивность обслуживания(2 стул) - {}'.format(_lambda, _ksi1, _ksi2))

num_of_rejected = 0
num_of_served = 0

program_start = time.time()
time_lambda=time.time()
persentage = 10

for c in range(C_SIZE):
    if c != 0:
        time.sleep(_lambda)  # waiting for client
        time_lambda = time.time()
    else:
        e.set()

    if c * 100 / C_SIZE >= persentage:
        print(persentage, "% finished", sep='')
        persentage += 10

    if print_steps:
        print("got new client! cur time = ", time_lambda-program_start )

    if chair1.is_busy:
        num_of_rejected += 1
        if print_steps:
            print("client rejected chair is busy")
    else:
        num_of_served += 1
        # clients.append(Client(gl_id, timer))
        gl_id += 1
        # cur_clients['first chair'] = clients[len(clients) - 1]  # remove?
        # cur_clients['first chair'].entrance_time_first = c * _lambda
        # x = threading.Thread(target=serving, args=(cur_clients['first chair'], chair1, chair2,))
        time_start = time.time()
        x = threading.Thread(target=serving, args=(Client(gl_id, time_start-program_start), chair1, chair2,))
        x.start()

x.join()
print("всего клиентов - {}, отклонено - {}, обслужено - {}".format(num_of_served + num_of_rejected,
                                                                   num_of_rejected, num_of_served))
print(
    "id| entrance_time_first | time_on_the_first_chair |  time_in_queue | "
    "entrance_time_second | time_on_the_second_chair | exit_time")

for k in logger_list:
    print(k.give_info())


mean_time_in_system = 0
P_denial = 0
P_wait = 0
mean_wait_time = 0

for k in logger_list:
    mean_time_in_system += _ksi1 + _ksi2 + k.give_info()[3]
    if k.give_info()[3] != 0:
        P_wait += 1
    mean_wait_time += k.give_info()[3]


mean_time_in_system /= num_of_served
P_denial = len(logger_list) * _ksi1 / logger_list[-1].give_info()[-1]
P_wait /= num_of_served
mean_wait_time /= num_of_served
P_no_clients_second_chair = len(logger_list) * _ksi2 / logger_list[-1].give_info()[-1]

print()
print("Среднее время в системе (1 стул - очередь - 2 стул)  ", mean_time_in_system * speed_x)
print("Занятость 1 стула                                    ", P_denial)
print("Отказов                                              ", num_of_rejected / (num_of_rejected + num_of_served))
print("Ожидающих клиентов                                   ", P_wait)
print("Среднее время ожидания                               ", mean_wait_time * speed_x)
print("Нет клиентов на 1 стуле                              ", (1 - P_denial))
print("Нет клиентов на 2 стуле                              ", P_no_clients_second_chair)
print()
print("speedX: ", speed_x, "\nPossible error: ", int(sa.get_expected_accurasy(speed_x) * 100), "%")

