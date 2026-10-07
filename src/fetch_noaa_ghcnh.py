from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "noaa" / "ghcnh"

BASE_URL = ("https://www.ncei.noaa.gov/oa/global-historical-climatology-network"
            "/hourly/access/by-year")
STATION = "USW00014734"        # Newark (KEWR), GHCN station ID
YEARS = range(2018, 2027)      # calendar years covering winters 2018-19 .. 2025-26

def fetch_year(year: int) -> None:
    out_file = OUT_DIR / f"GHCNh_{STATION}_{year}.psv"

    if out_file.exists() and out_file.stat().st_size > 0:
        print(f"{out_file.name}: already downloaded, skipping")
        return

    url = f"{BASE_URL}/{year}/psv/GHCNh_{STATION}_{year}.psv"
    response = requests.get(url, timeout=300)
    response.raise_for_status()

    if not response.content.strip():
        raise ValueError(f"{url} returned an empty file; not saving it")

    out_file.write_bytes(response.content)
    n_rows = response.content.count(b"\n") - 1
    print(f"{out_file.name}: {n_rows:,} rows")

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for year in YEARS:
        fetch_year(year)

if __name__ == "__main__":
    main()
