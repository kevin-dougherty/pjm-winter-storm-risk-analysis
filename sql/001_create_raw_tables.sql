-- Raw layer: mirrors the PJM hrl_load_metered feed as closely as possible.
-- Grain: one row = one hour of metered load for one load_area.
-- NOTE: load_area 'RTO' is the PJM-wide TOTAL. Exclude it when summing zones.
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.pjm_load_hourly (
    datetime_beginning_utc  TIMESTAMP  NOT NULL,
    datetime_beginning_ept  TIMESTAMP  NOT NULL,
    nerc_region             VARCHAR,
    mkt_region              VARCHAR,
    zone                    VARCHAR    NOT NULL,
    load_area               VARCHAR    NOT NULL,
    mw                      DOUBLE     NOT NULL,
    is_verified             BOOLEAN,
    ingested_at             TIMESTAMP  DEFAULT current_timestamp,
    PRIMARY KEY (datetime_beginning_utc, load_area)
);
