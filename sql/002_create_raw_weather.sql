-- Raw layer: routine hourly (FM15) reports from NOAA GHCNh.
-- Grain: one row = one FM15 report at one station (an hour CAN have more than one).
-- Times are UTC. Temperature and dew point in deg C.
-- Deduplication to one-per-hour happens in the clean layer, not here.
CREATE TABLE IF NOT EXISTS raw.ghcnh_fm15 (
    station                             VARCHAR    NOT NULL,
    obs_time                            TIMESTAMP  NOT NULL,   -- GHCNh "DATE", UTC
    temperature                         DOUBLE     NOT NULL,
    temperature_quality_code            VARCHAR,
    dew_point_temperature               DOUBLE,
    dew_point_temperature_quality_code  VARCHAR,
    wind_speed                          DOUBLE,
    wind_speed_quality_code             VARCHAR,
    wind_direction                      DOUBLE,
    wind_direction_quality_code         VARCHAR,
    source_file                         VARCHAR,
    ingested_at                         TIMESTAMP  DEFAULT current_timestamp,
    PRIMARY KEY (station, obs_time)
);