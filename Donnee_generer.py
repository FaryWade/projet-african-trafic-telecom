# ============================================================
# ÉTAPE 1 — Génération du dataset télécom africain
# ============================================================
# On importe les bibliothèques dont on a besoin
import pandas as pd        # Pour créer et manipuler des tableaux de données
import random              # Pour générer des valeurs aléatoires
from datetime import datetime, timedelta  # Pour créer des dates
import os                  # Pour créer des dossiers

# ============================================================

NB_LIGNES = 50000          # Nombre de lignes à générer (50 000 ici)
DATE_DEBUT = datetime(2024, 1, 1)   # Les données commencent le 1er jan 2024
DATE_FIN   = datetime(2024, 3, 31)  # Et finissent le 31 mars 2024

# ============================================================
# LISTES DE VALEURS POSSIBLES
# ============================================================
# Les pays africains couverts
PAYS = ["Senegal", "Mali", "Cote_Ivoire", "Burkina_Faso", "Guinea"]

# Les opérateurs télécom africains
OPERATEURS = ["Orange", "MTN", "Moov", "Wave", "Free"]

# Les types d'événements possibles
TYPES = ["CALL", "SMS", "DATA", "MOMO"]  # MOMO = Mobile Money

# Les statuts possibles
STATUTS = ["SUCCESS", "FAILED"]

# ============================================================
# FONCTION QUI GÉNÈRE UNE SEULE LIGNE / TRANSACTION
# ============================================================
def generer_ligne(i):
    """
    Cette fonction crée une transaction télécom aléatoire.
    'i' est juste le numéro de la ligne, pour créer un ID unique.
    """

    # Choisir un pays au hasard
    pays = random.choice(PAYS)

    # Choisir un opérateur au hasard
    operateur = random.choice(OPERATEURS)

    # Choisir un type d'événement au hasard
    # On met DATA et CALL plus souvent que SMS et MOMO (plus réaliste)
    type_evt = random.choices(
        TYPES,
        weights=[30, 20, 35, 15]  # 30% CALL, 20% SMS, 35% DATA, 15% MOMO
    )[0]

    # Générer une date/heure aléatoire entre DATE_DEBUT et DATE_FIN
    delta = DATE_FIN - DATE_DEBUT
    secondes_aleatoires = random.randint(0, int(delta.total_seconds()))
    date_heure = DATE_DEBUT + timedelta(seconds=secondes_aleatoires)

    # Créer un numéro de client anonymisé (ex: SN_004821)
    # On utilise un préfixe du pays + un numéro aléatoire
    prefixe_pays = pays[:2].upper()  # "SN" pour Senegal, "ML" pour Mali...
    msisdn = f"{prefixe_pays}_{random.randint(100000, 999999)}"

    # Générer la durée en secondes (seulement utile pour les appels)
    if type_evt == "CALL":
        duree = random.randint(10, 600)    # Entre 10 sec et 10 min
    else:
        duree = 0  # Pas de durée pour SMS, DATA, MOMO

    # Générer le volume de données en Mo (seulement pour DATA)
    if type_evt == "DATA":
        volume_mb = round(random.uniform(0.1, 500.0), 2)  # Entre 0.1 et 500 Mo
    else:
        volume_mb = 0.0

    # Générer le montant en francs CFA
    if type_evt == "MOMO":
        montant = random.randint(500, 500000)   # Transfert d'argent
    elif type_evt == "CALL":
        montant = random.randint(10, 2000)      # Coût d'un appel
    elif type_evt == "DATA":
        montant = random.randint(50, 5000)      # Forfait data
    else:  # SMS
        montant = random.randint(10, 100)

    # Générer le statut (90% succès, 10% échec — réaliste)
    statut = random.choices(
        STATUTS,
        weights=[90, 10]  # 90% SUCCESS, 10% FAILED
    )[0]

    # Générer l'identifiant de l'antenne réseau
    # Format : ANT_DKR_042 (ANT = antenne, DKR = Dakar, 042 = numéro)
    villes = ["DKR", "ABJ", "BKO", "OUA", "CKY"]  # Codes de villes
    ville = random.choice(villes)
    numero_antenne = random.randint(1, 200)
    antenne_id = f"ANT_{ville}_{numero_antenne:03d}"  # :03d = 3 chiffres (001, 042...)

    # Retourner toutes les valeurs sous forme de dictionnaire
    return {
        "msisdn": msisdn,
        "date_heure": date_heure.strftime("%Y-%m-%d %H:%M:%S"),  # Format standard
        "pays": pays,
        "operateur": operateur,
        "type_evenement": type_evt,
        "duree_secondes": duree,
        "volume_mb": volume_mb,
        "montant_xof": montant,
        "statut": statut,
        "antenne_id": antenne_id
    }

# ============================================================
# GÉNÉRATION DE TOUTES LES LIGNES
# ============================================================
print(f"Génération de {NB_LIGNES} lignes en cours...")

# On appelle generer_ligne() autant de fois que NB_LIGNES
# et on stocke tout dans une liste
data = [generer_ligne(i) for i in range(NB_LIGNES)]

# On transforme la liste en tableau (DataFrame pandas)
df = pd.DataFrame(data)

print(f"Dataset créé : {len(df)} lignes, {len(df.columns)} colonnes")
print(df.head())  # Affiche les 5 premières lignes pour vérifier

# ============================================================
# SAUVEGARDE EN CSV avec structure de dossiers (partitionnement Hive)
# ============================================================
# Le projet demande une structure de dossiers par date :
# raw/telecom/year=2024/month=01/day=15/
# On va créer un fichier par mois pour simplifier

# Ajouter des colonnes year, month, day pour le partitionnement
df["date_heure_dt"] = pd.to_datetime(df["date_heure"])
df["year"]  = df["date_heure_dt"].dt.year
df["month"] = df["date_heure_dt"].dt.month
df["day"]   = df["date_heure_dt"].dt.day

# Grouper les données par mois et sauvegarder chaque groupe
for (year, month), groupe in df.groupby(["year", "month"]):

    # Créer le chemin du dossier
    dossier = f"raw/telecom/year={year}/month={month:02d}/day=01"
    os.makedirs(dossier, exist_ok=True)  # Créer le dossier s'il n'existe pas

    # Supprimer les colonnes temporaires avant de sauvegarder
    groupe_clean = groupe.drop(columns=["date_heure_dt", "year", "month", "day"])

    # Sauvegarder en CSV
    chemin_fichier = f"{dossier}/telecom_data.csv"
    groupe_clean.to_csv(chemin_fichier, index=False)
    print(f"Sauvegardé : {chemin_fichier} ({len(groupe_clean)} lignes)")

print("\nTerminé ! Tous les fichiers CSV sont dans le dossier 'raw/'")
