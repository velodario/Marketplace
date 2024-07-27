# Marketplace

# Overview
The purpose of this project is to find synchronization methods to differentiate the actions of Producers and Consumers in how they use Products. For this method, I have chosen to use semaphores. A Semaphore maintains an internal counter that is decremented by a call to acquire() and incremented by a call to release(). The acquire() method will not allow the counter to decrement below 0, blocking the thread's execution in this case until the counter is incremented by a release(). Initially, I used two semaphores, one for the Consumer and one for the Producer. These semaphores, initialized with 1, will identify these components by IDs.

# Producer
When a Producer enters the flow, it will receive an ID and then proceed to publish its products, adhering to wait conditions if it fails. If a product is successfully added, it will be added to a dictionary with the key being the producer's ID and the value being an appended list of each published product for this producer, along with the product's availability. The product's availability differs based on the Consumer's actions in the marketplace.

# Consumer
Consumers have their own dictionary, with the key being the consumer's ID and the value being a list of products. If a Consumer adds a product to their cart, this product will be added to their list, and in the producer's dictionary, this product will no longer be available. For availability, I initialized a boolean variable.

# Synchronization
Another semaphore is used when displaying the final products to a Consumer. This is necessary because, in files with large inputs, there were race condition cases, and the products were not displayed correctly. Logging is used extensively in almost every function to track results from both classes, with the .info extension for standard operations and the .error extension for error cases. The log files are split with a maxBytes=100000.