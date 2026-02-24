--  Year on year improvement

use delhiAqi;
SELECT 
    YEAR(date) as year,
    ROUND(AVG(pm25), 1) as avg_pm25,
    ROUND(AVG(pm10), 1) as avg_pm10,
    ROUND(AVG(no2), 1) as avg_no2
FROM aqi_historical
WHERE pm25 IS NOT NULL
GROUP BY YEAR(date)
ORDER BY year;