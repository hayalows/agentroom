"""Independent Decimal verification of peer comparison against a pinned roll-up.
Run python -I verify_snapshot.py INPUT_CHECKOUT ROLLUP_OUTPUT_DIR PEER_OUTPUT_DIR.
Read-only; does not grant acceptance or independently adjudicate prior reviews.
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from decimal import Decimal as D
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def text_hash(p):
    return hashlib.sha256(p.read_bytes().decode("utf-8-sig").encode()).hexdigest()


def read_csv(p):
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        fields = reader.fieldnames
        require(fields and len(fields) == len(set(fields)), f"invalid header: {p}")
        rows = list(reader)
    require(all(None not in r and None not in r.values() for r in rows), f"row width: {p}")
    return rows


def index(rows, key):
    out = {}
    for r in rows:
        k = r[key]
        require(k not in out, f"duplicate {key}: {k}")
        out[k] = r
    return out


def val(r, historical):
    allowed = ("reported", "derived") if historical else ("estimated",)
    if r["status"] not in allowed or not r["value"].strip():
        return None
    n = D(r["value"])
    require(n.is_finite(), "nonfinite value")
    return n


def load_period(rows, period, scenario=None):
    selected = [r for r in rows if r["period"] == period and (scenario is None or r.get("scenario") == scenario)]
    return {k: val(r, scenario is None) for k, r in index(selected, "line_item").items()}


def ratio(a, b):
    return D(100) * a / b if a is not None and b is not None and b > 0 else None


def avg(a, b):
    return (a + b) / 2 if a is not None and b is not None else None


def capital(d):
    return d.get("car_pct") if d.get("car_pct") is not None else d.get("x_car_proxy_pct")


def package_hash(bank):
    names = ["README.md", "sources.md", "financials.csv", "assumptions.json", "forecast.csv", "checks.md"]
    code = next((n for n in ("model.py", "model.mjs", "model.js", "assumptions.md") if (bank/n).is_file() and (bank/n).stat().st_size), None)
    require(code is not None and all((bank/n).is_file() for n in names), f"incomplete package: {bank}")
    hashes = [[n, text_hash(bank/n)] for n in names + [code]]
    return hashlib.sha256(json.dumps(hashes, separators=(",", ":")).encode()).hexdigest()


def scope_marker(p):
    if not p.is_file():
        return None
    s = p.read_bytes().decode("utf-8")
    if not re.search(r"\bconditional\b", s, re.I):
        return None
    m = re.search(r"^Scope:\s*conditional\s*\(([^\r\n]+)\)\s*$", s, re.I | re.M)
    q = re.search(r'["“]conditional:\s*([^"”\r\n]+)["”]', s, re.I)
    gap = m.group(1) if m else q.group(1) if q else "source gap; see scope marker"
    return {"label": "conditional: " + gap.strip(), "sha256": digest(p)}


def verify(root, roll, peer):
    goal = root/"goals"/"ghana-bank-models"
    manifest = json.loads((roll/"manifest.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == 3, "use schema-3 scoped roll-up")
    source = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    require(source == manifest["sourceCommit"], "input must be exact pinned source commit")
    dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"], text=True)
    require(not dirty.strip(), "input checkout must be clean")
    accepted = index(manifest["acceptedEvidence"], "bank")
    excluded = index(manifest["exclusions"], "bank")
    roster = set(re.findall(r"^\|\s*([a-z0-9][a-z0-9-]*)\s*\|\s*.*?\s*\|$", (goal/"ROSTER.md").read_text(encoding="utf-8"), re.M)) - {"slug", "Slug"}
    require(not set(accepted) & set(excluded) and set(accepted) | set(excluded) == roster, "manifest roster mismatch")
    require((len(accepted), len(excluded), len(roster)) == (manifest["accepted"], manifest["excluded"], manifest["roster"]), "manifest counts mismatch")
    markers = {b: m for b in roster if (m := scope_marker(goal/"review-resolutions"/(b+".md"))) is not None}
    require(markers == manifest["conditionalMarkers"] and len(markers) == manifest["conditional"] and not set(markers) & set(accepted), "scope mismatch or ordinary contamination")
    ordinary = index(read_csv(peer/"comparison.csv"), "bank")
    conditional = index(read_csv(peer/"conditional-comparison.csv"), "bank")
    require(set(ordinary) == set(accepted), "ordinary peer membership mismatch")
    require(set(conditional) == set(markers), "conditional peer membership mismatch")
    macro = text_hash(goal/"sector"/"macro-assumptions"/"macro.csv")
    totals = {k: {} for k in ("total_assets", "customer_deposits", "profit_after_tax")}
    checks = 0

    def check(row, key, expected):
        nonlocal checks
        got = row[key]
        if expected is None:
            require(got == "", f"{row['bank']} {key}: expected blank, got {got}")
        elif isinstance(expected, D):
            tolerance = D(".000051") if key.endswith("_pct") else D(".000501")
            require(got != "" and D(got).is_finite() and abs(D(got)-expected) <= tolerance, f"{row['bank']} {key}: expected {expected}, got {got}")
        else:
            require(got == expected, f"{row['bank']} {key}: expected {expected}, got {got}")
        checks += 1

    for b, r in {**ordinary, **conditional}.items():
        bd = goal/"banks"/b
        history, forecast = read_csv(bd/"financials.csv"), read_csv(bd/"forecast.csv")
        p, a = load_period(history, "FY2024"), load_period(history, "FY2025")
        check(r, "source_commit", source)
        for key, item in (("assets_2025_m", "total_assets"), ("customer_deposits_2025_m", "customer_deposits"), ("pat_2025_m", "profit_after_tax")):
            check(r, key, a.get(item))
            if b in ordinary and a.get(item) is not None:
                totals[item][b] = a[item]
        for scenario in ("base", "downside", "upside"):
            f = load_period(forecast, "FY2030E", scenario)
            check(r, f"pat_{scenario}_2030_m", f.get("profit_after_tax"))
            check(r, f"car_{scenario}_2030_proxy_pct", capital(f))
        if b in ordinary:
            e = accepted[b]
            require(package_hash(bd) == e["packageFingerprint"], f"package digest mismatch: {b}")
            require(e["macroFingerprint"] == macro, f"macro digest mismatch: {b}")
            require(Path(e["reviewFile"]).name == e["reviewFile"] and e["reviewer"] != e["owner"], f"invalid review metadata: {b}")
            require(text_hash(goal/"reviews"/e["reviewFile"]) == e["reviewSha256"], f"review digest mismatch: {b}")
            for key, field in (("package_sha256", "packageFingerprint"), ("macro_sha256", "macroFingerprint"), ("reviewer", "reviewer")):
                check(r, key, e[field])
            op, cl = p.get("total_equity"), a.get("total_equity")
            valid = op is not None and cl is not None and op > 0 and cl > 0
            status = "unavailable" if op is None or cl is None else "n/m: nonpositive opening or closing equity" if not valid else "caution: equity changed by more than 2x" if cl/op > 2 or cl/op < D(".5") else "comparable"
            for key, expected in {
                "reported_car_2025_pct": a.get("car_pct"), "reported_npl_2025_pct": a.get("npl_pct"),
                "roa_2025_pct": ratio(a.get("profit_after_tax"), avg(p.get("total_assets"), a.get("total_assets"))),
                "equity_open_2025_m": op, "equity_close_2025_m": cl,
                "roe_2025_pct": ratio(a.get("profit_after_tax"), avg(op, cl)) if valid else None,
                "roe_2025_status": status, "roe_closing_equity_2025_pct": ratio(a.get("profit_after_tax"), cl),
                "gross_ldr_2025_pct": ratio(a.get("loans_and_advances_gross"), a.get("customer_deposits")),
            }.items():
                check(r, key, expected)
        else:
            e, m = excluded[b], markers[b]
            require(e["conditional"] == m["label"], f"exclusion marker mismatch: {b}")
            for key, expected in (("scope", m["label"]), ("scope_marker_sha256", m["sha256"]), ("claim_status", e["status"] or ""), ("review_stage", e["stage"] or ""), ("package_sha256", e["packageFingerprint"] or ""), ("macro_sha256", e["macroFingerprint"] or "")):
                check(r, key, expected)
            if e["packageFingerprint"]:
                require(package_hash(bd) == e["packageFingerprint"], f"conditional package digest mismatch: {b}")
            if e["macroFingerprint"]:
                require(e["macroFingerprint"] == macro, f"conditional macro mismatch: {b}")

    aggregate = read_csv(roll/"rollup.csv")
    for item, values in totals.items():
        expected = sum(values.values(), D(0)) if values else None
        t = manifest["totals"][item]
        require(t["n"] == len(values) and set(t["banks"]) == set(values), f"manifest total coverage: {item}")
        require((t["value"] is None and expected is None) or (t["value"] is not None and expected is not None and abs(D(str(t["value"]))-expected) <= D(".000001")), f"manifest total value: {item}")
        rows = [r for r in aggregate if r["table"] == "history_total" and r["period_or_scenario"] == "FY2025" and r["item"] == item and r["bank"] == "ACCEPTED_ONLY"]
        require(len(rows) == 1, f"missing or duplicate roll-up total: {item}")
        r = rows[0]
        require(int(r["n_banks_reporting"]) == len(values) and int(r["n_banks_eligible"]) == len(accepted) and set(filter(None, r["reporting_banks"].split(";"))) == set(values), f"roll-up coverage: {item}")
        require(r["source_commit"] == source and r["input_fingerprint"] == manifest["inputFingerprint"], f"roll-up provenance: {item}")
        check(r, "value", expected)
    return {"sourceCommit": source, "ordinary": len(ordinary), "conditional": len(conditional), "peerCellChecks": checks, "ordinaryTotals": {k: str(sum(v.values(), D(0))) if v else None for k, v in totals.items()}}


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    print(json.dumps(verify(*(Path(x).resolve() for x in sys.argv[1:])), indent=2))
