# Sales ETL Pipeline

Pipeline ETL de ventes construit avec PySpark. Les données passent par trois niveaux de qualité, puis sont modélisées en étoile, chargées dans PostgreSQL et visualisées dans un dashboard Streamlit.



<video controls width="720">
        <source src="https://raw.githubusercontent.com/yosr11/Pipeline-ETL-de-donn-es-de-ventes/main/pipeline%20vente.mp4" type="video/mp4">
        Votre navigateur ne prend pas en charge la lecture vidéo.
</video>

## Architecture

```text
data/raw/train.csv
        |
        v
01_bronze.py  -> data/bronze/sales       (lecture brute + normalisation des colonnes)
        |
        v
02_silver.py  -> data/silver/sales       (types, dates, doublons et valeurs invalides)
        |
        v
03_gold.py    -> data/gold/*             (faits, dimensions et KPI mensuels)
        |
        v
04_load_postgres.py -> PostgreSQL        (chargement du modèle analytique)
        |
        v
app.py        -> Streamlit                (dashboard des ventes)
```

Le modèle Gold contient :

- `fact_sales` : ventes, commandes, produits, clients et régions ;
- `dim_customer` : dimensions clients ;
- `dim_product` : dimensions produits ;
- `kpi_monthly_sales` : chiffre d'affaires et nombre de commandes par mois.

## Prérequis

- Windows avec Python 3.10 ou plus récent ;
- Java installé et disponible dans le `PATH` pour Spark ;
- PostgreSQL en fonctionnement sur `localhost:5432` ;
- Hadoop Windows installé dans `C:\hadoop`, avec `winutils.exe` dans `C:\hadoop\bin`.

Le script Spark configure automatiquement `HADOOP_HOME`, `PYSPARK_PYTHON` et `PYSPARK_DRIVER_PYTHON` pour cet emplacement Windows.

## Installation

Depuis la racine du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install pyspark pandas pyarrow sqlalchemy psycopg2-binary pg8000 streamlit pytest
```

Si PowerShell bloque l'activation de l'environnement virtuel, exécutez une fois :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Configuration PostgreSQL

Par défaut, les scripts utilisent :

- utilisateur : `postgres` ;
- mot de passe : `postgres` ;
- hôte : `localhost` ;
- port : `5432` ;
- base cible : `sales_dw`.

Pour utiliser un autre mot de passe, définissez `PG_PASSWORD` dans le terminal avant de lancer le pipeline :

```powershell
$env:PG_PASSWORD = "votre_mot_de_passe"
```

## Exécution du pipeline

Lancez les commandes suivantes dans l'ordre depuis la racine du projet :

```powershell
python src\01_bronze.py
python src\02_silver.py
python src\03_gold.py
python src\create_db.py
python src\04_load_postgres.py
```

`create_db.py` crée la base `sales_dw` à partir de la base PostgreSQL `postgres`. Si la base existe déjà, cette étape doit être ignorée ou adaptée.

## Tests de qualité

Les tests vérifient notamment l'absence de commandes invalides, de ventes négatives, de doublons et la conservation du total des ventes entre Silver et Gold :

```powershell
python -m pytest
```

Les fichiers Parquet de `data/bronze`, `data/silver` et `data/gold` sont générés par le pipeline et sont exclus du versionnement par `.gitignore`.

## Dashboard

Après le chargement dans PostgreSQL, démarrez Streamlit :

```powershell
python -m streamlit run app.py
```

Le dashboard affiche :

- l'évolution mensuelle du chiffre d'affaires ;
- le top 10 des produits ;
- les ventes par région.

## Structure du projet

```text
.
├── app.py                    # Dashboard Streamlit
├── data/
│   └── raw/train.csv         # Données sources
├── src/
│   ├── spark_session.py      # Configuration Spark locale
│   ├── 01_bronze.py         # Extraction
│   ├── 02_silver.py         # Nettoyage et validation
│   ├── 03_gold.py           # Modèle analytique
│   ├── 04_load_postgres.py  # Chargement PostgreSQL
│   ├── create_db.py         # Création de sales_dw
│   └── test_pg.py           # Vérification PostgreSQL
└── tests/
    └── test_quality.py      # Tests de qualité des données
```
## Démo


https://github.com/user-attachments/assets/7d99cc09-eec4-40f8-9098-1909e23a7c66

