/* Requête 7 : Détection de fraude (clients avec +10 transactions MOMO dans la journée) */
SELECT 
  msisdn,
  DATE(CAST(date_heure AS TIMESTAMP)) as date_jour,
  COUNT(*) as nb_transactions_momo,
  SUM(montant_xof) as montant_total_xof
FROM telecom_parquet
WHERE type_evenement = 'MOMO'
  AND statut = 'SUCCESS'
GROUP BY msisdn, DATE(CAST(date_heure AS TIMESTAMP))
HAVING COUNT(*) > 10
ORDER BY nb_transactions_momo DESC
LIMIT 20;
