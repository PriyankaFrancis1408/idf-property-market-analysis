import pandas as pd
from pathlib import Path

folder = Path(".")
files = sorted(folder.glob("*.csv.gz"))
print(len(files), "files found")

frames = [pd.read_csv(f, low_memory=False) for f in files]
df = pd.concat(frames, ignore_index=True)

print("ALL ROWS:", df.shape)

homes = df[df["type_local"].isin(["Appartement", "Maison"])]

print("ONLY HOMES:", homes.shape)
print(homes["type_local"].value_counts())

print("Rows:", len(homes))
print("Unique sales:", homes["id_mutation"].nunique())

rows_per_sale = homes.groupby("id_mutation").size()
print(rows_per_sale.value_counts().head())

sale_sizes = homes["id_mutation"].value_counts()
single_sales = sale_sizes[sale_sizes == 1].index

clean = homes[homes["id_mutation"].isin(single_sales)].copy()

print("CLEAN:", clean.shape)

print("Missing price:", clean["valeur_fonciere"].isna().sum())
print("Missing area:", clean["surface_reelle_bati"].isna().sum())
print("Area equal to 0:", (clean["surface_reelle_bati"] == 0).sum())

clean = clean.dropna(subset=["valeur_fonciere", "surface_reelle_bati"])

clean["prix_m2"] = clean["valeur_fonciere"] / clean["surface_reelle_bati"]

print("AFTER DROP:", clean.shape)
print(clean["prix_m2"].describe().round(0))

before = len(clean)

clean = clean[(clean["prix_m2"] >= 500) & (clean["prix_m2"] <= 30000)]

print("REMOVED:", before - len(clean))
print("FINAL:", clean.shape)
print(clean["prix_m2"].describe().round(0))

cols = [
    "id_mutation", "date_mutation", "code_departement", "nom_commune",
    "code_postal", "type_local", "valeur_fonciere", "surface_reelle_bati",
    "nombre_pieces_principales", "surface_terrain",
    "longitude", "latitude", "prix_m2",
]

clean[cols].to_csv("dvf_clean_idf_2025.csv", index=False)
print("Saved:", len(clean), "rows")