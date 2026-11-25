#!/usr/bin/env python3
"""Builds macro.csv for the ghana-bank-models goal. Standard library only.

Run:  python build_macro.py      (writes macro.csv next to this file)

Every number is one of:
  reported   copied from a cited source (source_id, see SOURCES.md)
  derived    computed here from reported numbers (formula in notes)
  estimated  an assumption by the owner (method in notes), forecasts only
  unavailable  not found in the sources read so far
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []


def add(scenario, year, driver, value, unit, source_id, status, notes=""):
    rows.append([scenario, year, driver, "" if value is None else value, unit, source_id, status, notes])


def mean(xs):
    return sum(xs) / len(xs)


# ------------------------------------------------------------------ history (reported)
# Policy rate, year-end. Source S-BOG-MPR (policy rate trends); 2024 and 2025 cross-checked in S-BOG-SUM-JAN26 / S-BOG-SUM-NOV26.
for y, v in [(2021, 14.5), (2022, 27.0), (2023, 30.0), (2024, 27.0), (2025, 18.0)]:
    note = "Last MPC decision effective in the year."
    if y == 2025:
        note += " The BoG trend table shows a mistyped effective date for the Nov 2025 row; the Dec-2025 value of 18.00 is confirmed in S-BOG-SUM-NOV26."
    add("actual", y, "policy_rate_pct", v, "percent", "S-BOG-MPR", "reported", note)

# FX end-period, BoG interbank (GHS per USD), December values. Source S-BOG-FX.
for y, v in [(2021, 6.01), (2022, 8.58), (2023, 11.88), (2024, 14.70), (2025, 10.45)]:
    add("actual", y, "ghs_per_usd_end", v, "GHS per USD", "S-BOG-FX", "reported", "December end-period interbank rate.")

# FX average: only 2021 and 2022 monthly averages were retrieved.
m2021 = [5.76, 5.76, 5.73, 5.73, 5.73, 5.75, 5.78, 5.83, 5.86, 5.88, 5.91, 5.95]
m2022 = [6.01, 6.31, 7.05, 7.11, 7.13, 7.19, 7.39, 8.06, 8.75, 11.17, 13.07, 10.03]
add("actual", 2021, "ghs_per_usd_avg", round(mean(m2021), 3), "GHS per USD", "S-BOG-FX", "derived", "Simple mean of the 12 BoG monthly average rates for 2021.")
add("actual", 2022, "ghs_per_usd_avg", round(mean(m2022), 3), "GHS per USD", "S-BOG-FX", "derived", "Simple mean of the 12 BoG monthly average rates for 2022.")
for y in (2023, 2024, 2025):
    add("actual", y, "ghs_per_usd_avg", None, "GHS per USD", "S-BOG-FX", "unavailable", "Monthly average rows for this year were not in the page extract. Follow-up: read the BoG exchange-rate table filtered to this year.")

# GDP growth (annual, real), S-BOG-SUM-NOV26 notes (GSS, revised 18 Mar 2026).
for y, v in [(2023, 3.1), (2024, 5.7), (2025, 6.0)]:
    add("actual", y, "gdp_growth_pct", v, "percent", "S-BOG-SUM-NOV26", "reported", "Overall real GDP growth, GSS series revised 18 Mar 2026.")
for y in (2021, 2022):
    add("actual", y, "gdp_growth_pct", None, "percent", "", "unavailable", "Not in sources read. Follow-up: Ghana Statistical Service national accounts.")

# Inflation year-end (Dec, y/y). Only Dec 2025 retrieved.
add("actual", 2025, "inflation_cpi_pct", 5.4, "percent", "S-BOG-SUM-NOV26", "reported", "December 2025 year-on-year, GSS chain-linked series (base 2021=100).")
for y in (2021, 2022, 2023, 2024):
    add("actual", y, "inflation_cpi_pct", None, "percent", "", "unavailable", "Not in sources read (the new chain-linked series starts at base 2021). Follow-up: GSS CPI release for December of this year.")

# T-bill rates, 2025 monthly (interest equivalent), from S-BOG-SUM-JAN26 (Jan-Sep) and S-BOG-SUM-NOV26 (Oct-Dec, matches).
t91_2025 = [28.37, 26.93, 17.15, 15.47, 15.11, 14.74, 13.44, 10.26, 10.45, 10.63, 10.98, 11.08]
t364_2025 = [30.26, 28.90, 19.85, 18.62, 16.64, 15.76, 14.84, 13.11, 12.94, 12.90, 13.03, 12.92]
add("actual", 2025, "tbill_91d_pct", round(mean(t91_2025), 2), "percent", "S-BOG-SUM-JAN26", "derived", "Simple mean of 12 monthly 91-day interest-equivalent rates, Jan-Dec 2025. Intra-year change was very large (28.4 to 11.1), so the average hides the path.")
add("actual", 2025, "tbill_364d_pct", round(mean(t364_2025), 2), "percent", "S-BOG-SUM-JAN26", "derived", "Simple mean of 12 monthly 364-day interest-equivalent rates, Jan-Dec 2025.")
for y in (2021, 2022, 2023, 2024):
    for d in ("tbill_91d_pct", "tbill_364d_pct"):
        add("actual", y, d, None, "percent", "", "unavailable", "Not in sources read. Follow-up: BoG monthly time series (Monthly Average 91/364-Day T-bill) for this year.")

# 10-year post-DDEP secondary-market yield (S-BOG-SUM-NOV26 table 3b), Dec 2025 value only.
add("actual", 2025, "govt_bond_yield_pct", None, "percent", "S-BOG-SUM-NOV26", "unavailable", "Only Oct-Dec 2025 monthly values exist in the source (10-year post-DDEP: 15.44, 15.40, 15.80), so no full-year average. Series used: 10-year post-DDEP secondary-market yield.")

# ------------------------------------------------------------------ 2026 year-to-date actuals (Jan-Oct)
t91_ytd = [11.17, 8.96, 4.89, 4.90, 4.91, 5.27, 5.85, 5.38, 4.72, 4.62]
t364_ytd = [12.97, 11.53, 9.57, 10.02, 10.27, 11.29, 13.45, 12.16, 12.16, 9.74]
b10_ytd = [15.86, 12.62, 11.86, 12.49, 12.49, 14.33, 15.00, 14.70, 14.22, 15.01]
fx_avg_ytd = [10.79, 10.92, 10.87, 11.07, 11.45, 11.41, 11.54, 11.33, 11.50, 11.69]
# Latest auctions (23 Nov 2026): 91d 4.5193, 364d 9.4470 (S-BOG-TB). Nov-Dec assumed at these levels.
t91_2026 = (sum(t91_ytd) + 2 * 4.52) / 12
t364_2026 = (sum(t364_ytd) + 2 * 9.45) / 12
b10_2026 = (sum(b10_ytd) + 2 * 15.01) / 12
fx_avg_2026 = (sum(fx_avg_ytd) + 2 * 11.85) / 12

# ------------------------------------------------------------------ forecasts
YEARS = [2026, 2027, 2028, 2029, 2030]
SC = {
    # policy rate: year-end. 2026 = 11.0 already decided on 18 Nov 2026 (reported), next MPC 18-20 Jan 2027.
    "policy_rate_pct": {
        "base":     [11.0, 10.0, 9.5, 9.0, 9.0],
        "downside": [11.0, 14.0, 14.0, 12.0, 11.0],
        "upside":   [11.0, 9.0, 8.5, 8.5, 8.5],
    },
    "tbill_91d_pct": {
        "base":     [round(t91_2026, 2), 5.5, 6.5, 7.5, 8.0],
        "downside": [round(t91_2026, 2), 9.0, 11.0, 10.0, 9.5],
        "upside":   [round(t91_2026, 2), 4.5, 5.0, 6.0, 6.5],
    },
    "tbill_364d_pct": {
        "base":     [round(t364_2026, 2), 9.5, 9.5, 9.0, 9.0],
        "downside": [round(t364_2026, 2), 13.0, 14.0, 12.0, 11.0],
        "upside":   [round(t364_2026, 2), 8.5, 8.0, 8.0, 8.0],
    },
    "govt_bond_yield_pct": {
        "base":     [round(b10_2026, 2), 14.0, 13.0, 12.5, 12.0],
        "downside": [round(b10_2026, 2), 17.0, 17.0, 15.5, 14.5],
        "upside":   [round(b10_2026, 2), 12.5, 11.5, 11.0, 10.5],
    },
    # inflation: year-end y/y. Oct 2026 = 5.5 (reported). BoG expects a gradual return to its 8 percent (+/-2) target band.
    "inflation_cpi_pct": {
        "base":     [6.0, 7.5, 8.0, 8.0, 8.0],
        "downside": [7.0, 11.0, 10.5, 10.0, 9.5],
        "upside":   [5.5, 6.0, 7.0, 7.5, 8.0],
    },
    # FX end-period GHS per USD. 2026E anchor: BoG daily weighted median about 11.85 in Nov 2026.
    "ghs_per_usd_end": {
        "base":     [11.9, 12.9, 13.9, 14.8, 15.7],
        "downside": [12.2, 14.2, 16.0, 17.6, 19.0],
        "upside":   [11.8, 12.4, 12.9, 13.4, 13.9],
    },
    "gdp_growth_pct": {
        "base":     [6.0, 5.0, 5.0, 4.8, 4.8],
        "downside": [5.8, 3.0, 3.5, 4.0, 4.0],
        "upside":   [6.2, 6.0, 5.8, 5.5, 5.5],
    },
}
NOTES = {
    "policy_rate_pct": "2026E is reported: cut from 14 to 11 on 18 Nov 2026 (S-BOG-MPC-NOV26). 2027-2030 are estimates: path set toward an inflation target of 8 +/- 2 percent; downside assumes a tightening response to a cedi or oil shock; upside assumes faster easing.",
    "tbill_91d_pct": "2026E = (Jan-Oct actual monthly mean x 10 + 2 x 4.52) / 12, Nov-Dec assumed at the latest 91-day auction (4.52 on 23 Nov 2026). 2027+ are estimates: market rates sit far below the policy rate, so they are assumed to converge upward gradually (base) or sharply (downside).",
    "tbill_364d_pct": "2026E = (Jan-Oct actual monthly mean x 10 + 2 x 9.45) / 12, Nov-Dec at the latest 364-day auction (9.447 on 23 Nov 2026). 2027+ are estimates.",
    "govt_bond_yield_pct": "Series: 10-year post-DDEP secondary-market yield. 2026E = (Jan-Oct monthly mean x 10 + 2 x 15.01) / 12 (Oct 2026 level held for Nov-Dec). 2027+ are estimates.",
    "inflation_cpi_pct": "Year-end y/y. Oct 2026 reported at 5.5 percent; 2026E assumes a modest rise by December. BoG forecasts a gradual return into the target band over the medium term. 2027+ are estimates.",
    "ghs_per_usd_end": "2026E anchored on the BoG daily interbank weighted median of about 11.85 in Nov 2026 (S-BOG-FX). 2027+ are estimates of depreciation: base about 8 percent a year falling to about 6; downside much faster; upside about 4 percent.",
    "gdp_growth_pct": "Q1 2026 6.4 and Q2 2026 6.0 reported (S-BOG-SUM-NOV26). 2026E to 2030E are estimates.",
}
for driver, by_sc in SC.items():
    for sc, vals in by_sc.items():
        for y, v in zip(YEARS, vals):
            note = NOTES[driver]
            add(sc, f"FY{y}E", driver, v, "percent" if "ghs" not in driver else "GHS per USD", "OWNER-ESTIMATE", "estimated", note)

# Derived forecast FX average = mean of opening and closing year-end rate, except 2026E (YTD actual + Nov/Dec assumption).
for sc, ends in SC["ghs_per_usd_end"].items():
    prev = 10.45
    for y, e in zip(YEARS, ends):
        if y == 2026:
            val = round(fx_avg_2026, 3)
            note = "2026E = (Jan-Oct actual monthly average x 10 + 2 x 11.85) / 12."
        else:
            val = round((prev + e) / 2, 3)
            note = "Simple average of opening and closing year-end rates (approximation)."
        add(sc, f"FY{y}E", "ghs_per_usd_avg", val, "GHS per USD", "OWNER-ESTIMATE", "estimated", note)
        prev = e

# ------------------------------------------------------------------ regulatory (same in all scenarios)
# FY2026E rows describe rules in force in Nov 2026 (reported). FY2027E onward are carry-forwards of the current rule (estimated),
# not reported future facts (review by gemini and codex, 2026-11-25).
CRR_NOTE = ("Uniform cash reserve ratio of 20 percent in domestic currency, effective 4 Jun 2026, replacing the earlier dynamic CRR (S-BOG-MPC-MAY26). "
            "BoG published a Liquidity Coverage Ratio exposure draft on 9 Oct 2026 that could change liquidity rules (not read).")
CAR_NOTE = ("Regulatory minimum capital adequacy ratio of 13.0 percent, quoted in the BoG Monetary Policy Report September 2026 (solvency section): industry CAR 19.1 percent in Aug 2026 'well above the regulatory minimum requirement of 13.0 percent' (S-BOG-MPR-SEP26, read by claude). "
            "Earlier history: a temporary lower 10 percent threshold under DDEP forbearance applied in 2024 and expired by Dec 2025 (per gemini's review citing CalBank AR 2024 p.120 and codex's reading of GCB FY2025; not verified by claude).")
CAP_NOTE = ("Minimum paid-up capital of GHS 400 million required by 31 Dec 2018 (BoG Notice BG/GOV/SEC/2017/19, S-BOG-CAP17). A search on 2026-11-25 found NO newer minimum for universal banks "
            "(2026 capital reforms found apply to microfinance and community banks only), but this is not proof. Treat as an unconfirmed carry-forward until a reviewer confirms with the BoG.")
for sc in ("base", "downside", "upside"):
    for y in YEARS:
        now = (y == 2026)
        st = "reported" if now else "estimated"
        tail = "" if now else " FY2027E onward is a carry-forward estimate: the current rule is held flat."
        add(sc, f"FY{y}E", "crr_pct", 20.0, "percent", "S-BOG-MPC-MAY26", st, CRR_NOTE + tail)
        add(sc, f"FY{y}E", "min_car_pct", 13.0, "percent", "S-BOG-MPR-SEP26", st, CAR_NOTE + tail)
        add(sc, f"FY{y}E", "min_capital_ghs_m", 400.0, "GHS millions", "S-BOG-CAP17", "estimated", CAP_NOTE)
add("actual", 2024, "crr_pct", None, "percent", "", "unavailable", "A dynamic CRR applied before 4 Jun 2026 (tiers by loan-to-deposit ratio, per a Fitch note). The tier table was not read in full. Follow-up if a bank's history needs it.")
add("actual", 2025, "crr_pct", None, "percent", "", "unavailable", "Dynamic CRR regime; exact rate by bank depended on its loan-to-deposit ratio.")

with open(os.path.join(HERE, "macro.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["scenario", "year", "driver", "value", "unit", "source_id", "status", "notes"])
    w.writerows(rows)
print("wrote macro.csv:", len(rows), "rows")
for k, v in [("t91_2026", t91_2026), ("t364_2026", t364_2026), ("b10_2026", b10_2026), ("fx_avg_2026", fx_avg_2026)]:
    print(k, round(v, 3))
