# 🌤️ Estación Meteorológica y Ambiental con Telemetría en Tiempo Real

> **Proyecto para Práctica Profesionalizante I — Escuela PRoA (Sede Río Tercero)**  
> **Desarrollado por:** N²-EFMG Solutions  
> **Repositorio Oficial:** [NN-EFMG-Solutions] 

---

## 📌 Descripción del Proyecto

Sistema integral de adquisición, almacenamiento y visualización de variables ambientales en tiempo real desarrollado para la **Escuela PRoA Río Tercero**. 

La solución captura parámetros físicos críticos (**temperatura**, **humedad relativa** y **calidad del aire / detección de gases MQ-2**) a través de una arquitectura basada en **Arduino UNO**. Los datos son transmitidos vía interfaz serial USB hacia un servicio en **Python 3.12**, el cual procesa las tramas, valida la integridad de las lecturas y las inyecta de forma persistente en un motor de base de datos **MySQL Server**.

El sistema dispone de un **Dashboard CLI (Panel de Control)** responsivo en consola que presenta las métricas operativas en vivo y genera **alertas climáticas y de riesgo ambiental** de forma dinámica según umbrales preconfigurados.

---

## 🏗️ Arquitectura del Sistema

```text
[ Sensor DHT11 ] ──┐
                   ├──> [ Arduino UNO ] ──(Serial USB)──> [ Python Dashboard ] ──> [ MySQL DB ]
[ Sensor MQ-2  ] ──┘                                      (Colorama / PySerial)     (mediciones)
