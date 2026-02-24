-- aqi calculation US EPA formula 
use delhiAqi;
SELECT 
    YEAR(date) as year,
    ROUND(AVG(pm25), 1) as avg_pm25,
    ROUND(AVG(pm10), 1) as avg_pm10,
    ROUND(AVG(no2), 1) as avg_no2,
    -- AQI approximation from PM2.5
    ROUND(AVG(
        CASE 
            WHEN pm25 <= 12    THEN (50/12) * pm25
            WHEN pm25 <= 35.4  THEN 50 + (50/23.4) * (pm25 - 12)
            WHEN pm25 <= 55.4  THEN 100 + (50/20) * (pm25 - 35.4)
            WHEN pm25 <= 150.4 THEN 150 + (50/95) * (pm25 - 55.4)
            WHEN pm25 <= 250.4 THEN 200 + (100/100) * (pm25 - 150.4)
            WHEN pm25 <= 350.4 THEN 300 + (100/100) * (pm25 - 250.4)
            ELSE 400 + (100/149.6) * (pm25 - 350.4)
        END
    ), 1) as calculated_aqi
FROM aqi_historical
WHERE pm25 IS NOT NULL
GROUP BY YEAR(date)
ORDER BY year;