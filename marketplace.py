"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Semaphore
import logging
from logging.handlers import RotatingFileHandler


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producer_storage = {}  # stores pairs [Product, bool]
        self.id_producer = 0
        self.id_consumer = 0
        self.consumer_cart = {}
        # semaphore to add a different id for each consumer
        self.sem_consumer_reg = Semaphore(1)
        # semaphore to add a different id for each producer
        self.sem_producer_reg = Semaphore(1)
        # semaphore for product display for thread safety
        self.print_order = Semaphore(1)
        logging.basicConfig(
            handlers=[RotatingFileHandler(
                'marketplace.log', maxBytes=100000, backupCount=10)],
            level=logging.INFO
        )

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.sem_producer_reg.acquire()
        self.id_producer += 1
        logging.info('Added producer id {}'.format(self.id_producer))
        self.producer_storage[self.id_producer] = [[]]
        self.sem_producer_reg.release()
        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: int
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns: True or False. If the caller receives False, it should wait and then try again.
        """
        current_product = [product, True]  # add product and its availability
        complete_storage = None

        for key in self.producer_storage:
            if key == producer_id:
                if len(self.producer_storage[key]) < self.queue_size_per_producer:
                    self.producer_storage[key].append(current_product)
                    logging.info('{} successfully published in the marketplace'.format(current_product))
                    complete_storage = True
                else:
                    complete_storage = False
                break
        return complete_storage

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns: an int representing the cart_id
        """
        self.sem_consumer_reg.acquire()
        self.id_consumer += 1
        logging.info('Added consumer id {}'.format(self.id_consumer))
        self.consumer_cart[self.id_consumer] = []
        self.sem_consumer_reg.release()
        return self.id_consumer

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.

        :type cart_id: int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns: True or False. If the caller receives False, it should wait and then try again.
        """
        last_length = len(self.consumer_cart[cart_id])
        self.consumer_cart[cart_id].append(product)
        current_length = len(self.consumer_cart[cart_id])
        added_product = current_length > last_length

        if added_product:
            logging.info('{} added to cart'.format(product))
        else:
            logging.error('{} failed to add to cart'.format(product))

        for key, value in self.producer_storage.items():
            if key == product:
                value[1] = False
                break
        return added_product

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        current_cart = self.consumer_cart[cart_id]
        current_cart.remove(product)
        self.consumer_cart[cart_id] = current_cart
        logging.info('{} removed from cart'.format(product))

        for key, value in self.producer_storage.items():
            if key == product and not value[1]:
                value[1] = True
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: int
        :param cart_id: id cart
        """
        logging.info('Order placed {}'.format(self.consumer_cart[cart_id]))
        return self.consumer_cart[cart_id]
