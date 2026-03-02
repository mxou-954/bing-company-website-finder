# Site Scraper — Recherche automatique de sites officiels

Script Python qui enrichit un fichier Excel d'entreprises en trouvant automatiquement leur site officiel via Bing.

Né du besoin de normaliser rapidement des centaines de fiches prospects qui n'avaient pas de site web renseigné dans le CRM.

---

## Comment ça marche

Pour chaque entreprise (colonne "Raison Sociale") :

1. Lance une recherche Bing en headless (Selenium + Chrome)
2. Parcourt les premiers résultats
3. Filtre les domaines parasites (annuaires, réseaux sociaux, Wikipedia, presse...)
4. Conserve le premier lien pertinent comme "site officiel"
5. Sauvegarde le fichier après chaque ligne (reprise possible en cas d'interruption)

---

## Structure

```
site-scraper/
├── main.py              ← Point d'entrée
├── config.py            ← Constantes (timeouts, patterns exclus, etc.)
├── driver.py            ← Initialisation Chrome headless
├── scraper.py           ← Logique de recherche Bing + filtrage
├── excel_handler.py     ← Lecture / écriture Excel
├── requirements.txt
└── README.md
```

---

## Installation

### Prérequis

- Python >= 3.10
- Google Chrome installé
- ChromeDriver compatible (ou dans le PATH)

### Dépendances

```bash
pip install -r requirements.txt
```

---

## Utilisation

```bash
python main.py <fichier_input.xlsx> <fichier_output.xlsx>
```

### Exemple

```bash
python main.py prospects_brut.xlsx prospects_enrichis.xlsx
```

Le script affiche la progression en temps réel :

```
[1/350] Recherche Bing pour 'Dupont SAS' ... https://www.dupont-sas.fr
[2/350] Recherche Bing pour 'Martin & Co' ... https://www.martin-co.com
[3/350] Recherche Bing pour '' ... vide → aucune URL
```

---

## Configuration

Tout se modifie dans `config.py` :

| Variable | Default | Description |
|----------|---------|-------------|
| `DRIVER_PATH` | `None` | Chemin vers chromedriver (None = auto-detect dans PATH) |
| `PAGE_LOAD_TIMEOUT` | `20` | Timeout chargement page Bing (secondes) |
| `PAUSE_BETWEEN` | `1.5` | Pause entre chaque requête (anti-blocage Bing) |
| `MAX_RESULTS` | `10` | Nombre de liens Bing inspectés par recherche |
| `BAD_PATTERNS` | voir fichier | Domaines/mots-clés à exclure des résultats |

### Domaines exclus par défaut

Les résultats provenant de ces domaines sont automatiquement ignorés : societe.com, pappers.fr, linkedin.com, facebook.com, Wikipedia, PagesJaunes, presse généraliste, etc. La liste complète est dans `config.py`.

---

## Format Excel

### Entrée (obligatoire)

| Raison Sociale |
|----------------|
| Dupont SAS |
| Martin & Co |
| ... |

### Sortie (ajoutée automatiquement)

| Raison Sociale | Site officiel |
|----------------|---------------|
| Dupont SAS | https://www.dupont-sas.fr |
| Martin & Co | https://www.martin-co.com |

---

## Notes

- Le fichier est sauvegardé après **chaque entreprise** : en cas de crash ou d'interruption, relancez simplement la commande avec le fichier de sortie comme input pour reprendre là où vous en étiez.
- Augmentez `PAUSE_BETWEEN` si Bing bloque les requêtes (captcha).
- Le mode headless ne consomme quasiment pas de ressources graphiques.
