/* Requête 6 Évolution quotidienne du nombre d'événements */
SELECT 
  DATE(CAST(date_heure AS TIMESTAMP)) as date_jour,
  COUNT(*) as nb_evenements,
  SUM(CASE WHEN type_evenement = 'CALL' THEN 1 ELSE 0 END) as nb_appels,
  SUM(CASE WHEN type_evenement = 'SMS' THEN 1 ELSE 0 END) as nb_sms,
  SUM(CASE WHEN type_evenement = 'DATA' THEN 1 ELSE 0 END) as nb_data,
  SUM(CASE WHEN type_evenement = 'MOMO' THEN 1 ELSE 0 END) as nb_momo
FROM telecom_parquet
GROUP BY DATE(CAST(date_heure AS TIMESTAMP))
ORDER BY date_jour
LIMIT 10;
