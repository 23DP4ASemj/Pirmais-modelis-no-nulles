# Rezultātu interpretācija

### 1. Kas ir šie dati un no kurienes tie nāk?

Izmantota UCI Machine Learning Repository datu kopa "Automobile". Tajā ir informācija par 1985. gada automobiļiem. Sākotnēji bija 205 rindas un 26 kolonnas.

Avots: https://archive.ics.uci.edu/dataset/10/automobile

### 2. Kas ar datiem bija nepareizi un ko tu ar tiem izdarīji?

Datos bija trūkstošas vērtības. Tika izmestas 4 rindas bez cenas un 0 dublikātu rindas. Skaitliskās vērtības tika aizpildītas ar mediānu, bet kategoriskās - ar biežāko vērtību. Pēc tīrīšanas palika 201 rinda un 0 trūkstošu vērtību.

### 3. Ko modelis prognozē un cik labi?

Modelis prognozē automobiļa virsbūves tipu (`body-style`). Izmantots RandomForestClassifier.

- Modeļa precizitāte: 70,73%.
- Bāzes līnijas precizitāte: 46,34%.

Modelis pārspēja bāzes līniju par 24,39 procentpunktiem.

### 4. Kuras divas kolonnas izrādījās svarīgākās un vai tas ir loģiski?

- `num-of-doors` - 0.124270.
- `height` - 0.102719.

Tas ir loģiski, jo durvju skaits un automobiļa augstums ir saistīti ar virsbūves tipu.

### 5. Viena konkrēta rinda, kurā modelis kļūdījās

Modelis kļūdījās, prognozējot Nissan automobili:

- Faktiskais virsbūves tips: `hatchback`.
- Modeļa prognoze: `sedan`.
- Cena: 8949.

Iespējams, automobiļa īpašības bija līdzīgas sedan tipa automobiļiem.

### 6. Ko ar šo modeli NEDRĪKST darīt?

Šo modeli nedrīkst izmantot automobiļu automātiskai klasificēšanai CSDD reģistrācijas dokumentos bez cilvēka pārbaudes. Modeļa precizitāte ir tikai 70,73%, tāpēc tas var kļūdaini noteikt automobiļa virsbūves tipu un radīt nepareizus datus dokumentos.

### Pašvērtējums

Man izdevās sakārtot datus un izveidot modeli, kas pārspēja bāzes līniju. Man neizdevās panākt, lai modelis pareizi prognozētu visus automobiļus. Nākamreiz es izmēģinātu citus modeļa iestatījumus, lai uzlabotu rezultātu.