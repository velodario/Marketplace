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
        self.producer_storage = {}  # pastreaza perechile [Product, bool]
        self.id_producer = 0
        self.id_consumer = 0
        self.consumer_cart = {}
        # semafor pentru a adauga id diferit pentru fiecare consumator
        self.sem_consumer_reg = Semaphore(1)
        # semafor pentru a adauga id diferit pentru fiecare producator
        self.sem_producer_reg = Semaphore(1)
        # semafor la afisarea produselor pentru thread safety
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
        self.id_producer = self.id_producer + 1
        logging.info('adaugat id producator {}'.format(self.id_producer))
        self.producer_storage[self.id_producer] = [[]]
        # adaugam id nou in dictionar
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
        current_product.append(product)  # adaugam Produsul in lista
        current_product.append(True)  # adaugam disponibilitatea Produsului
        complete_storage = None

        for keys in self.producer_storage:  # pentru fiecare id cheie
            if keys == producer_id:  # daca gasim id-ul
                # daca este loc in lista de produse cu acest id
                if len(self.producer_storage[keys]) < self.queue_size_per_producer:
                    self.producer_storage[keys].append(
                        current_product)  # adaugam produsul in lista
                    logging.info(
                        '{} publicat in marketplace cu succes'.format(current_product))
                    complete_storage = True
                    break
                else:
                    complete_storage = False  # altfel nu e loc, intoarcem false
        return complete_storage

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.sem_consumer_reg.acquire()
        self.id_consumer = self.id_consumer + 1
        logging.info('adaugat id consumator {}'.format(self.id_consumer))
        # adaugam id nou in dictionar
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
        # lungimea listei inainte de a adauga produsul
        last_length = len(self.consumer_cart[cart_id])
        # adaug produsul in lista de produse la consumator (cart)
        self.consumer_cart[cart_id].append(product)
        # lungimea listei dupa adaugarea produsului
        current_length = len(self.consumer_cart[cart_id])
        # daca lungimea dupa mai mare decat inainte, produsul este adaugat
        if current_length > last_length:
            logging.info('{} added to cart'.format(product))
            added_product = True
        else:
            logging.error('{} failed to add to cart'.format(product))
            added_product = False

        # parcurg produsele in dictionarul de producatorii
        for value in self.producer_storage.items():
            if value[0] == product:  # daca produsul exista
                # nu mai este disponibil deoarece este adaugat in cart
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
        current_cart = self.consumer_cart[cart_id]  # primesc lista de produse cu acest id
        current_cart.remove(product)  # sterg produsul din lista

        self.consumer_cart[cart_id] = current_cart  # actualizez lista
        logging.info('{} removed from cart'.format(product))
        for value in self.producer_storage.items():
            # daca produsul exista in dictionarul de producator si nu este disponibil
            if value[0] == product and value[1] is False:
                # acum este disponibil deoarece este sters din cart
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
