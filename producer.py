"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def run(self):
        id_producer = self.marketplace.register_producer()  # primesc id pentru producator
        while True:
            for prod_id in self.products:  # pentru fiecare product
                # pentru fiecare numar de cantitate
                for _ in range(0, prod_id[1]):
                    # publicare produs in marketplace
                    check = self.marketplace.publish(id_producer, prod_id[0])
                    if check is True:
                        time.sleep(prod_id[2])
                    else:
                        self.marketplace.logging.error(
                            '{} product failed to publish, retrying republish'.format(prod_id[0]))
                        time.sleep(self.republish_wait_time)
