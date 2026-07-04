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