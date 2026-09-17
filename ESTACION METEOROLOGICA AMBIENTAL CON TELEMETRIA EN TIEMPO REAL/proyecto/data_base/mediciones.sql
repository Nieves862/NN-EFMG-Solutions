-- SQL
CREATE DATABASE estacionmetereologica_proa;

USE estacionmetereologica_proa;

CREATE TABLE mediciones (
    id_mediciones INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperatura INT, 		 -- El DHT11 mide de 1 en 1 grado, un INT es más que suficiente y eficiente
    humedad INT      		 -- ¡Perfecto! Como es entera, guardamos un INT (ocupa poquísimo espacio)
);

-- Consulta de prueba (para verificar que se creó vacía)
SELECT * FROM mediciones;

SELECT * FROM mediciones ORDER BY id_mediciones DESC;

INSERT INTO mediciones (temperatura, humedad) 
VALUES (12, 86);

-- SQL TEMPERATURAS
SELECT 
    fecha_hora, 
    temperatura,
    humedad,
    CASE 
        WHEN temperatura > 30 THEN 'ALERTA: CALOR'
        WHEN temperatura < 15 THEN 'ALERTA: FRIO'
        ELSE 'ESTADO OPTIMO'
    END AS diagnostico_clima
FROM mediciones;

-- 10/08/2026
ALTER TABLE mediciones 
ADD COLUMN gas INT AFTER humedad;

-- 3. Inserciones de prueba (Normal, Calor y Fuga de Gas)
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (24, 55, 120); -- Óptimo
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (36, 40, 150); -- Alerta Calor
INSERT INTO mediciones (temperatura, humedad, gas) VALUES (22, 60, 480); -- Alerta Fuga de Gas

SELECT 
    fecha_hora,
    temperatura,
    humedad,
    gas,
    CASE 
        WHEN gas > 300 THEN 'ALERTA: GAS / ANOMALÍA EN AIRE'
        WHEN temperatura >= 35 THEN 'ALERTA: CALOR EXTREMO'
        WHEN temperatura <= 15 THEN 'ALERTA: FRÍO EXTREMO'
        ELSE 'ESTADO ÓPTIMO'
    END AS diagnostico_integral
FROM mediciones 
ORDER BY fecha_hora DESC;

-- 02/09/2026 Tipos de AIRES
SELECT 
    fecha_hora,
    gas,
    CASE 
        WHEN gas > 500 THEN 'ALERTA CRÍTICA: FUGA DE GAS / CONCENTRACIÓN ALTA'
        WHEN gas BETWEEN 250 AND 500 THEN 'ALERTA MEDIA: HUMO / VAPORES EN AIRE'
        WHEN gas BETWEEN 120 AND 249 THEN 'PRECAUCIÓN: AIRE POCO PURO'
        ELSE 'ESTADO ÓPTIMO'
    END AS diagnostico_aire
FROM mediciones 
ORDER BY id_mediciones DESC;



