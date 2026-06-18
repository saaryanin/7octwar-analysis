# Oct 7 War — Casualty Statistics
> Data source: [oct7database.com](https://oct7database.com)
> Last updated: <!-- add date -->
> Queries: `sql/02_statistics_queries.sql`

---

## 1. Overall Totals

### 1a. Grand Total
|total_records|total_soldiers|total_civilians|soldier_pct|
|-------------|--------------|---------------|-----------|
|2198|896|1302|40.8|

### 1b. Status Breakdown
|status_simple|total|soldiers|civilians|pct_of_total|
|-------------|-----|--------|---------|------------|
|Killed|1947|872|1075|88.6|
|Released / Rescued|165|9|156|7.5|
|Kidnapped and Killed|85|15|70|3.9|
|Released then Died|1|0|1|0.0|

### 1c. Soldiers — Confirmed Deaths
| soldiers_killed |
|----------------|
|887|

**Findings:**
- Of 2,198 total casualties, **896 (40.8%) were soldiers** and 1,302 (59.2%) were civilians.
- **887 soldiers died** (872 killed + 15 kidnapped and killed); the remaining 9 soldiers were released or rescued and survived.
- The vast majority of deaths were classified as "Killed" (88.6%). Civilians outnumbered soldiers among the killed (1,075 vs 872), but soldiers made up nearly all the smaller categories proportionally.

---

## 2. Deaths by Front

### 2a. Full Breakdown per Front
|front|total_casualties|soldiers|civilians|avg_soldier_age|youngest_soldier|oldest_soldier|
|-----|----------------|--------|---------|---------------|----------------|--------------|
|Gaza|1885|755|1130|24.0|18.0|53.0|
|North|165|113|52|27.1|18.0|53.0|
|West Bank|43|18|25|27.9|20.0|55.0|
|Home|36|4|32|30.3|19.0|51.0|
|Jordan|5|2|3|44.0|20.0|68.0|
|Iraq|2|2|0|19.0|19.0|19.0|
|Accident|2|2|0|38.5|34.0|43.0|
|Yemen|1|0|1||||
|Other|6|0|6||||
|Iran|53|0|53||||


### 2b. Soldiers Killed per Front
|front|soldiers_killed|
|-----|---------------|
|Gaza|746|
|North|113|
|West Bank|18|
|Home|4|
|Jordan|2|
|Iraq|2|
|Accident|2|


**Findings:**
- **Gaza was by far the deadliest front: 746 soldiers killed (84% of the 887 confirmed soldier deaths)**, with the youngest average age (24.0).
- The **North (Lebanon) front** is second with 113 killed, at an older average age (27.1) — consistent with heavier reservist involvement.
- Soldier deaths fall off sharply after the two main fronts: West Bank (18), Home (4), and a handful elsewhere.
- The **Iran front (53 casualties) and Yemen/Other were entirely civilian** — these reflect long-range missile/drone strikes on the home front rather than ground combat.
- *Data note:* "Accident" appears as a *front* for 2 records — likely a mislabel that belongs under cause of death.

---

## 3. Monthly Timeline

### 3a. Monthly death toll across all fronts (Soldiers)
|death_year_month|soldiers_killed|
|----------------|---------------|
|2023-10|283|
|2023-11|63|
|2023-12|108|
|2024-01|53|
|2024-02|20|
|2024-03|16|
|2024-04|9|
|2024-05|36|
|2024-06|25|
|2024-07|17|
|2024-08|16|
|2024-09|9|
|2024-10|62|
|2024-11|30|
|2024-12|17|
|2025-01|17|
|2025-02|4|
|2025-04|3|
|2025-05|8|
|2025-06|20|
|2025-07|18|
|2025-08|2|
|2025-09|13|
|2025-10|5|
|2026-01|1|
|2026-02|1|
|2026-03|10|
|2026-04|7|
|2026-05|8|
|2026-06|6|


### 3b. Top 10 Deadliest Months (Soldiers)
|death_year_month|soldiers_killed|
|----------------|---------------|
|2023-10|283|
|2023-12|108|
|2023-11|63|
|2024-10|62|
|2024-01|53|
|2024-05|36|
|2024-11|30|
|2024-06|25|
|2025-06|20|
|2024-02|20|


**Findings:**
- **Peak month: October 2023 with 283 soldiers killed** — the Oct 7 attack itself plus the opening days of the war. This single month accounts for ~32% of all soldier deaths.
- Second peak: **December 2023 (108)**, reflecting the intensive Gaza ground maneuver.
- A clear secondary spike in **October 2024 (62)** corresponds to the ground operation into southern Lebanon.
- **Notable pattern:** deaths follow distinct operational waves rather than a steady rate — large spikes during ground offensives (Oct–Dec 2023, Oct 2024) separated by lower-intensity months. A smaller bump in **June 2025 (20)** aligns with the Iran conflict period.
- The long tail through 2025–2026 shows continued but much lower-level casualties.

---

## 4. Age Distribution of Soldiers

### 4a. Summary Stats
|youngest|oldest|avg_age|soldiers_with_known_age|soldiers_unknown_age|
|--------|------|-------|-----------------------|--------------------|
|18.0|68.0|24.6|896|0|


### 4b. Age Buckets
|age_group|count|pct|
|---------|-----|---|
|Under 20|135|15.1|
|20-24|484|54.0|
|25-29|97|10.8|
|30-34|77|8.6|
|35-39|55|6.1|
|40+|48|5.4|


### 4c. 10 Youngest Soldiers Killed
|first_name|last_name|age|front|death_date|cause_of_death|
|----------|---------|---|-----|----------|--------------|
|Neriya|Nagari|18.0|Gaza|2023-10-07||
|Ofir|Davidiyan|18.0|Gaza|2023-10-07||
|Shirat-Yam|Amar|18.0|Gaza|2023-10-07||
|Hadar|Cohen|18.0|Gaza|2023-10-07||
|Ilay|Azar|18.0|Gaza|2023-10-07||
|Kamay|Achiel|18.0|North|2023-10-14|Accident|
|Michael|Ruzal|18.0|Gaza|2024-05-05|Mortar|
|Ariel|Ohana|19.0|Gaza|2023-10-08||
|Nik|Beizer|19.0|Gaza|2023-11-10|Idf Shelling|
|Ron|Sherman|19.0|Gaza|2023-11-10|Idf Shelling|


**Findings:**
- **Most common age group: 20–24, which alone accounts for 484 soldiers (54%).**
- The force that died was strikingly young: **about 69% were under 25** (Under 20: 15.1% + 20–24: 54.0%), and the **average age was just 24.6**.
- The youngest were **18** (the minimum conscription/service age) and the oldest was **68** — the full span reflects both young conscripts and older reservists.
- Age data is complete: **all 896 soldiers have a known age** (0 missing).
- Older soldiers (40+) make up only 5.4%, consistent with most reservists being called up in their 20s–30s.

---

## 5. Cause of Death (Soldiers)

### 5a. Top Causes Overall
|cause_of_death|count|pct|
|--------------|-----|---|
|Explosive|157|25.0|
|Anti-Tank|154|24.5|
|Gunfire|120|19.1|
|Accident|54|8.6|
|Sniper|36|5.7|
|Friendly Fire|31|4.9|
|Mortar|21|3.3|
|Drone|16|2.5|
|Rocket|12|1.9|
|רחפן נפץ|11|1.7|
|Shooting Attack|5|0.8|
|Ramming Attack|4|0.6|
|Idf Shelling|3|0.5|
|Grenade Malfunction|1|0.2|
|Interceptor|1|0.2|


**Findings:**
- **Combat weapons dominate: Explosive (25.0%), Anti-Tank (24.5%), and Gunfire (19.1%) together cause ~69% of soldier deaths** — the signature of close-quarters urban/ground fighting.
- **Non-combat and fratricide losses are significant:** Accident (8.6%), Friendly Fire (4.9%), and IDF Shelling (0.5%) together account for ~14% of deaths, underscoring the dangers of dense, fast-moving operations.
- Anti-tank fire being nearly as deadly as general explosives points to heavy use of guided missiles/RPGs against armor and buildings.
- *Data note:* `רחפן נפץ` (Hebrew for "explosive drone", 11 deaths, 1.7%) should be merged with the English **Drone** category — a cleanup item for the Tableau views. Counts here are limited to soldiers with a recorded cause (627 of 887).

---

## 6. Residence — Where Did Soldiers Come From?

### 6a. Top 20 Cities / Towns
|residence|soldiers|pct|
|---------|--------|---|
|Jerusalem|73|8.1|
|Modi’In Makabim Re’Ut|24|2.7|
|Tel Aviv-Yafo|23|2.6|
|Petah Tikva|22|2.5|
|Haifa|20|2.2|
|Rehovot|19|2.1|
|Ramat Gan|16|1.8|
|Ashdod|15|1.7|
|Be’Er Sheva|14|1.6|
|Ra’Anana|14|1.6|
|Ashkelon|13|1.5|
|Rosh Haayin|13|1.5|
|Beit Shemesh|12|1.3|
|Rishon Lezion|12|1.3|
|Dimona|10|1.1|
|Netanya|10|1.1|
|Eli|9|1.0|
|Hadera|9|1.0|
|Herzliya|9|1.0|
|Holon|9|1.0|


### 6b. Foreign Nationals
| country | soldiers |
|---------|----------|
| (no rows returned) | |

**Findings:**
- **Jerusalem leads by a wide margin with 73 soldiers (8.1%)** — far ahead of any other locality, reflecting both its large population and its religious-Zionist communities with high combat-unit enlistment.
- After Jerusalem the distribution is long-tailed: the next towns (Modi'in, Tel Aviv, Petah Tikva, Haifa) each contribute only 2–3%, and no single city dominates.
- Casualties are spread across the whole country — major cities, periphery towns (Dimona, Be'er Sheva), and settlements (Eli) all appear — showing the war's human cost reached nearly every type of community.
- **The foreign-nationals query returned no rows**, meaning every soldier in the dataset has country = Israel (or blank). Country is not a useful breakdown dimension for soldiers; residence/city is the better geographic field for Tableau.

---

## 7. Gender Breakdown

### Overall
|gender|total|soldiers|civilians|
|------|-----|--------|---------|
|Female|482|44|438|
|Male|1716|852|864|


### Female Soldiers Detail
|first_name|last_name|age|front|role|status_simple|cause_of_death|
|----------|---------|---|-----|----|-------------|--------------|
|Ofir|Davidiyan|18.0|Gaza|Soldier|Killed||
|Liri|Albag|18.0|Gaza|Soldier|Released / Rescued||
|Shirat-Yam|Amar|18.0|Gaza|Soldier|Killed||
|Hadar|Cohen|18.0|Gaza|Soldier|Killed||
|Shir|Biton|19.0|Gaza|Soldier|Killed||
|Lior|Levy|19.0|Gaza|Soldier|Killed||
|Daniella|Gilboa|19.0|Gaza|Soldier|Released / Rescued||
|Noam|Abramovich|19.0|Gaza|Soldier|Killed||
|Karina|Ariev|19.0|Gaza|Soldier|Released / Rescued||
|Shai|Ashram|19.0|Gaza|Soldier|Killed||
|Agam|Berger|19.0|Gaza|Soldier|Released / Rescued||
|Adi|Groman|19.0|Gaza|Soldier|Killed||
|Noa|Marciano|19.0|Gaza|Soldier|Kidnapped and Killed||
|Shira|Shohat|19.0|Gaza|Soldier|Killed||
|Danit|Cohen|19.0|Gaza|Soldier|Killed||
|Eden|Alon-Levy|19.0|Gaza|Soldier|Killed||
|Naama|Boni|19.0|Gaza|Soldier|Killed||
|Shir|Shlomo|19.0|Gaza|Soldier|Killed||
|Roni|Eshel|19.0|Gaza|Soldier|Killed||
|Naama|Levy|19.0|Gaza|Soldier|Released / Rescued||
|Osher|Barzilay|19.0|Gaza|Soldier|Killed||
|Ori|Megidish|19.0|Gaza|Soldier|Released / Rescued||
|Adi|Landman|19.0|Gaza|Soldier|Killed||
|Shirel|Mor|19.0|Gaza|Soldier|Killed||
|Aviv|Hajaj|19.0|Gaza|Soldier|Killed||
|Mia|Viallovo Polo|19.0|Gaza|Soldier|Killed||
|Yarin|Peled|20.0|Gaza|Soldier|Killed||
|Sivan|Asraf|20.0|Gaza|Soldier|Killed||
|Yael|Leibushor|20.0|Gaza|Soldier|Killed||
|Shahaf|Nesani|20.0|Gaza|Soldier|Killed||
|Noa|Prais|20.0|Gaza|Soldier|Killed||
|Adar|Ben-Simon|20.0|Gaza|Soldier|Killed||
|Shirel|Haim Pour|20.0|Gaza|Soldier|Killed||
|Yam|Glass|20.0|Gaza|Soldier|Killed||
|Shir|Eilat|20.0|Gaza|Soldier|Killed||
|Agam|Naim|20.0|Gaza|Soldier|Killed|Explosive|
|Sahar|Saudian|21.0|Gaza|Soldier|Killed||
|Or|Moses|22.0|Gaza|Soldier|Killed||
|Eden|Nimri|22.0|Gaza|Soldier|Killed||
|Adi|Borech|22.0|Gaza|Soldier|Killed|Rocket|
|Alina|Pravosudova|23.0|Gaza|Soldier|Killed||
|Kamay|Achiel|18.0|North|Soldier|Killed|Accident|
|Omer|Benjo|20.0|North|Soldier|Killed|Rocket|
|Rotem|Yanai|20.0|North|Soldier|Killed|רחפן נפץ|

**Findings:**
- **Of 896 soldier casualties, 44 (4.9%) were women.** Among civilians the split is far more even (438 female / 864 male), so the soldier population skews heavily male as expected.
- **The female soldiers were overwhelmingly young** — almost all 18–20, with a concentration at age 19, reflecting conscript-age service.
- **Almost all are from the Gaza front**, and several of the highest-profile cases appear here: the Nahal Oz field-observers (*tatzpitaniyot*) who were either killed or kidnapped on Oct 7. Notably, **7 of the female soldiers were "Released / Rescued"** (e.g. Liri Albag, Agam Berger, Naama Levy, Ori Megidish, Daniella Gilboa, Karina Ariev) and survived, and Noa Marciano was "Kidnapped and Killed."
- Cause of death is recorded for very few female soldiers, so cause-level analysis isn't reliable for this subgroup.

---

## 8. Role Breakdown

| role | count | avg_age |
|---|---|---|
| Soldier | 896 | 24.6 |

**Findings:**
- **Not a useful breakdown:** the `role` field collapses to a single value ("Soldier") for the entire soldiers view, so it returns just one row (896, avg age 24.6). It cannot distinguish rank, unit, or specialization.
- If finer role analysis is wanted later, it would require richer source data (e.g. rank/unit fields) that this dataset doesn't contain. Skip this dimension for Tableau.

---

## Key Takeaways

1. **A young, ground-combat toll concentrated in Gaza.** Of 896 soldier casualties, **887 died**, **84% on the Gaza front**, and roughly **69% were under 25** (average age 24.6). The data describes an overwhelmingly young force lost primarily in urban ground fighting.

2. **The war came in operational waves, not a steady stream.** Soldier deaths spike sharply during ground offensives — **October 2023 (283, ~32% of all deaths)** and December 2023 (108) in Gaza, then October 2024 (62) in Lebanon — separated by lower-intensity months. Timeline visualizations should emphasize these waves.

3. **Combat weapons dominate, but fratricide and accidents are non-trivial.** Explosives, anti-tank fire, and gunfire cause ~69% of deaths, while **accidents (8.6%) and friendly fire (4.9%) together exceed 13%** — a meaningful, often under-discussed share.

4. **A second front and a home front are visible in the data.** The North (Lebanon) is a clear secondary theater (113 soldiers, older average age), while the Iran/Yemen fronts produced **only civilian casualties** from long-range strikes — soldier vs. civilian patterns differ sharply by front.

5. **Women were few but prominent.** Just 4.9% of soldier casualties were women, nearly all aged 18–20 on the Gaza front — including the Nahal Oz observers, several of whom were later released or rescued.

---

## Data Quality Notes (carry into Tableau views)
- Merge `רחפן נפץ` (Hebrew "explosive drone", 11 records) into the **Drone** cause category.
- "Accident" appears as both a **front** and a **cause of death** — the 2 "Accident" front records should likely be reassigned.
- `country` is effectively constant (Israel) for soldiers — use **residence** for geographic mapping, not country.
- `role` collapses to a single value for soldiers — drop it as an analysis dimension.
- Cause of death is recorded for only ~627 of 887 fallen soldiers; cause-based charts should note the missing share or filter explicitly.
