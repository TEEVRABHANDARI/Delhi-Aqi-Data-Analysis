Use delhiAqi;
--  Odd-Even periods vs normal
SELECT 
    CASE
        WHEN date BETWEEN '2016-01-01' AND '2016-01-15' THEN 'Odd-Even Jan 2016'
        WHEN date BETWEEN '2016-04-15' AND '2016-04-30' THEN 'Odd-Even Apr 2016'
        WHEN date BETWEEN '2017-11-13' AND '2017-11-17' THEN 'Odd-Even Nov 2017'
        ELSE 'Normal'
    END as period,
    ROUND(AVG(no2), 2) as avg_no2,
    ROUND(AVG(pm25), 2) as avg_pm25,
    COUNT(*) as days
FROM aqi_historical
GROUP BY period
ORDER BY avg_pm25;