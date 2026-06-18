"""
Builds and maintains the city_region_lookup table in the SQLite DB.

Run order:
  1. python src/create_sqlite_db.py
  2. python src/geocode_regions.py   ← this script
  3. (re)create views in DBeaver
  4. python src/export_tableau_csvs.py

Safe to re-run: already-classified cities are skipped.
When new casualties are added to the dataset, re-running this script
geocodes any new city names and adds them to the lookup automatically.
"""

import sqlite3
import time
import requests
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "oct7_analysis.db"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "oct7-casualty-analysis/1.0 (yaninsahar@gmail.com)"

# All cities already classified manually (ASCII apostrophe throughout).
# These are seeded instantly — no API calls needed for them.
MANUAL: dict[str, list[str]] = {
    "North": [
        "Haifa", "Nesher", "Kiryat Ata", "Kiryat Bialik", "Kiryat Motzkin",
        "Kiryat Yam", "Dalyat Al-Karmel", "Yagur", "Ramat Yohanan", "Ramat David",
        "Ramat Yishai", "Kiryat Tiv'On", "Rekhassim", "Atlit", "Avtin", "Eshar",
        "Giv'At Ela", "Neve Ziv", "Zikron Ya'Akov", "Binyamina",
        "Binyamina-Giv'At Ada", "Or Akiva", "Caesarea", "Pardes Hanna-Karkur",
        "Pardes Hanna", "Shimshit", "Shameret",
        "Karmi'El", "Nof Hagalil", "Afula", "Migdal Haemek", "Yokne'Am Illit",
        "Moreshet", "Kfar Tavor", "Kfar Baruch", "Beit Keshet", "Shadmot Devora",
        "Dovrat", "Lavi", "Lotem", "Rakefet", "Genigar", "Mitzpe Netofa",
        "Har Halutz", "Shorashim", "Adi", "Hoshaya", "Sde Ilan", "יישוב היוגב", "Ramat Naftali",
        "Yiftah", "Kfar Shamai", "Moledet", "Masad",
        "Acre", "Nahariyya", "Shlomi", "Ma'Alot Tarshiha", "Gesher Haziv",
        "Shavei Tzion", "Kabri", "Amka", "Kfar Yasif", "Hurfeish", "Ein Hamifratz",
        "Peki'In", "Beit Jann", "Yanuh-Jat", "Sajur", "Kafr Kanna", "Kfar Kanna",
        "Maghar", "Zarzir", "Kamun", "Tuba-Zangariyye",
        "Tiberias", "Poriya Illit", "Beit She'An", "Afikim", "Ein Hanatziv",
        "Sde Nehemia", "Sde Ya'Akov", "Yesud Hama'Ala", "Mesilot", "Hamadia",
        "Yardena", "Sde Eliyahu", "Shadmot Mehola",
        "Safed", "Kiryat Shmona", "Kfar Gil'Adi", "Ramot Naftali",
        "Ayelet Hashahar", "Rosh Pinna",
        "Katzrin", "Merom Golan", "Majdal Shams", "Nov", "Afik", "Odem",
        "Avnei Eitan", "Haspin", "Keidar",
    ],
    "Central": [
        "Hadera", "Elyakhin", "Harish", "Katzir", "Bat Hefer",
        "Giv'At Haim Ihud", "Giv'At Haim Me'Uhad", "Mishmarot",
        "Netanya", "Even Yehuda", "Kadima-Zoran", "Tel Mond", "Kfar Yona",
        "Tzur Moshe", "Tzur Yitzhak", "Nir Eliyahu", "Nitzanei Oz",
        "Herut", "Gan Yoshiya", "Sde Warburg", "Beit Yitzhak-Sha'Ar Hefer",
        "Harsha", "Bahan",
        "Kfar Sava", "Ra'Anana", "Hod Hasharon", "Kokhav Ya'Ir",
        "Kokhav Ya'Ir Tzur Yig'Al", "Nirit", "Azri'El", "Sha'Arei Tikva",
        "Sitria", "Tzur Natan", "Ganei Am", "Tzofit", "Tzofim", "Einav",
        "Herzliya", "Ramat Hasharon", "Rishpon", "Shefayim",
        "Tel Aviv-Yafo", "Tel Aviv", "Ramat Gan", "Givatayim",
        "Or Yehuda", "Giv'At Shmuel", "Kiryat Ono", "Yehud-Monosson",
        "Petah Tikva", "Rosh Haayin", "Shoham", "Yarhiv", "Nehalim",
        "Ganei Tikva", "Bareket", "Kfar Azar", "Rinnatya", "Giv'At Shapira",
        "Hadid", "Neve Yarak",
        "Lod", "Kfar Chabad", "Ben Shemen", "Beit Nehemia", "Beit Dagan",
        "Tzafriya", "Kfar Shmuel", "Beit Arif", "Gan Haim", "Hogla",
        "Holon", "Bat Yam", "Rishon Lezion",
        "Rehovot", "Ness Ziona", "Kfar Aviv", "Beit Hanan", "Giv'At Brenner",
        "Yad Rambam",
        "Modi'In Makabim Re'Ut", "Modi'In", "Re'Ut", "Lapid",
        "Hashmona'Im", "Kfar Oranim", "Beit Hashmonai",
        "Jerusalem", "Mevaseret Zion", "Motza Illit", "Beit Shemesh",
        "Tzur Hadassa", "Bar Giora", "Nes Harim", "Ora", "Srigim",
        "Har'El", "Tsor'A", "Kfar Hashmonai",
    ],
    "South": [
        "Ashdod", "Ashkelon", "Nitzan", "Mabu'Im",
        "Kiryat Gat", "Kiryat Malakhi", "Gedera", "Yavne",
        "Mazkeret Batya", "Kfar Menahem", "Ein Tzurim", "Revadim",
        "Masu'Ot Itzhak", "Merkaz Shapira", "Ganot Hadar", "Aderet",
        "Beit Gamli'El", "Ganei Tal", "Shomeriya", "Eitan", "Even Shmuel",
        "Ge'A", "Nir Banim", "Kidron", "Arugot", "Ezer", "Benei Adam",
        "Kfar Harif", "Hafetz Haim", "Yakhini", "Yad Binyamin", "Karmit",
        "Giv'Ot Bar",
        "Sderot", "Ofakim", "Alumim", "Be'Eri", "Patish", "Nir Yitzhak",
        "Shani", "Yoshivya", "Ganot", "Peduyim", "Gilat", "Benei Dekalim",
        "Shlomit", "Ein Habesor",
        "Be'Er Sheva", "Omer", "Lehavim", "Meitar", "Rahat", "Hura",
        "Segev Shalom", "Abu Rubeiya", "Dimona", "Yeruham",
        "Midreshet Ben-Gurion", "Be'Er Milka", "Asael",
        "Ein Gedi", "Mitzpe Ramon", "Tzofer", "Idan", "Paran", "Eilat",
        "Tene", "Dekel",
    ],
    "West Bank": [
        "Ariel", "Kedumim", "Karnei Shomron", "Eli", "Shilo", "Ofra",
        "Beit El", "Yitzhar", "Itamar", "Rehelim", "Yakir", "Nili",
        "Bruchin", "Peduel", "Kiryat Netafim", "Shavei Shomron", "Hermesh",
        "Tal Menashe", "Alfei Menashe", "Oranit", "Kochav Ya'Akov",
        "Revava", "Sal'It", "Havot Yair", "Har Brakha", "Immanuel",
        "Geva Binyamin", "Neve Tzuf", "Talmon", "Dolev", "Psagot",
        "Tel Tzion", "Ma'Ale Michmash", "Beit Arie", "Mevo Horon",
        "Giv'At Ze'Ev", "Modi'In Illit", "Almon",
        "Efrat", "Elazar", "Alon Shvut", "Neve Daniel", "Kfar Etzion",
        "Karmei Tzur", "Migdal Oz", "Geva'Ot", "Nokdim",
        "Betar Illit", "Mevo Beitar",
        "Ma'Ale Adumim", "Almog", "Mitzpe Yeriho", "Mehola",
        "Kiryat Arba", "Hebron", "Otniel", "Susya", "Tene Omarim",
    ],
}


