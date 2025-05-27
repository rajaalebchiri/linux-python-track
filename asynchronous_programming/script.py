import asyncio

async def order_coffee(customer_name, order):
    print(f"{customer_name} orders coffee")
    print(f"barista prepping {order} for {customer_name}")
    if order == "cappuccino":
        await asyncio.sleep(4)
    elif order == "latte":
        await asyncio.sleep(3)
    elif order == "espresso":
        await asyncio.sleep(3)
    else:
        raise asyncio.CancelledError("Order Cancelled")
    print(f"Coffee Ready for {customer_name}")

async def prepping():
    queue = asyncio.Queue()
    customers = ["alice", "Bob", "Charlie", "David"]
    orders = ["latte", "cappuccino", "espresso", "double espresso"]
    tasks = [
        asyncio.create_task(order_coffee(c, o))
        for c, o in zip(customers, orders)
    ]
    try:
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=3.5)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(prepping())
