
-- Step 1: Drop everything and start clean
DROP TABLE IF EXISTS aqi_live;
DROP TABLE IF EXISTS aqi_historical;

-- Step 2: Rebuild aqi_live (stores daily snapshots forever)
CREATE TABLE aqi_live (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    station         VARCHAR(200),
    city            VARCHAR(100),
    state           VARCHAR(100),
    pollutant_id    VARCHAR(50),
    pollutant_min   FLOAT,
    pollutant_max   FLOAT,
    pollutant_avg   FLOAT,
    last_update     DATETIME,
    latitude        FLOAT,
    longitude       FLOAT,
    fetched_date    DATE,
    UNIQUE KEY no_duplicates (station, pollutant_id, fetched_date)
);

-- Step 3: Rebuild aqi_historical (Kaggle station data 2010-2023)
CREATE TABLE aqi_historical (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    station     VARCHAR(200),
    city        VARCHAR(100),
    date        DATE,
    pm25        FLOAT,
    pm10        FLOAT,
    no2         FLOAT,
    so2         FLOAT,
    co          FLOAT,
    ozone       FLOAT,
    UNIQUE KEY no_duplicates (station, date)
);


select * from aqi_live;

select * from aqi_historical;