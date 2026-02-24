
CREATE DATABASE IF NOT EXISTS DelhiAqi;
USE DelhiAqi;

CREATE TABLE IF NOT EXISTS aqi_live (
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

CREATE TABLE IF NOT EXISTS aqi_historical (
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