/* Requête 3 Taux d'échec par type d'événement */
SELECT type_evenement,
       COUNT(*) as total,
       SUM(CASE WHEN statut = 'FAILED' THEN 1 ELSE 0 END) as total_echecs,
       ROUND(SUM(CASE WHEN statut = 'FAILED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taux_echec_pct
FROM telecom_parquet
GROUP BY type_evenement
ORDER BY taux_echec_pct DESC;
