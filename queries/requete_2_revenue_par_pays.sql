/* requête 2 Revenue total par pays et par opérateur */
SELECT pays, 
       operateur,
       SUM(montant_xof) as revenue_total_xof
FROM telecom_parquet
WHERE statut = 'SUCCESS'
GROUP BY pays, operateur
ORDER BY pays, revenue_total_xof DESC;
