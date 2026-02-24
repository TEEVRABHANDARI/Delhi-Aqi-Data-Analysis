--  Weekend vs weekday NO2
use delhiAqi;
SELECT 
    CASE 
        WHEN DAYOFWEEK(date) IN (1,7) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    ROUND(AVG(no2), 2) as avg_no2,
    ROUND(AVG(pm25), 2) as avg_pm25
FROM aqi_historical
WHERE no2 IS NOT NULL
GROUP BY day_type;
