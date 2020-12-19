import threading
import time
import random
import speedx_accurasy as sa

import numpy as np

random.seed(1)

log_dict={
    (0,0):0,
    (1,0):0,
    (0,1):0,
    (1,1):0,
    ('b',1):0,
}

C_SIZE = 50
served = False
checked = False
uptime = False

# settings
speed_x = 1
print_steps = 1
time_in_Q = 0
zero_ppl_s = 0
zero_ppl_e = 0

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
    global time_in_Q
    global zero_ppl_s
    global zero_ppl_e
    if zero_ppl_s != 0:
        zero_ppl_s = time.time() - zero_ppl_s
        zero_ppl_s = 0
    chair1.serving1(client)

    if chair2.is_busy:
         print("client", client.id, "is waiting for second chair")
         start = time.time()
    ###
         e.wait()
         print("client", client.id, "is no longer waiting")
         end = time.time()
         client.time_in_queue = end - start
         print("client - {}, time in queue {}".format(client.id, client.time_in_queue))
   # start = time.time()
   # e.wait()
   # end = time.time()
   # client.time_in_queue = end - start
    e.clear()
    if print_steps:
        print("client - {}, time in queue {}".format(client.id, client.time_in_queue))
    chair1.is_busy = False
    chair2.serving2(client)
    # client.exit_time = client.entrance_time_second + client.time_on_the_second_chair
    logger_list.append(client)
    time_in_Q += client.time_in_queue
    if not chair1.is_busy:
        zero_ppl_s = time.time()
    e.set()
    return


class Chair:
    entrance_time = None
    exit_time = None
    is_busy = False

    def __init__(self):
        pass

    def serving1(self, client):
        global _ksi1
        #_ksi1 = np.random.exponential(1/nu1)
        _ksi1 = random.expovariate(nu1)
        print('1-',_ksi1)
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
        global _ksi2
       # _ksi2 = np.random.exponential(1/nu2)
        _ksi2 = random.expovariate(nu2)
        print('2-',_ksi2)
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
gl_id = 0
e = threading.Event()

### init vars

lmb = 1 / 2

# _lambda = np.random.poisson(lmb) / speed_x
# _ksi1 = random.expovariate(lmb) / speed_x
# _ksi2 = random.expovariate(lmb) / speed_x

lm = (0.5)
nu1 = (0.7)
nu2 = (1.4)

_lambda = 1
_ksi1 = 1
_ksi2 = 1

#print('интенсивность поступления заявок - {}, интенсивность обслуживания(1 стул) - {},'
#      ' интенсивность обслуживания(2 стул) - {}'.format(_lambda * speed_x, _ksi1 * speed_x,
#                                                        _ksi2 * speed_x))

num_of_rejected = 0
num_of_served = 0

program_start = time.time()
time_lambda = time.time()
persentage = 10
print("|       |")

for c in range(C_SIZE):
    random.seed()
    if c * 100 // C_SIZE >= persentage:
        print("#", sep='', end='')
        persentage += 10

    if c != 0:
        #_lambda = random.expovariate(lm)
        _lambda = np.random.poisson(1/lm)
        print("lmb", _lambda)
       # _lambda = np.random.gamma(lm)
        time.sleep(_lambda)  # waiting for client
        time_lambda = time.time()
    else:
        e.set()

    if print_steps:
        print("got new client! cur time = ", time_lambda - program_start)

    if chair1.is_busy:
        num_of_rejected += 1
        if print_steps:
            print("client rejected chair is busy")
    else:
        num_of_served += 1
        gl_id += 1
        time_start = time.time()
        x = threading.Thread(target=serving, args=(Client(gl_id, time_start - program_start), chair1, chair2,))
        x.start()

x.join()
program_end = time.time()
tot_time=program_end-program_start
print("QQQQQQ TIME = ", time_in_Q / (program_end - program_start))
print("ZERO TIME = ", zero_ppl_s / (program_end - program_start))
print()
print("всего клиентов - {}, отклонено - {}, обслужено - {}".format(num_of_served + num_of_rejected,
                                                                   num_of_rejected, num_of_served))

if print_steps:
    print(
        "id| entrance_time_first | time_on_the_first_chair |  time_in_queue | "
        "entrance_time_second | time_on_the_second_chair | exit_time")
