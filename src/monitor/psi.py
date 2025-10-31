# src/monitor/psi.py
from __future__ import annotations
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd

TARGET = "default.payment.next.month"

def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    # дискретизация по квантилям базового распределения
    qs = np.linspace(0, 1, bins + 1)
    cuts = np.unique(np.quantile(expected, qs))
    e_hist, _ = np.histogram(expected, bins=cuts)
    a_hist, _ = np.histogram(actual,   bins=cuts)
    e = np.clip(e_hist / max(1, e_hist.sum()), 1e-6, 1)
    a = np.clip(a_hist / max(1, a_hist.sum()), 1e-6, 1)
    return float(np.sum((a - e) * np.log(a / e)))

def main(train_csv: str, new_csv: str, out_json: str):
    train = pd.read_csv(train_csv)
    new   = pd.read_csv(new_csv)
    common = [c for c in train.columns if c in new.columns and c != TARGET]
    res = {}
    for c in common:
        if pd.api.types.is_numeric_dtype(train[c]):
            res[c] = psi(train[c].values, new[c].values, bins=10)
    Path(out_json).write_text(json.dumps({"psi": res}, indent=2, ensure_ascii=False))
    print(f"PSI saved to {out_json}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--train", default="data/processed/train.csv")
    p.add_argument("--new",   default="data/processed/test.csv")  # имитация «потока»
    p.add_argument("--out",   default="artifacts/psi.json")
    a = p.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    main(a.train, a.new, a.out)