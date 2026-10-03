from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "pjm_risk.duckdb"
RAW_DIR = ROOT / "data" / "raw" / "pjm" / "hrl_load_metered"

UPSERT_SQL = """
    INSERT INTO raw.pjm_load_hourly
        (datetime_beginning_utc, datetime_beginning_ept, nerc_region, mkt_region,
         zone, load_area, mw, is_verified)
    SELECT datetime_beginning_utc, datetime_beginning_ept, nerc_region, mkt_region,
           zone, load_area, mw, is_verified
    FROM read_csv_auto('{path}')
    ON CONFLICT (datetime_beginning_utc, load_area) DO UPDATE SET
        mw          = EXCLUDED.mw,
        is_verified = EXCLUDED.is_verified,
        ingested_at = now()
"""

def main():
    con = duckdb.connect(str(DB_PATH))
    for csv in sorted(RAW_DIR.glob("*.csv")):
        before = con.sql("SELECT COUNT(*) FROM raw.pjm_load_hourly").fetchone()[0]
        con.execute(UPSERT_SQL.format(path=csv.as_posix()))
        after = con.sql("SELECT COUNT(*) FROM raw.pjm_load_hourly").fetchone()[0]
        print(f"{csv.name}: {after - before:+,} new rows (table total {after:,})")
    con.close()

if __name__ == "__main__":
    main()
