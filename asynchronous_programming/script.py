import asyncio
from asyncio import Queue
from random import randrange

class Order:
    def __init__(self, order_name: str, prepping_time: int):
        self.order_name = order_name
        self.prep_time = prepping_time

class Customer:
    def __init__(self, id: int, customer_name: str, order: Order):
        self.id = id
        self.customer_name = customer_name
        self.order = order

async def place_order(queue: Queue, id: int, name: str, order_name: str, prepping_time: int):
    order = Order(order_name= order_name, prepping_time=prepping_time)
    customer = Customer(id=id, customer_name=name, order=order)
    await queue.put(customer)

async def prepping_order(queue: Queue, i: int):
    while not queue.empty():
        customer: Customer = await queue.get()
        print(f"The barista number {i} prepping the order {customer.order.order_name} for customer {customer.customer_name}")
        await asyncio.sleep(customer.order.prep_time)
        queue.task_done()
        print("The order is ready")


async def main():
    queue = Queue()
    customers = [
        {
            "id": 1, 
            "customer_name": "David", 
            "order_name": "espresso", 
            "prepping_time": .3
        },
        {
            "id": 2, 
            "customer_name": "Jack",
            "order_name": "latte", 
            "prepping_time": .5
        },
        {
            "id": 3, 
            "customer_name": "SOMETHING",
            "order_name": "double esporesso",
            "prepping_time": .7
        }    
    ]
    

    orders = [place_order(queue=queue, id=customer["id"], name=customer["customer_name"], order_name=customer["order_name"], prepping_time=customer["prepping_time"]) for customer in customers]
    await asyncio.gather(*orders)


    baristas = [asyncio.create_task(prepping_order(queue=queue, i=i)) for i in range(3)]


    await queue.join()

    for b in baristas:
        b.cancel()

if __name__ == "__main__":
    asyncio.run(main())
