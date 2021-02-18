#!/usr/bin/env python3

import os, sys, time
import stockquotes as sq
import cryptocompare as cc
import datetime as dt
import rich

update_interval = 15
updates = 0
term_size = os.get_terminal_size()
term_width = int(term_size[0])
term_height = int(term_size[1])

stocks = ['GME', 'AMC', 'BB', 'T']
crypto = ['BTC', 'ETH']

s_prices = []
s_changes = []
c_prices = []
c_changes = []
c_open_prices = []

os.system('clear')
print('Refueling rockets...')

def get_percent_change(coin, index): # not working yet
    if len(c_open_prices) == 0:
        for i in range(len(crypto)):
            price = cc.get_historical_price_day(i, 'USD', toTs=time.time())
            c_open_prices.append(price)

    price = cc.get_price(coin, currency='USD')[coin]['USD'] 
    change_percent = ((price - c_open_prices[index]) / price) * 100

    return change_percent 

def get_prices():
    s_prices.clear()
    s_changes.clear()
    if len(stocks) > 0:
        for i in range(len(stocks)):
            stock = sq.Stock(stocks[i])
            s_prices.append(stock.current_price)
            s_changes.append(stock.increase_percent)

    c_prices.clear()

    if len(crypto) > 0:
        for i in range(len(crypto)):
            coin = crypto[i]
            price = cc.get_price(coin, currency='USD')[coin]['USD']      
 
            c_prices.append(price)

    update_ui()

def update_ui():
    os.system('clear')
    print('Stocks:')
    if len(stocks) > 0:
        for i in range(len(stocks)):
            stock = stocks[i]
            price = s_prices[i]
            change_percent = s_changes[i]
            print(f'{stock} - ${price:,} ({change_percent:+n}%)')

    print('\nCrypto')
    if len(crypto) > 0:
        for i in range(len(crypto)):
           coin = crypto[i]
           price = c_prices[i]
           print(f'{coin} - ${price:,}')
    print('')

while True:
    get_prices()
    updates += 1
    print(f'Updated {updates} times.')
    time.sleep(update_interval)
