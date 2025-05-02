-- Script to rank country origins of bands, ordered by their number of fans
SELECT origin, SUM(fans) AS nb_fans FROM metal_bands 
WHERE origin IS NOT NULL
GROUP BY origin
ORDER BY nb_fans DESC;
