import ru_local
import random
import math

CFG = {
    1: {
        'type': [ru_local.AI80],
        'customers': 3
    },
    2: {
        'type': [ru_local.AI92],
        'customers': 2
    },
    3: {
        'type': [
            ru_local.AI92,
            ru_local.AI95,
            ru_local.AI98
        ],
        'customers': 4
    }
}

PRICE = {
    ru_local.AI80: 43,
    ru_local.AI92: 47.3,
    ru_local.AI95: 50.8,
    ru_local.AI98: 67.5
}

gas_stat = {1: [], 2: [], 3: []}
unfilled = 0
revenue = 0
customers = []
fuel = {
    ru_local.AI80: 0,
    ru_local.AI92: 0,
    ru_local.AI95: 0,
    ru_local.AI98: 0
}


def convert_time(time):
    """
    The function converts time measurement in minutes to time measurement in minutes and hours.
    :param time: Time in minutes.
    :return: Time in format "hh:mm".
    """
    if len(str(time // 60)) == 1:
        if len(str(time % 60)) == 1:
            return '0' + str(time // 60) + ':' + '0' + str(time % 60)
        return '0' + str(time // 60) + ':' + str(time % 60)
    if len(str(time % 60)) == 1:
        return str(time // 60) + ':' + '0' + str(time % 60)
    return str(time // 60) + ':' + str(time % 60)


with open('input.txt', encoding='UTF-8') as f:
    for info in f:
        name = info.rstrip()
        client = info.split()
        client[0] = client[0].split(':')
        customers.append({
            'time': int(client[0][0]) * 60 + int(client[0][1]),
            'liters': int(client[1]),
            'type': client[2],
            'name': name
        })


for time in range(1440):
    # Checking to see if any customer is due to leave at this point in time.
    for stat_num in gas_stat:
        if gas_stat[stat_num] != [] and time == gas_stat[stat_num][0][0]:
            print(ru_local.filled(
                time=convert_time(time),
                client_name=gas_stat[stat_num][0][1]
            ))
            gas_stat[stat_num].pop(0)
            for stat in CFG:
                print(ru_local.station_stat(
                    num=stat,
                    queue=CFG[stat]['customers'],
                    gas_type=', '.join(CFG[stat]['type']),
                    customers_num=len(gas_stat[stat])
                ))

    # If a customer arrives at the current time, we process it.
    stat_num = None
    if customers[0]['time'] == time:
        m_queue = float('inf')
        for stat in CFG:
            if customers[0]['type'] in CFG[stat]['type'] and \
               len(gas_stat[stat]) < m_queue and \
               len(gas_stat[stat]) < CFG[stat]['customers']:
                m_queue = len(gas_stat[stat])
                stat_num = stat

        # Calculation of refueling time.
        refill_time = math.ceil(customers[0]['liters'] / 10)
        extra_time = random.randint(-1, 1)
        if refill_time + extra_time < 1:
            extra_time = random.randint(0, 1)

        # If there is an available gas station, process the customer.
        if stat_num is not None:
            # Calculation of the end of refueling time.
            if len(gas_stat[stat_num]) == 0:
                full_time = time + refill_time + extra_time
            else:
                full_time = gas_stat[stat_num][-1][0] + refill_time + extra_time

            # Checking that the customer has time to refuel before the end of the specified time period.
            if 1440 - full_time >= 0:
                fuel[customers[0]['type']] += customers[0]['liters']
                gas_stat[stat_num].append([full_time, f"{customers[0]['name']} {str(refill_time + extra_time)}"])
                print(ru_local.new_customer_queue(
                    time=convert_time(time),
                    name=gas_stat[stat_num][-1][1],
                    stat_num=stat_num
                ))
                for stat in CFG:
                    print(ru_local.station_stat(
                        num=stat,
                        queue=CFG[stat]['customers'],
                        gas_type=', '.join(CFG[stat]['type']),
                        customers_num=len(gas_stat[stat])
                    ))
            else:
                print(ru_local.unfilled(
                    time=convert_time(time),
                    name=customers[0]['name'],
                    filling_time=str(refill_time + extra_time)
                ))
                unfilled += 1
        else:
            print(ru_local.unfilled(
                time=convert_time(time),
                name=customers[0]['name'],
                filling_time=str(refill_time + extra_time)
            ))
            unfilled += 1

        customers.pop(0)

# Print results.
print(ru_local.RESULTS)
for fuel_type in fuel:
    print(ru_local.total_liters(
        liters=fuel[fuel_type],
        fuel_type=fuel_type
    ))
    revenue += fuel[fuel_type] * PRICE[fuel_type]
print(ru_local.total_unfilled(num=unfilled))
print(ru_local.revenue(summ=revenue))
