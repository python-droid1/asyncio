import asyncio

async def fetch_slow_service():
    print("Service: Connecting to microservice...")
    await asyncio.sleep(10)
    print("Service: Data retrieved!")
    return {"status": "success"}

async def main():
    print("Main: Requesting data with a 3-second timeout limit...")
    try:
        result = await asyncio.wait_for(fetch_slow_service(), timeout=3.0)
        print(f"Main: Received result: {result}")
    except asyncio.TimeoutError:
        print("Main: The microservice took too long and was cancelled!")

asyncio.run(main())







import asyncio

async def fetch_fast():
    print("Fast Service: Connecting...")
    await asyncio.sleep(1)
    print("Fast Service: Done!")
    return "Fast Data"

async def fetch_slow():
    print("Slow Service: Connecting...")
    await asyncio.sleep(5)
    print("Slow Service: Done!")
    return "Slow Data"

async def main():
    try:
        print("Main: Launching both services with a 3-second total timeout...")
        
        # Wrapping gather inside the timeout
        results = await asyncio.wait_for(
            asyncio.gather(fetch_fast(), fetch_slow()), 
            timeout=3.0
        )
        print(f"Main: Success! Collected: {results}")
        
    except asyncio.TimeoutError:
        print("Main: Timeout triggered! The group took too long.")

asyncio.run(main())