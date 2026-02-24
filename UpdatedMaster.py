import requests
import pandas as pd
import mysql.connector
from datetime import date
import os
import time

API_KEY     = "your_actual_key_here"
BASE_URL    = "your_actual_url_here"
DB_PASSWORD = "your_actual_password_here"
KAGGLE_FOLDER = r"C:\Users\Deel\Desktop\Project streaming\DelhiAQI\delhiKaggleData"
LIVE_FOLDER   = r"C:\Users\Deel\Desktop\Project streaming\DelhiAQI\delhiLiveData"

# SETUP
os.makedirs(LIVE_FOLDER, exist_ok=True)

print("Connecting to MySQL...")
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=DB_PASSWORD,
    database="DelhiAqi"
)
cursor = conn.cursor()
print("Connected.\n")

today = date.today()

def safe_float(val):
    try:
        return float(val) if pd.notna(val) else None
    except:
        return None

#api
print(f"--- JOB 1: Fetching live data for {today} ---")

POLLUTANTS = ["PM2.5", "PM10", "NO2", "SO2", "CO", "OZONE"]

# Delete today data and store yesterday data permanently
cursor.execute("DELETE FROM aqi_live WHERE fetched_date = %s", (today,))
conn.commit()

insert_live = """
    INSERT IGNORE INTO aqi_live 
    (station, city, state, pollutant_id, pollutant_min, pollutant_max,
     pollutant_avg, last_update, latitude, longitude, fetched_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

total_live = 0
all_today  = []
for pollutant in POLLUTANTS:
    params = {
        "api-key"              : API_KEY,
        "format"               : "json",
        "limit"                : "500",
        "filters[state]"       : "Delhi",
        "filters[city]"        : "Delhi",
        "filters[pollutant_id]": pollutant
    }

    try:
        # Retry up to 3 times on timeout
        r = None
        for attempt in range(3):
            try:
                r = requests.get(BASE_URL, params=params, timeout=30)
                break
            except requests.exceptions.Timeout:
                print(f"    Timeout attempt {attempt+1}/3, retrying...")
                time.sleep(5)

        if r is None:
            print(f"    All 3 attempts failed for {pollutant}, skipping")
            continue

        print(f"  {pollutant} — status: {r.status_code}")

        records = r.json().get("records", [])
        rows = []

        for rec in records:
            row = (
                str(rec.get("station",      "")),
                str(rec.get("city",         "")),
                str(rec.get("state",        "")),
                str(rec.get("pollutant_id", "")),
                safe_float(rec.get("min_value")),
                safe_float(rec.get("max_value")),
                safe_float(rec.get("avg_value")),
                str(rec.get("last_update",  "")),
                safe_float(rec.get("latitude")),
                safe_float(rec.get("longitude")),
                today
            )
            rows.append(row)
            all_today.append(row)

        if rows:
            cursor.executemany(insert_live, rows)
            conn.commit()
            total_live += len(rows)
            print(f"    Inserted {len(rows)} stations into MySQL")
        else:
            print(f"    No records returned")

    except Exception as e:
        print(f"    ERROR for {pollutant}: {e}")

    time.sleep(1)
# Save today's full live snapshot as CSV
if all_today:
    df_today = pd.DataFrame(all_today, columns=[
        "station", "city", "state", "pollutant_id",
        "pollutant_min", "pollutant_max", "pollutant_avg",
        "last_update", "latitude", "longitude", "fetched_date"
    ])
    csv_path = os.path.join(LIVE_FOLDER, f"delhi_live_{today}.csv")
    df_today.to_csv(csv_path, index=False)
    print(f"\n  Saved CSV: {csv_path}")

print(f"\nJOB 1 COMPLETE — {total_live} live rows inserted for {today}\n")

# kaggle data
print("--- JOB 2: Checking historical data ---")

cursor.execute("SELECT COUNT(*) FROM aqi_historical")
hist_count = cursor.fetchone()[0]
print(f"  Current rows in aqi_historical: {hist_count}")

if hist_count == 0:
    print("  Table is empty — loading Kaggle data now...")
    print("  This takes 2-5 minutes. Do not close the terminal.\n")

    df_stations = pd.read_csv(os.path.join(KAGGLE_FOLDER, "stations_info.csv"))
    df_stations = df_stations[df_stations["state"] == "Delhi"][
                    ["file_name", "station_location", "city"]
                  ]

    insert_hist = """
        INSERT IGNORE INTO aqi_historical
        (station, city, date, pm25, pm10, no2, so2, co, ozone)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    col_map = {
        "PM2.5 (ug/m3)" : "pm25",
        "PM10 (ug/m3)"  : "pm10",
        "NO2 (ug/m3)"   : "no2",
        "SO2 (ug/m3)"   : "so2",
        "CO (mg/m3)"    : "co",
        "Ozone (ug/m3)" : "ozone",
    }

    delhi_files = sorted([f for f in os.listdir(KAGGLE_FOLDER) if f.startswith("DL")])
    total_hist  = 0

    for file in delhi_files:
        station_code = file.replace(".csv", "")
        match        = df_stations[df_stations["file_name"] == station_code]
        station_name = match["station_location"].values[0] if len(match) > 0 else station_code

        try:
            df = pd.read_csv(os.path.join(KAGGLE_FOLDER, file))
            df.columns = df.columns.str.strip()
            df["From Date"] = pd.to_datetime(df["From Date"], errors="coerce")
            df = df.dropna(subset=["From Date"])
            df = df.set_index("From Date")

            existing = {k: v for k, v in col_map.items() if k in df.columns}
            df = df[list(existing.keys())]
            df.columns = list(existing.values())

            df_daily = df.resample("D").mean().reset_index()

            rows = []
            for _, row in df_daily.iterrows():
                rows.append((
                    station_name,
                    "Delhi",
                    row["From Date"].date(),
                    safe_float(row.get("pm25")),
                    safe_float(row.get("pm10")),
                    safe_float(row.get("no2")),
                    safe_float(row.get("so2")),
                    safe_float(row.get("co")),
                    safe_float(row.get("ozone")),
                ))

            cursor.executemany(insert_hist, rows)
            conn.commit()
            total_hist += len(rows)
            print(f"  {station_name}: {len(rows)} daily rows")

        except Exception as e:
            print(f"  ERROR — {file}: {e}")

    print(f"\nJOB 2 COMPLETE — {total_hist} historical rows loaded\n")

else:
    print(f"  Already loaded ({hist_count} rows) — skipping\n")

## final 
cursor.execute("SELECT COUNT(*) FROM aqi_live")
live_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM aqi_historical")
hist_total = cursor.fetchone()[0]

cursor.execute("SELECT MIN(fetched_date), MAX(fetched_date) FROM aqi_live")
live_range = cursor.fetchone()

cursor.execute("SELECT MIN(date), MAX(date) FROM aqi_historical")
hist_range = cursor.fetchone()


print("COMPLETE")
print(f"  aqi_live       : {live_total} rows | {live_range[0]} to {live_range[1]}")
print(f"  aqi_historical : {hist_total} rows | {hist_range[0]} to {hist_range[1]}")
print(f"  Live CSVs      : {LIVE_FOLDER}")
print("════════════════════════════════════════")

cursor.close()
conn.close()
