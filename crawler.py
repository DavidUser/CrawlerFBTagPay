import requests

def get_on_facebook(route, token):
    url = "https://graph.facebook.com/v2.10/%s&access_token=%s" % (route,token)
    response = requests.get(url)
    response.status_code == 200 or print("Can't get post from page. " + response.reason)
    return response.json()

def get_comments(_id, token):
    GET_COMMENTS_URL = "%s?fields=comments" % _id
    comments_on_post = get_on_facebook(GET_COMMENTS_URL, token)
    if 'comments' in comments_on_post:
        return get_on_facebook(GET_COMMENTS_URL, token)['comments']['data']
    return []

def send_pay(merchant_id, payer_id, amount):
    """Send a payment request to tag pay backoffice

    :bid: data of transaction
    :returns: True if payment is approved.

    """
    endpoint = 'http://localhost:61369/api/transaction'
    body = {
        'FacebookSellerId' : merchant_id,
        'FacebookBuyerId' : payer_id,
        'Amount' : int(float(amount)*100)
    }

    response = requests.post(endpoint, json=body);

    return response.status_code == 201

class Bid():

    """Comment with Bid"""

    def __init__(self):
        """TODO: to be defined1. """
        self.comment_id = ''
        self.amount = 0
        self.payer_id = ''

class Merchant():
    def __init__(self, _id, token):
        self.payments = []
        self.paid = []
        self._id = _id
        self.token = token

    def get_selling_posts(self):
        GET_POSTS_URL = "%s/posts?fields=message" % self._id
        facebook_response = get_on_facebook(GET_POSTS_URL, self.token)
        if 'error' in facebook_response :
            return 
        posts_on_page = facebook_response['data']
        selling_posts = []
        sell_tag = '#tagpay #vendo'

        for post in posts_on_page:
            print(post)
            if 'message' in post:
                if post['message'].find(sell_tag) != -1:
                    post_id = post['id']
                    selling_posts.append(post_id)

        return selling_posts

    def get_bid_comments(self, post_id):
        comments_on_post = get_comments(post_id, self.token)
        bid_comments = []
        pay_tag = '#pago'

        for comment in comments_on_post:
            message = comment['message'].split()
            if pay_tag in message:
                tag_position = message.index(pay_tag)
                bid = Bid()
                bid.payer_id = comment['from']['id']
                bid.amount = message[tag_position + 1]
                bid.comment_id = comment['id']
                bid_comments.append(bid)

        return bid_comments

    def get_payments_on_selling_post(self, post_id):
        payments = []
        sell_tag = '#vendido'
        bid_comments = self.get_bid_comments(post_id)
        if bid_comments is None:
            return
        for bid in bid_comments:
            replies = get_comments(bid.comment_id, self.token)
            for reply in replies:
                if sell_tag in reply['message'].split() and reply['from']['id'] == self._id:
                    payments.append(bid)
                    print(payments)
        return payments

    def update_all_payments(self):
        selling_posts = self.get_selling_posts()
        if selling_posts is None:
            return
        for post in selling_posts:
            for payment in self.get_payments_on_selling_post(post):
                # update payments
                if payment.comment_id not in [p.comment_id for p in self.paid] and payment.comment_id not in [p.comment_id for p in self.payments]:
                    self.payments.append(payment)
        
        return self.payments

    def charge_payments(self):
        payments_paid = []

        for payment in self.payments:
            payment_result_sucessfull = send_pay(self._id, payment.payer_id, payment.amount)
            if payment_result_sucessfull:
                self.paid.append(payment)
                payments_paid.append(payment)

        self.payments = [payment for payment in self.payments if payment not in payments_paid]

    def print_payments(self):
        print ("===========")
        print ("paid: ")
        for bid in self.paid:
            print ("Comment %s indicate to pay R$ %s from user %s" % (bid.comment_id, bid.amount, bid.payer_id))
        print ("---------")
        print ("payments: ")
        for bid in self.payments:
            print ("Comment %s indicate to pay R$ %s from user %s" % (bid.comment_id, bid.amount, bid.payer_id))
        print ("===========")
