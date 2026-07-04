import asyncio
import aiohttp

async def background_counter():
    for i in range(1, 5):
        print(f"Counter: Checking in {i}...")
        await asyncio.sleep(0.2)

async def fetch_google():
    print("Fetch: Starting request to Google...")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.google.com") as response:
            status = response.status
            print(f"Fetch: Got response from Google with status {status}")

async def main():
    await asyncio.gather(
        fetch_google(),
        background_counter()
    )

asyncio.run(main())


# ===============================
# Section 
# ===============================


import asyncio

async def check_stock():
    print("Store: Checking inventory...")
    await asyncio.sleep(1.5)  # Simulating database lookup
    print("Store: Item is in stock!")
    return True

async def process_payment():
    print("Payment: Contacting bank...")
    await asyncio.sleep(2.0)  # Simulating credit card processing
    print("Payment: Charge approved!")
    return True

async def main():
    print("--- Checkout Started ---")
    
    # gather runs both concurrently and waits for all results
    results = await asyncio.gather(
        check_stock(),
        process_payment()
    )
    
    # results contains [stock_status, payment_status]
    in_stock = results[0]
    payment_success = results[1]
    
    if in_stock and payment_success:
        print("Server: Both tasks passed! Order Shipped!")
    else:
        print("Server: Order failed.")

asyncio.run(main())


# ===============================
# Semaphores 
# ===============================

import asyncio

async def access_resource(task_id, semaphore):
    # async with automatically acquires and releases the semaphore key
    async with semaphore:
        print(f"Task {task_id}: Entered the resource.")
        await asyncio.sleep(2)
        print(f"Task {task_id}: Leaving the resource.")

async def main():
    # Allow a maximum of 2 tasks at the same time
    sem = asyncio.Semaphore(2)
    
    # Launch 4 tasks concurrently
    await asyncio.gather(
        access_resource(1, sem),
        access_resource(2, sem),
        access_resource(3, sem),
        access_resource(4, sem)
    )

asyncio.run(main())