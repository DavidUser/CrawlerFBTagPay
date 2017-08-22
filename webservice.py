import threading
from flask import Flask, request

webservice = Flask(__name__)

@webservice.route("/health")
def root():
    return 'Alive.'

from crawler import Merchant

lock = threading.Lock()

merchants = []

@webservice.route("/work")
def work():
    lock.acquire()
    for merchant in merchants:
        merchant.update_all_payments();
        merchant.charge_payments();
        merchant.print_payments();
    lock.release()
    return 'done'

@webservice.route("/merchants", methods=['POST'])
def add_merchant():
    body = request.get_json();
    print body

    _id = body['id']
    token = body['token']

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
        while True:
            work()
            print "working..."
            time.sleep(1)

