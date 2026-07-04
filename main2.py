from pathlib import Path
import requests
import time


def fetch_and_save():
    base_url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master"
    years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026]
    download_dir = Path("worldcups")
    download_dir.mkdir(exist_ok=True)

    with requests.Session() as session:
        for year in years:
            try:
                response = session.get(f"{base_url}/{year}/worldcup.json", timeout=30)
                response.raise_for_status()
                (download_dir / f"{year}.json").write_text(response.text, encoding="utf-8")
                print(f"[OK] {year}")
            except Exception as e:
                print(f"[FAIL] {year}: {e}")


if __name__ == "__main__":
    start = time.perf_counter()
    fetch_and_save()
    print(f'Time: {time.perf_counter() - start}')
