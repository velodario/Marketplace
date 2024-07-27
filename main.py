from consumer import Consumer
from producer import Producer
from marketplace import Marketplace
from product import Tea, Coffee

if __name__ == "__main__":
    # Initialize Marketplace
    marketplace = Marketplace(queue_size_per_producer=10)

    # Define products
    tea = Tea(name="Green Tea", price=10, type="Green")
    coffee = Coffee(name="Espresso", price=20, acidity="Medium", roast_level="Dark")

    # Define producer's product list (product, quantity, wait_time)
    producer_products = [(tea, 5, 2), (coffee, 3, 1)]

    # Initialize Producer
    producer = Producer(products=producer_products, marketplace=marketplace, republish_wait_time=1)
    
    # Define consumer's cart actions
    consumer_carts = [
        [{"type": "add", "product": tea, "quantity": 2}],
        [{"type": "add", "product": coffee, "quantity": 1}]
    ]

    # Initialize Consumers
    consumers = [Consumer(carts=consumer_carts, marketplace=marketplace, retry_wait_time=1)]

    # Start Producer and Consumers
    producer.start()
    for consumer in consumers:
        consumer.start()

    # Join threads
    producer.join()
    for consumer in consumers:
        consumer.join()
