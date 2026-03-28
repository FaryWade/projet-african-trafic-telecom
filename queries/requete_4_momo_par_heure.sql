/* Requête 4  Volume Mobile Money par heure de la journée */
SELECT HOUR(CAST(date_heure AS TIMESTAMP)) as heure,
       COUNT(*) as nb_transactions,
       SUM(montant_xof) as volume_total_xof
FROM telecom_parquet
WHERE type_evenement = 'MOMO'
GROUP BY HOUR(CAST(date_heure AS TIMESTAMP))
ORDER BY heure;
