-- Raw layer: data stored as close to the source as possible.
-- One row = one hour of metered load for one load area.
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.pjm_load_hourly (
    datetime_beginning_utc  TIMESTAMP   NOT NULL,  -- the true key; never ambiguous
    datetime_beginning_ept  TIMESTAMP   NOT NULL,  -- local prevailing time, kept for readability
    area                    VARCHAR     NOT NULL,  -- e.g. 'RTO', 'PS'
    load_mw                 DOUBLE      NOT NULL,
    is_verified             BOOLEAN,
    ingested_at             TIMESTAMP   DEFAULT current_timestamp,
    PRIMARY KEY (datetime_beginning_utc, area)
);