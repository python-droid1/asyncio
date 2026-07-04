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


# ===============================
# Semaphore, timeout, erro handling 
# ===============================


import asyncio
import aiohttp

async def fetch_url(session, url, semaphore):
    # The semaphore ensures only 2 requests hit the network at the exact same time
    async with semaphore:
        try:
            print(f"Fetcher: Requesting {url}...")
            
            # Set a strict 2-second timeout for the network request
            async with asyncio.wait_for(session.get(url), timeout=2.0) as response:
                data = await response.text()
                print(f"Fetcher: Successfully retrieved {url} ({len(data)} bytes)")
                return data
                
        except asyncio.TimeoutError:
            print(f"Error: {url} timed out after 2 seconds!")
            return None
        except aiohttp.ClientError as e:
            print(f"Error: Network issue connecting to {url}: {e}")
            return None

async def main():
    urls = [
        "https://www.google.com",
        "https://www.httpbin.org/delay/5",  # This will trigger our timeout error
        "https://this-is-a-broken-url.xyz", # This will trigger a network connection error
        "https://www.python.org"
    ]
    
    # Limit to a maximum of 2 concurrent connections
    sem = asyncio.Semaphore(2)
    
    async with aiohttp.ClientSession() as session:
        # Bundle all tasks together using a list comprehension
        tasks = [fetch_url(session, url, sem) for url in urls]
        
        print("Main: Starting concurrent requests...")
        results = await asyncio.gather(*tasks)
        print("Main: All tasks finished processing.")

asyncio.run(main())