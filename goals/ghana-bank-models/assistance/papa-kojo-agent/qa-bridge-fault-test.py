"""Fault injection on scratch copy; tests historical bridge status, statement, unit.
Usage: python -I qa-bridge-fault-test.py /path/to/goals/ghana-bank-models
"""
import csv, importlib.util, pathlib, shutil, sys, tempfile
root=pathlib.Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location("validator",root/"sector/qa-sweep/validate.py")
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
with tempfile.TemporaryDirectory() as tmp:
    dest=pathlib.Path(tmp)/"prudential-bank"
    shutil.copytree(root/"banks/prudential-bank",dest)
    qa.BANKS=tmp
    f=dest/"financials.csv"
    original=f.read_bytes()
    for name,patch in [
        ("baseline",{}),("wrong_statement",{"statement":"income_statement"}),
        ("estimated_history",{"status":"estimated"}),
        ("wrong_unit",{"unit":"percent"}),("wrong_amount",{"value":"1.000"})]:
        f.write_bytes(original)
        with f.open(encoding="utf-8-sig",newline="") as inp:
            reader=csv.DictReader(inp);fields=reader.fieldnames;rows=list(reader)
        target=[r for r in rows if r["line_item"]=="x_amounts_written_off_bridge" and r["period"]=="FY2024"]
        assert len(target)==1,target
        target[0].update(patch)
        with f.open("w",encoding="utf-8",newline="") as out:
            writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows)
        result=qa.check_bank("prudential-bank")
        print(name,"FAIL",len(result["fail"]),"WARN",len(result["warn"]),result["fail"])
