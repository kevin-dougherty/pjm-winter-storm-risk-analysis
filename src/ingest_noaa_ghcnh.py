from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "pjm_risk.duckdb"
RAW_DIR = ROOT / "data" / "raw" / "noaa" / "ghcnh"

UPSERT_SQL = """
    INSERT INTO raw.ghcnh_fm15
        (station, obs_time,
         temperature, temperature_quality_code,
         dew_point_temperature, dew_point_temperature_quality_code,
         wind_speed, wind_speed_quality_code,
         wind_direction, wind_direction_quality_code,
         source_file)
    SELECT CAST(STATION AS VARCHAR),
           CAST(DATE AS TIMESTAMP),
           CAST(temperature AS DOUBLE),
           CAST(temperature_Quality_Code AS VARCHAR),
           CAST(dew_point_temperature AS DOUBLE),
           CAST(dew_point_temperature_Quality_Code AS VARCHAR),
           CAST(wind_speed AS DOUBLE),
           CAST(wind_speed_Quality_Code AS VARCHAR),
           CAST(wind_direction AS DOUBLE),
           CAST(wind_direction_Quality_Code AS VARCHAR),
           '{file_name}'
    FROM read_csv_auto('{path}', sep='|')
    WHERE temperature_Report_Type = 'FM15'
      AND temperature IS NOT NULL
    ON CONFLICT (station, obs_time) DO UPDATE SET
        temperature                        = EXCLUDED.temperature,
        temperature_quality_code           = EXCLUDED.temperature_quality_code,
        dew_point_temperature              = EXCLUDED.dew_point_temperature,
        dew_point_temperature_quality_code = EXCLUDED.dew_point_temperature_quality_code,
        wind_speed                         = EXCLUDED.wind_speed,
        wind_speed_quality_code            = EXCLUDED.wind_speed_quality_code,
        wind_direction                     = EXCLUDED.wind_direction,
        wind_direction_quality_code        = EXCLUDED.wind_direction_quality_code,
        source_file                        = EXCLUDED.source_file,
        ingested_at                        = now()
"""

def main():
    con = duckdb.connect(str(DB_PATH))
    for f in sorted(RAW_DIR.glob("*.psv")):
        before = con.sql("SELECT COUNT(*) FROM raw.ghcnh_fm15").fetchone()[0]
        con.execute(UPSERT_SQL.format(path=f.as_posix(), file_name=f.name))
        after = con.sql("SELECT COUNT(*) FROM raw.ghcnh_fm15").fetchone()[0]
        print(f"{f.name}: {after - before:+,} new rows (table total {after:,})")
    con.close()

if __name__ == "__main__":
    main()
