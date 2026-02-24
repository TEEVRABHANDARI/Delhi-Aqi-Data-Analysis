# Delhi AQI Analysis Dashboard

## The Problem
Delhi's air quality data exists but is buried in government portals. 
Residents have no simple way to answer: is today safe to go outside?

## What I Built
An automated pipeline pulling live data from India's official CPCB API 
into a Power BI dashboard — updated daily via Windows Task Scheduler.

## Key Findings
- Delhi has never had a safe air year since 2010 — every year averaged 
  3.5x India's own legal PM2.5 limit
- 2020 was the cleanest year in a decade — not policy, COVID lockdown
- Odd-even scheme ran during crisis days — PM2.5 still 2x annual average
- Weekend traffic restrictions move NO2 by just 4%
- NO2 down 22% since 2010. PM2.5 barely moved. Different problem entirely.

## Tech Stack
- Python (requests, pandas, mysql-connector) — API pipeline
- MySQL — data storage (113,918 historical rows + live daily data)
- Power BI — dashboard and DAX measures
- Windows Task Scheduler — daily automation
- Data: CPCB Government API (live) + Kaggle historical 2010–2023

## Dashboard Pages
1. Live Monitor — real time station map, AQI cards
2. Historical Trends — 13 year pollutant analysis
3. Pollutant Deep Dive — what improved vs what didn't
4. Weekday vs Weekend — traffic impact analysis
<img width="1300" height="734" alt="image" src="https://github.com/user-attachments/assets/4d70e600-0b1b-4b24-89dd-4d7e1b0b6e81" />
<img width="1311" height="747" alt="image" src="https://github.com/user-attachments/assets/cba45726-c080-491f-863d-e852739efe7e" />
<img width="1324" height="751" alt="image" src="https://github.com/user-attachments/assets/efb4c655-e0ea-4d92-8dd4-c01066d46ff6" />
<img width="1295" height="734" alt="image" src="https://github.com/user-attachments/assets/f39a3ae5-6183-4197-9cc8-6301729846f2" />

## Data Sources
- Live: data.gov.in CPCB API
- Historical: CPCB station data 2010–2023
