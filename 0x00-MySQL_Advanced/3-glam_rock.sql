-- List bands with Glam rock as their main style, ranked by longevity
SELECT band_name,
    IF(split = 0, 2022 - formed, 2022 - split) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
