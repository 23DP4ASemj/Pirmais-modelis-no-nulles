## Ko dara šis projekts?

1. Nolasa sākotnējos automobiļu datus.
2. Pārbauda un sakārto datus.
3. Aizpilda trūkstošās vērtības un izdzēš rindas bez norādītas cenas.
4. Izveido mašīnmācīšanās modeli, kas prognozē automobiļa virsbūves tipu.
5. Salīdzina modeļa rezultātus ar bāzes līniju.
6. Parāda divas svarīgākās datu kolonnas.

## Kā palaist projektu?

Lai palaistu projektu, datorā jābūt instalētam Python.

Vispirms instalē nepieciešamās bibliotēkas:

```bash
pip install pandas scikit-learn
```

Pēc tam palaid datu tīrīšanas skriptu:

```bash
python 01_tirisana.py
```

Šis skripts izveidos sakārtotu datu failu `tirs.csv`.

Kad datu tīrīšana ir pabeigta, palaid modeli:

```bash
python 02_modelis.py
```

Terminālī būs redzama modeļa precizitāte, bāzes līnijas precizitāte, svarīgākās kolonnas un viena kļūdaina prognoze, ja tāda ir.

## Izmantotās bibliotēkas

- **Pandas** - datu nolasīšanai un apstrādei.
- **Scikit-learn** - datu sagatavošanai, modeļa apmācībai un rezultātu pārbaudei.

## Projekta struktūra

```text
Pirmais-modelis-no-nulles/
│
├── dati/
│   ├── imports-85.data
│   ├── imports-85.names
│   └── AVOTS.txt
│
├── 01_tirisana.py
├── 02_modelis.py
├── tirs.csv
├── rezultati.md
└── README.md
```

## Datu avots

UCI Machine Learning Repository - Automobile Dataset

https://archive.ics.uci.edu/dataset/10/automobile

