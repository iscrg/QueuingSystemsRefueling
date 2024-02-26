RESULTS = '\nРезультаты:'


def filled(time, client_name):
    return f"В {time} клиент {client_name} заправил свой автомобиль и покинул АЗС."


def station_stat(num, queue, gas_type, customers_num):
    return f"Автомат №{num} максимальная очередь: {queue} марки бензина: {gas_type} ->{'*' * customers_num}."


def new_customer_queue(time, name, stat_num):
    return f"В {time} новый клиент: {name} встал в очередь к автомату №{stat_num}."


def unfilled(time, name, filling_time):
    return f"В {time} новый клиент: {name} {filling_time} не смог заправить автомобиль и покинул АЗС."


def total_liters(liters, fuel_type):
    return f"За сутки было заправлено {liters} литров {fuel_type}"


def total_unfilled(num):
    return f"Количество клиентов, которые покинули АЗС не заправив автомобиль из-за 'скопившейся' очереди {num}"


def revenue(summ):
    return f"Доход: {summ}"