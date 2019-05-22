
#!/usr/bin/env python3

import csv

import psycopg2
import pandas as pd

import wrapper as w


#print ("in object_relational_mapper.py")

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(dbname = 'terminal_trader')
        self.cursor     = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()

    def create_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        self.cursor.execute(
            """CREATE TABLE {table_name}(
                pk SERIAL PRIMARY KEY
            );""".format(table_name = table_name))

    def add_column(self, table_name, column_name, column_type):
        self.cursor.execute(
            """ALTER TABLE {table_name}
                ADD COLUMN {column_name} {column_type}
                ;""".format(table_name = table_name, column_name = column_name, column_type = column_type))

def does_not_exist(username):
    with Database() as db:
        db.cursor.execute(
            "SELECT username FROM users WHERE username=%s;", (username,))
        occurences = db.cursor.fetchall()
        if len(occurences) < 1:
            print("occurences", occurences, type(occurences))
            return True
        else:
            print("username taken")
            return False







class User:

    def __init__(self, username):
        self.username = username

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def login(self, password):
        with Database() as db:
            db.cursor.execute(
                """SELECT password
                    FROM users
                    WHERE username=%s;""",
                    (self.username,))
            if password == db.cursor.fetchone():
                return True
            else:
                return False

    def signup(self, password, balance):
        if does_not_exist(self.username):
            with Database() as db:
                db.cursor.execute(
                """INSERT INTO users(
                        username,
                        password,
                        balance
                    ) VALUES (
                        %s, %s, %s
                    );""", (self.username, password, balance)
                )
                return True
        else:
            return False



    def buy(self, ticker_symbol, trade_volume):
        # TODO connect to the model, un-hardcode the username, un-hardcode the price, un-hardcode the trade_volume

        with Database() as db:
            db.cursor.execute(
                """SELECT balance from users where username='simbuilder';""")
            my_cash = db.cursor.fetchone()
            last_price = w.quote(ticker_symbol)

            if (float(my_cash[0]) >= trade_volume * last_price):
                print ("Filled! You bought {} {} @ {}.".format(trade_volume, ticker_symbol, last_price))
                pass
            else:
                print ("Rejected! You don't have enough funds available.")

    def calc_market_value(trade_volume, last_price):
        pass

        ## PSEUDO:
        # need to finish with POS vs NEG costs for buy vs sell
        # calc_mkt_value = share qty * last_price
        # if buy: +qty * mkt_price = +mkt_value
        # if sell: -qty * mkt_price = -mkt_value

        market_value = trade_volume * last_price




    def sell(self, ticker_symbol, trade_volume):
        pass
#        with Database() as db:
 #           my_position - db.cursor.execute(
  #              """ SELECT position from"""
        # TODO
        pass




    def update_balance(self, username, market_value):
        with Database() as db:
            db.cursor.execute(
                """SELECT balance FROM users where username = {};""".format(username))
            balance_start = db.cursor.fetchone()
            # balance_start returns a tuple; next line extracts the single value I want
            balance_start = balance_start[0]
            order_cost = market_value                   #TODO pass in the market_value
            balance_end = balance_start - order_cost   #TODO need to wrap in FLOAT? or already float??

            db.cursor.execute(
                """UPDATE users
                    SET balance = {}
                    WHERE username = {};""".format(balance_end, username))



if __name__ == "__main__":
    with User('simbuilder') as u:
#        ticker_symbol = input ("Which ticker? ")
#        volume = int( input ("How many shares? "))

#        u.buy(ticker_symbol, volume)  # ticker + order_qty

        u.update_balance ('username', 25000)
