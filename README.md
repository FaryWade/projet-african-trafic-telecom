# Analyse Big Data Serverless des Données de Trafic Télécom en Afrique

## Description
Pipeline d'analyse Big Data serverless sur AWS pour analyser les données de trafic télécom en Afrique (appels, SMS, Data, Mobile Money).

## Architecture
- **Amazon S3** : Data lake (raw/ et processed/)
- **AWS Glue Crawler** : Catalogage automatique des données
- **AWS Glue ETL** : Transformation CSV → Parquet (compression Snappy)
- **Amazon Athena** : Requêtes SQL analytiques
- **IAM** : Gestion des accès et permissions
- **CloudWatch** : Monitoring des jobs

## Structure du projet
```
projet/
├── generate_data.py         # Script de génération du dataset
├── glue_etl_job.py          # Job ETL Glue (CSV → Parquet)
├── queries/
│   ├── requete_1_top10_antennes.sql
│   ├── requete_2_revenue_par_pays.sql
│   ├── requete_3_taux_echec.sql
│   ├── requete_4_momo_par_heure.sql
│   ├── requete_5_distribution_appels.sql
│   ├── requete_6_evolution_quotidienne.sql
│   ├── requete_7_detection_fraude.sql
│   └── requete_8_operateur_fiable.sql
└── README.md
```

## Dataset
- 50 000 lignes générées synthétiquement
- Période : Janvier - Mars 2024
- Pays couverts : Sénégal, Mali, Côte d'Ivoire, Burkina Faso, Guinée
- Opérateurs : Orange, MTN, Moov, Wave, Free

## Résultats clés
- Parquet 8x plus économique que CSV sur Athena
- DATA est le service le plus utilisé (35%)
- MTN domine les revenus au Mali et en Guinée
- Orange est le plus fiable au Burkina Faso et au Sénégal

## Auteurs
Farimata Wade - Khadidiatou Diallo - ISI Dakar 
