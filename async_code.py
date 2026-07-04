import asyncio

async def fetch_data(id, delay):
    print(f"Task {id}: Starting...")
    await asyncio.sleep(delay)
    print(f"Task {id}: Done!")

async def main():
    await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 3)
    )

asyncio.run(main())