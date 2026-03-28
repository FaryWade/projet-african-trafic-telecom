/*  Requête 8 Opérateur le plus fiable par pays*/
SELECT 
  pays,
  operateur,
  COUNT(*) as total_transactions,
  ROUND(SUM(CASE WHEN statut = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_succes_pct
FROM telecom_parquet
GROUP BY pays, operateur
ORDER BY pays, taux_succes_pct DESC;
