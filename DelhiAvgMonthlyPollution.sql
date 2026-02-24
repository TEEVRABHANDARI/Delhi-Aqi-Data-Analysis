use delhiAqi;

SELECT 
    MONTH(date) as month,
    MONTHNAME(date) as month_name,
    ROUND(AVG(pm25), 1) as avg_pm25
FROM aqi_historical
WHERE pm25 IS NOT NULL
GROUP BY MONTH(date), MONTHNAME(date)
ORDER BY avg_pm25 DESC;