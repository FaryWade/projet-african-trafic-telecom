/* requête 1 Top 10 antennes par volume data */
SELECT antenne_id, 
       ROUND(SUM(volume_mb), 2) as volume_total_mb
FROM telecom_parquet
WHERE type_evenement = 'DATA'
GROUP BY antenne_id
ORDER BY volume_total_mb DESC
LIMIT 10;
