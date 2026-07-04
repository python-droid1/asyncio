import asyncio
from pathlib import Path
import aiohttp
import time


async def fetch_and_save():
    base_url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master"
    years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026]
    download_dir = Path("worldcups")
    download_dir.mkdir(exist_ok=True)

    async def fetch(year, session):
        try:
            async with session.get(f"{base_url}/{year}/worldcup.json") as response:
                response.raise_for_status()
                text = await response.text()
                (download_dir / f"{year}.json").write_text(text, encoding="utf-8")
                print(f"[OK] {year}")
        except Exception as e:
            print(f"[FAIL] {year}: {e}")

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch(year, session) for year in years))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(fetch_and_save())
    print(f'Time: {time.perf_counter() - start}')

