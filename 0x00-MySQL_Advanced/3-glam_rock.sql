-- Script that lists all bands with Glam rock as their main style, ranked by
-- their longetivity
SELECT 
    name AS band_name, 
    CASE 
        WHEN split IS NULL OR split > 2022 THEN 2022 - formed
	ELSE split - formed
    END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
