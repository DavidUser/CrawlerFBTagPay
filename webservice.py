import threading
from flask import Flask, request

app = Flask(__name__)

@app.route("/health")
def root():
    return 'Alive.'

from crawler import Merchant

lock = threading.Lock()

merchants = []

@app.route("/work")
def work():
    lock.acquire()
    for merchant in merchants:
        merchant.update_all_payments();
        merchant.charge_payments();
        merchant.print_payments();
    lock.release()
    return 'done'

@app.route("/merchants", methods=['POST'])
def add_merchant():
    body = request.get_json();
    _id = body['id']
    token = body['token']
    print token

    lock.acquire()
    if _id in [merchant.id for merchant in merchants]:
        lock.release()
        return 'Merchant %s already on database.' % _id

    merchant = Merchant(_id, token)
    print merchant.token
    merchants.append(merchant)
    lock.release()

    return 'Merchant %s added.' % _id

import time

class CrawlerWork(threading.Thread):
    def __init__(self):
        """TODO: to be defined1. """
        threading.Thread.__init__(self)

    def run(self):
        work()

crawler_working = CrawlerWork()
#crawler_working.start()

