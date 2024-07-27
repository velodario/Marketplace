"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time
import logging



class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        id_consumer = self.marketplace.new_cart()  # get id for consumer
        for consumers in self.carts:
            for action in consumers:
                quantity_product = 0
                # while not exceeding the quantity
                while action['quantity'] > quantity_product:
                    if action['type'] == "add":
                        check_add = self.marketplace.add_to_cart(
                            id_consumer, action['product'])
                        if check_add is True:
                            quantity_product += 1
                        else:
                            logging.error(
                                '{} failed to add to cart, retrying wait'.format(action['product']))
                            time.sleep(self.retry_wait_time)
                    if action['type'] == "remove":
                        self.marketplace.remove_from_cart(
                            id_consumer, action['product'])
                        quantity_product += 1

        logging.info('order placed {}'.format(
            self.marketplace.place_order(id_consumer)))