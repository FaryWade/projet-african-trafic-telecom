/* Requête 5 — Distribution des appels par durée */
SELECT 
  CASE 
    WHEN duree_secondes < 60 THEN 'Moins de 1 min'
    WHEN duree_secondes BETWEEN 60 AND 300 THEN '1 à 5 min'
    ELSE 'Plus de 5 min'
  END as categorie_duree,
  COUNT(*) as nb_appels,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pourcentage
FROM telecom_parquet
WHERE type_evenement = 'CALL'
GROUP BY 
  CASE 
    WHEN duree_secondes < 60 THEN 'Moins de 1 min'
    WHEN duree_secondes BETWEEN 60 AND 300 THEN '1 à 5 min'
    ELSE 'Plus de 5 min'
  END
ORDER BY nb_appels DESC;