def normalize(text: str) -> str:
    """Match the REPLACE chain used in the SQL view."""
    return (
        text.replace("’", "'")   # U+2019 right single quotation mark
            .replace("‘", "'")   # U+2018 left single quotation mark
            .replace("׳", "'")   # U+05F3 Hebrew geresh
    )


def geocode(city: str) -> dict | None:
    params = {
        "q": city,
        "countrycodes": "il,ps",
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }
    try:
        r = requests.get(
            NOMINATIM_URL,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json()
        return results[0] if results else None
    except Exception as exc:
        print(f"    ⚠️  request failed: {exc}")
        return None


def classify(result: dict) -> tuple[str, float, float]:
    lat = float(result["lat"])
    lon = float(result["lon"])
    address = result.get("address", {})
    country_code = address.get("country_code", "")
    state = address.get("state", "")

    if country_code == "ps":
        region = "West Bank"
    elif "Jerusalem" in state:
        # Jerusalem District sits south of the lat threshold but belongs to Central
        region = "Central"
    elif lat > 32.45:
        region = "North"
    elif lat >= 31.96:
        region = "Central"
    else:
        region = "South"

    return region, lat, lon


def build_lookup() -> None:
    if not DB_PATH.exists():
        print(f"❌  Database not found at {DB_PATH}")
        print("    Run src/create_sqlite_db.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS city_region_lookup (
            city_normalized TEXT PRIMARY KEY,
            region          TEXT NOT NULL,
            lat             REAL,
            lon             REAL,
            source          TEXT NOT NULL DEFAULT 'manual'
        )
    """)
    conn.commit()

    # Seed manually classified cities (no API needed)
    seeded = 0
    for region, cities in MANUAL.items():
        for city in cities:
            cur.execute(
                "INSERT OR IGNORE INTO city_region_lookup (city_normalized, region, source) "
                "VALUES (?, ?, 'manual')",
                (city, region),
            )
            if cur.rowcount:
                seeded += 1
    conn.commit()
    print(f"✅  Seeded {seeded} manual entries")

    # Find residence values in the DB not yet in the lookup
    cur.execute("""
        SELECT DISTINCT
            REPLACE(REPLACE(REPLACE(residence, char(8217), char(39)),
                                                char(8216), char(39)),
                                                char(1523),  char(39)) AS res
        FROM idf_casualties
        WHERE is_soldier = TRUE
          AND status_simple IN (
              'Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died'
          )
          AND residence IS NOT NULL
          AND residence NOT IN ('Nan', 'Unknown')
    """)
    all_cities = {row[0] for row in cur.fetchall()}

    cur.execute("SELECT city_normalized FROM city_region_lookup")
    known = {row[0] for row in cur.fetchall()}

    to_geocode = sorted(all_cities - known)

    if not to_geocode:
        print("✅  No unknown cities — lookup is complete")
        conn.close()
        return

    print(f"\n🔍  Geocoding {len(to_geocode)} unknown cities via Nominatim...")
    print("    (1 request/sec to respect rate limits)\n")

    for i, city in enumerate(to_geocode, 1):
        print(f"  [{i}/{len(to_geocode)}] {city!r} ... ", end="", flush=True)
        result = geocode(city)
        if result:
            region, lat, lon = classify(result)
            cur.execute(
                "INSERT OR REPLACE INTO city_region_lookup "
                "  (city_normalized, region, lat, lon, source) "
                "VALUES (?, ?, ?, ?, 'geocoded')",
                (city, region, lat, lon),
            )
            conn.commit()
            print(f"→ {region}  ({lat:.4f}, {lon:.4f})")
        else:
            print("→ ⚠️  not found, skipping")

        time.sleep(1.1)  # Nominatim ToS: max 1 req/sec

    conn.close()

    print("\n✅  Done. Re-run this script any time new data is loaded.")
    print("    Then refresh the tableau_soldiers_by_region view in DBeaver.")


if __name__ == "__main__":
    build_lookup()
