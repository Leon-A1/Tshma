import random

def trademkr():

    buyorsell = ['BUY','SELL']
    winorlose = ['WIN','WIN','WIN', 'LOSE','WIN','WIN', 'LOSE', 'LOSE']
    assets = ['BTC/USD','ETH/USD','XRP/USD','LTC/USD','DAG/USD','ATOM/USD','BCH/USD','ETC/USD','BSV/USD','USD/EOS','USD/TRX','USD/DASH','USD/BNB','ZEC/BTC','NEO/ETH','ADA/BTC','LINK/BNB','BTC/ETH','BNB/ETH','XLM/ADA']

        #a function to create profits
    # numgen = [random.randrange(0, 5, 1) for i in range(10)]
    total = []
    trade = []
    howmany = 0
    # if todays_day == time_now.day:
    #     howmany = 14
    # if howmany < 10:

    while howmany < 25:
        trade.append(random.choice(assets))
        trade.append(random.choice(buyorsell))
        trade.append(random.choice(winorlose))
                # trade.append(random.choice(numgen))
        trade.append(round(random.uniform(0.1,4), 2))
        howmany += 1
        total.append(trade)
        trade = []

    return total





def balance_updater(balance, profits_amount_total, loses_amount_total):

    balance = float(balance) +(profits_amount_total)-(loses_amount_total)

    return  balance






def profits_updater(total):

    profits_amount_total = 0

    for p in total:
        if p[2] == 'WIN':
            profits_amount_total = profits_amount_total + p[3]

    return profits_amount_total




def lose_updater(total):

    loses_amount_total = 0
    for p in total:
        if p[2] == 'LOSE':
            loses_amount_total = loses_amount_total + p[3]

    return loses_amount_total





if __name__ == '__main__':
    profit()
