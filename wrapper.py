#!/usr/bin/env python3

import json

import requests


def lookup(company_name):
    response = json.loads(requests.get(f'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input={company_name}').text)
    ticker_symbol = response[0]['Symbol']
    return ticker_symbol

def quote():
    pass


if __name__ == "__main__":
    #response = json.loads(requests.get('http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=TSLA').text)
    user_input = input("What ticker symbol?")
    print (lookup(user_input))

