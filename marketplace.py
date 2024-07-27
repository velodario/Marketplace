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
        self.producer_storage = {}  # stores [Product, bool] pairs
        self.id_producer = 0
        self.id_consumer = 0
        self.consumer_cart = {}
        # semaphore for adding different id for each consumer
        self.sem_consumer_reg = Semaphore(1)
        # semaphore for adding different id for each producer
        self.sem_producer_reg = Semaphore(1)
        # semaphore for displaying products for thread safety
        self.print_order = Semaphore(1)
        logging.basicConfig(
            handlers=[RotatingFileHandler(
                'marketplace.log', maxBytes=100000, backupCount=10)],
            level=logging.INFO)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.sem_producer_reg.acquire()
        self.id_producer += 1
        logging.info('Producer id {} added'.format(self.id_producer))
        self.producer_storage[self.id_producer] = [[]]
        # add new id to dictionary
        self.sem_producer_reg.release()
        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        current_product = []
        current_product.append(product)  # add product to list
        current_product.append(True)  # add product availability
        complete_storage = None

        for keys in self.producer_storage:  # for each id key
            if keys == producer_id:  # if id is found
                # if there is space in the list of products with this id
                if len(self.producer_storage[keys]) < self.queue_size_per_producer:
                    self.producer_storage[keys].append(current_product)  # add product to list
                    logging.info(
                        '{} successfully published in the marketplace'.format(current_product))
                    complete_storage = True
                    break
                else:
                    complete_storage = False  # otherwise there is no space, return false
        return complete_storage

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.sem_consumer_reg.acquire()
        self.id_consumer += 1
        logging.info('Consumer id {} added'.format(self.id_consumer))
        # add new id to dictionary
        self.consumer_cart[self.id_consumer] = []
        self.sem_consumer_reg.release()
        return self.id_consumer

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        added_product = None
        # length of the list before adding the product
        last_length = len(self.consumer_cart[cart_id])
        # add product to the list of products for the consumer (cart)
        self.consumer_cart[cart_id].append(product)
        # length of the list after adding the product
        current_length = len(self.consumer_cart[cart_id])
        # if length after is greater than before, the product is added
        if current_length > last_length:
            logging.info('{} added to cart'.format(product))
            added_product = True
        else:
            logging.error('{} failed to add to cart'.format(product))
            added_product = False

        # go through the products in the producer dictionary
        for value in self.producer_storage.items():
            if value[0] == product:  # if the product exists
                # it is no longer available as it is added to the cart
                value[1] = False
                break
        return added_product

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        current_cart = self.consumer_cart[cart_id]  # get the list of products with this id
        current_cart.remove(product)  # remove the product from the list

        self.consumer_cart[cart_id] = current_cart  # update the list
        logging.info('{} removed from cart'.format(product))
        for value in self.producer_storage.items():
            # if the product exists in the producer dictionary and is not available
            if value[0] == product and value[1] is False:
                # now it is available as it is removed from the cart
                value[1] = True
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logging.info('order placed {}'.format(self.consumer_cart[cart_id]))
        return self.consumer_cart[cart_id]