if print_steps:
    for k in logger_list:
        print(k.give_info())

for i in range(len(logger_list)):
    if(i==0):
        log_dict[(1,0)]+=logger_list[i].time_on_the_first_chair
    elif (i == len(logger_list) - 1):
        break
    elif(logger_list[i].entrance_time_first>logger_list[i-1].exit_time):
        log_dict[(1, 0)] += logger_list[i].time_on_the_first_chair

    #if(logger_list[i].entrance_time_second<logger_list[i+1].entrance_time_first):

    if(logger_list[i+1].entrance_time_first + logger_list[i+1].time_on_the_first_chair < logger_list[i].exit_time):
        tmp = logger_list[i + 1].time_on_the_first_chair + logger_list[i + 1].entrance_time_first - logger_list[i].exit_time
        if(tmp<0):
            log_dict[(0,1)]+=logger_list[i].time_on_the_second_chair
        else:
            
            log_dict[(1,1)]+=logger_list[i+1].time_on_the_first_chair
    elif logger_list[i + 1].entrance_time_first<logger_list[i].exit_time:
        tmp = logger_list[i + 1].time_on_the_first_chair+logger_list[i+1].entrance_time_first-logger_list[i].exit_time
        log_dict[(1, 0)] += tmp
        log_dict[(1,1)]+=logger_list[i + 1].time_on_the_first_chair-tmp
    else:
        log_dict[(0,1)]+=logger_list[i].time_on_the_second_chair
        log_dict[(0,0)]+=logger_list[i+1].entrance_time_first-logger_list[i].exit_time

print("TRUE RES")
for i in log_dict.values():
    print(i)
   # print(i/tot_time)

mean_time_in_system = 0
P_denial = 0
P_wait = 0
mean_wait_time = 0
first_chair_entrances = []
second_chair_entrances = []

for k in logger_list:
    mean_time_in_system += _ksi1 + _ksi2 + k.give_info()[3]
    if k.give_info()[3] != 0:
        P_wait += 1
    mean_wait_time += k.give_info()[3]
    first_chair_entrances.append(k.give_info()[1])
    second_chair_entrances.append(k.give_info()[4])


sset1 = []
sset2 = []
id = 0
for item in first_chair_entrances:
    sset1.append(tuple((item, item + logger_list[id].give_info()[2])))
    id += 1

id = 0
for item in second_chair_entrances:
    sset2.append(tuple((item, item + logger_list[id].give_info()[-2])))
    id += 1

print(sset1)
print(sset2)

system_work_time = logger_list[-1].give_info()[-1]
matrix = sa.get_segment_intersection(sset1, sset2, system_work_time)
t_b_1 = mean_wait_time / system_work_time
matrix[0][1] -= t_b_1
mean_time_in_system /= num_of_served
P_denial = len(logger_list) * _ksi1 / system_work_time
P_wait /= num_of_served
mean_wait_time /= num_of_served
P_no_clients_second_chair = len(logger_list) * _ksi2 / system_work_time

print()
print("Среднее время в системе (1 стул - очередь - 2 стул)  ", mean_time_in_system * speed_x)
print("Занятость 1 стула                                    ", P_denial)
print("Отказов                                              ", num_of_rejected / (num_of_rejected + num_of_served))
print("Ожидающих клиентов                                   ", P_wait)
print("Среднее время ожидания                               ", mean_wait_time * speed_x)
print("Нет клиентов на 1 стуле                              ", (1 - P_denial))
print("Нет клиентов на 2 стуле                              ", P_no_clients_second_chair)
print("-----------------------------------------------------------")
print("(0, 0)                                               ", matrix[0][0])
print("(0, 1)                                               ", matrix[0][1])
print("(1, 0)                                               ", matrix[1][0])
print("(1, 1)                                               ", matrix[1][1])
print("(b, 1)                                               ", t_b_1)
print("-----------------------------------------------------------")
print("Проверка суммой (==1): ", matrix[0][0] + matrix[0][1] + matrix[1][0] + matrix[1][1] + t_b_1)
print("speedX: ", speed_x, "\nMean min speedX error: ", 100 - int(sa.get_expected_accurasy(speed_x) * 10000) / 100, "%")
