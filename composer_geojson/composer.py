#!/usr/bin/env python3
# composer.py
# Requisiti: solo Python standard library (no dipendenze esterne)

import json
import math
import os
from pathlib import Path
from typing import Any, Iterable

# ---- Configurazione cartelle ----
BASE_DIR = Path(__file__).resolve().parent
INPUT_RAW_DIR = BASE_DIR / "input" / "input_raw"
INPUT_FMT_DIR = BASE_DIR / "input" / "input_formattati"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "aggregato.geojson"

# ---- Utility per coordinate ----
def round_number_7(x: float) -> float:
    """
    Arrotonda a 7 decimali. Se il numero ha <=7 decimali 'intenzionali',
    il valore numerico non cambia e la serializzazione JSON non aggiunge zeri.
    """
    if isinstance(x, (int,)) or (isinstance(x, float) and (math.isinf(x) or math.isnan(x))):
        return x
    return round(float(x), 7)

def round_coords_in_place(obj: Any) -> Any:
    """
    Visita ricorsivamente una struttura di coordinate (liste di liste …) e
    arrotonda tutti i numeri a 7 decimali. Restituisce l’oggetto modificato.
    """
    if isinstance(obj, list):
        return [round_coords_in_place(v) for v in obj]
    elif isinstance(obj, (int, float)):
        return round_number_7(obj)
    else:
        return obj

def normalize_geometry(geom: dict) -> dict:
    """
    Applica arrotondamento coordinate nelle varie tipologie di geometria GeoJSON.
    """
    if not isinstance(geom, dict):
        return geom
    if "coordinates" in geom:
        geom["coordinates"] = round_coords_in_place(geom["coordinates"])
    elif geom.get("type") == "GeometryCollection" and "geometries" in geom:
        geom["geometries"] = [normalize_geometry(g) for g in geom["geometries"]]
    return geom

def normalize_feature(feature: dict) -> dict:
    """
    Arrotonda coordinate della feature; non tocca properties/id.
    """
    if not isinstance(feature, dict):
        return feature
    if feature.get("type") != "Feature":
        return feature
    if "geometry" in feature and feature["geometry"] is not None:
        feature["geometry"] = normalize_geometry(feature["geometry"])
    return feature

def iter_features_from_geojson(doc: dict) -> Iterable[dict]:
    """
    Estrae Feature da:
      - Feature
      - FeatureCollection
    Ignora geometrie raw (non-Feature) per robustezza.
    """
    t = doc.get("type")
    if t == "Feature":
        yield doc
    elif t == "FeatureCollection":
        for f in doc.get("features", []):
            if isinstance(f, dict) and f.get("type") == "Feature":
                yield f

# ---- I/O helper ----
def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_json_minified(path: Path, obj: Any) -> None:
    """
    Scrive il JSON su una sola linea (minificato).
    """
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    path.write_text(s, encoding="utf-8")

# ---- Pipeline ----
def format_input_files() -> list[Path]:
    """
    Legge tutti i file in input_raw, formatta le features (arrotonda coord a 7 decimali)
    e salva in input_formattati come linee singole.
    Ritorna la lista dei file creati in input_formattati.
    """
    INPUT_FMT_DIR.mkdir(parents=True, exist_ok=True)
    created_files: list[Path] = []

    raw_files = sorted(
        [p for p in INPUT_RAW_DIR.glob("**/*") if p.is_file() and p.suffix.lower() in (".json", ".geojson")]
    )

    for raw in raw_files:
        try:
            doc = read_json(raw)
        except Exception as e:
            print(f"[WARN] Impossibile leggere {raw}: {e}")
            continue

        feats = list(iter_features_from_geojson(doc))
        if not feats:
            print(f"[WARN] Nessuna Feature valida in {raw}, salto.")
            continue

        # Se il file ha N feature, salviamo N file formattati (1 feature per file)
        for idx, feat in enumerate(feats, start=1):
            feat_norm = normalize_feature(feat)
            # nome output: basename + (idx se multiple)
            base = raw.stem
            out_name = f"{base}.geojson" if len(feats) == 1 else f"{base}_{idx}.geojson"
            out_path = INPUT_FMT_DIR / out_name
            write_json_minified(out_path, feat_norm)
            created_files.append(out_path)
            print(f"[OK] Formattato → {out_path.relative_to(BASE_DIR)}")
    return created_files

def aggregate_formatted_to_output(fmt_files: list[Path]) -> Path:
    """
    Aggrega tutte le feature formattate in una FeatureCollection unica
    salvata in output/aggregato.geojson
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    features: list[dict] = []

    for fp in sorted(fmt_files):
        try:
            feat = read_json(fp)
        except Exception as e:
            print(f"[WARN] Impossibile leggere formattato {fp}: {e}")
            continue

        # Normalizza nel caso servisse (idempotente)
        for f in iter_features_from_geojson(feat):
            features.append(normalize_feature(f))

    fc = {"type": "FeatureCollection", "features": features}
    write_json_minified(OUTPUT_FILE, fc)
    print(f"[OK] Aggregato → {OUTPUT_FILE.relative_to(BASE_DIR)} (features: {len(features)})")
    return OUTPUT_FILE

def main():
    # Verifica cartelle
    INPUT_RAW_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_FMT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[i] Input RAW:  {INPUT_RAW_DIR}")
    print(f"[i] Input FMT:  {INPUT_FMT_DIR}")
    print(f"[i] Output dir: {OUTPUT_DIR}")

    formatted_files = format_input_files()
    aggregate_formatted_to_output(formatted_files)

if __name__ == "__main__":
    main()
