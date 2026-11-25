from pathlib import Path
import pandas as pd

# Nosaka projekta mapes atrašanās vietu, lai failu ceļi darbotos neatkarīgi no termināļa mapes.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "dati" / "imports-85.data"
OUTPUT_FILE = PROJECT_DIR / "tirs.csv"

# Piešķir datu kopas 26 kolonnām nosaukumus atbilstoši UCI dokumentācijai.
columns = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location",
    "wheel-base", "length", "width", "height", "curb-weight",
    "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
    "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
    "city-mpg", "highway-mpg", "price"
]

# Nolasa oriģinālo komatatdalīto failu un pārvērš simbolu '?' par trūkstošu vērtību.
df = pd.read_csv(
    DATA_FILE,
    header=None,
    names=columns,
    na_values="?",
    skipinitialspace=True
)

initial_rows = len(df)
print(f"Rindu skaits sākumā: {initial_rows}")

# Pārvērš skaitliskās kolonnas skaitļu tipos, jo sākotnējā failā tās var būt nolasītas kā teksts.
numeric_columns = [
    "symboling", "normalized-losses", "wheel-base", "length", "width",
    "height", "curb-weight", "engine-size", "bore", "stroke",
    "compression-ratio", "horsepower", "peak-rpm", "city-mpg",
    "highway-mpg", "price"
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Noņem pilnīgi vienādas rindas, lai viena automašīna netiktu ieskaitīta vairākas reizes.
duplicates_removed = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Izmet rindas bez cenas, jo cenu nevar izmantot apmācībā, ja pareizā atbilde nav zināma.
missing_price_removed = int(df["price"].isna().sum())
df = df.dropna(subset=["price"]).copy()

# Aizpilda skaitlisko pazīmju trūkstošās vērtības ar mediānu, ko mazāk ietekmē ekstrēmas vērtības.
numeric_features = [column for column in numeric_columns if column != "price"]
numeric_filled = {}
for column in numeric_features:
    missing_count = int(df[column].isna().sum())
    if missing_count > 0:
        df[column] = df[column].fillna(df[column].median())
        numeric_filled[column] = missing_count

# Aizpilda kategorisko pazīmju trūkstošās vērtības ar biežāko vērtību, saglabājot pārējās rindas.
categorical_columns = df.select_dtypes(exclude="number").columns.tolist()
categorical_filled = {}
for column in categorical_columns:
    missing_count = int(df[column].isna().sum())
    if missing_count > 0:
        most_common = df[column].mode(dropna=True)
        if not most_common.empty:
            df[column] = df[column].fillna(most_common.iloc[0])
            categorical_filled[column] = missing_count

# Saglabā iztīrītos datus atsevišķā CSV failā, nemainot lejupielādēto oriģinālu.
df.to_csv(OUTPUT_FILE, index=False)

removed_total = duplicates_removed + missing_price_removed
print("\nTīrīšanas pārskats:")
print(f"Dublikātu rindas izdzēstas: {duplicates_removed}")
print(f"Rindas bez cenas izdzēstas: {missing_price_removed}")
print(f"Kopā izdzēstas rindas: {removed_total}")
print(f"Rindu skaits beigās: {len(df)}")
print(f"Aizpildītās skaitliskās vērtības: {numeric_filled}")
print(f"Aizpildītās kategoriskās vērtības: {categorical_filled}")
print(f"Atlikušās trūkstošās vērtības: {int(df.isna().sum().sum())}")
print(f"\nFails saglabāts: {OUTPUT_FILE}")
