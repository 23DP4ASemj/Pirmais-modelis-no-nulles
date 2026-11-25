
from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score


# Nosaka projekta mapi un sakārtoto datu faila atrašanās vietu.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "tirs.csv"

# Nolasa iepriekš sakārtotos automobiļu datus.
df = pd.read_csv(DATA_FILE)

# Izvēlas automobiļa virsbūves tipu kā prognozējamo vērtību.
target = "body-style"

# Sagatavo pazīmes, izņemot prognozējamo kolonnu.
X = df.drop(columns=[target])
y = df[target]

# Nosaka skaitliskās un kategoriskās kolonnas automātiski.
numeric_columns = X.select_dtypes(include="number").columns.tolist()
categorical_columns = X.select_dtypes(exclude="number").columns.tolist()

# Skaitliskajām kolonnām aizpilda iespējamās trūkstošās vērtības ar mediānu.
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

# Kategoriskās kolonnas pārveido skaitļos, izmantojot One-Hot Encoding.
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Apvieno abu tipu datu apstrādi vienā priekšapstrādes procesā.
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_columns),
    ("cat", categorical_transformer, categorical_columns)
])

# Sadala datus apmācības un testa daļā, saglabājot klašu proporcijas.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Izveido modeli, kas izmanto nejaušu lēmumu koku kopu.
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ))
])

# Apmāca modeli, izmantojot tikai apmācības datus.
model.fit(X_train, y_train)

# Prognozē degvielas tipu testa datiem.
predictions = model.predict(X_test)

# Aprēķina modeļa precizitāti uz testa datiem.
model_accuracy = accuracy_score(y_test, predictions)

# Izveido bāzes modeli, kas vienmēr prognozē biežāko degvielas tipu.
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)

# Aprēķina bāzes līnijas precizitāti uz tiem pašiem testa datiem.
baseline_predictions = baseline.predict(X_test)
baseline_accuracy = accuracy_score(y_test, baseline_predictions)

# Izvada abu modeļu precizitāti salīdzināšanai.
print("REZULTĀTI")
print(f"Modeļa precizitāte: {model_accuracy:.2%}")
print(f"Bāzes līnijas precizitāte: {baseline_accuracy:.2%}")

if model_accuracy > baseline_accuracy:
    print("Modelis pārspēj bāzes līniju.")
elif model_accuracy == baseline_accuracy:
    print("Modelis sasniedza tādu pašu rezultātu kā bāzes līnija.")
else:
    print("Modelis nepārspēj bāzes līniju.")

# Iegūst apstrādāto pazīmju nosaukumus un to svarīguma vērtības.
feature_names = model.named_steps["preprocessor"].get_feature_names_out()
importances = model.named_steps["classifier"].feature_importances_

# Saskaita vienas sākotnējās kolonnas kategoriju svarīguma vērtības.
importance_df = pd.DataFrame({
    "column": [name.split("__", 1)[1].split("_", 1)[0]
               if name.startswith("cat__")
               else name.split("__", 1)[1]
               for name in feature_names],
    "importance": importances
})

# Apvieno vienas sākotnējās kolonnas svarīguma vērtības.
importance_df = importance_df.groupby("column")["importance"].sum()
importance_df = importance_df.sort_values(ascending=False)

print("\nDIVAS SVARĪGĀKĀS KOLONNAS")
print(importance_df.head(2).to_string())

# Atrod pirmo testa piemēru, kurā modelis kļūdījās.
wrong_predictions = X_test.copy()
wrong_predictions["actual"] = y_test
wrong_predictions["predicted"] = predictions

errors = wrong_predictions[
    wrong_predictions["actual"] != wrong_predictions["predicted"]
]

print("\nNEPAREIZA PROGNOZE")

if not errors.empty:
    print(errors.iloc[0].to_string())
else:
    print("Testa datos modelim nebija kļūdainu prognožu.")
