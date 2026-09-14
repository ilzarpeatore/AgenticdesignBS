# Módulo: Calentamiento y activación

**Tipo:** General
**Se activa cuando:** siempre — cada sesión de cada cliente, sea cual sea el objetivo. Es, junto con `contraindicaciones-medicas.md` y `gestion-fatiga-deload.md`, un módulo "de fondo".
**Versión:** 0.1.0 · **Última actualización:** 2026-09-14
**Procedencia:** primer módulo escrito desde cero — no existía ninguna cobertura de calentamiento en el sistema hasta ahora.

## 1. Protocolo base: RAMP

Estructura en 4 fases secuenciales (Jeffreys, 2007), adaptable en duración según la sesión y el tiempo disponible:

1. **Raise (elevar):** actividad aeróbica de baja intensidad (2-5 min) para subir temperatura corporal y frecuencia cardíaca.
2. **Activate (activar):** ejercicios dinámicos que implican a los grupos musculares principales de la sesión (ej. zancadas, elevaciones de rodilla) — 2-4 min.
3. **Mobilize (movilizar):** trabajo de movilidad articular específico de los patrones que se van a entrenar ese día (ej. movilidad de cadera antes de sentadilla/bisagra) — 2-3 min.
4. **Potentiate (potenciar):** preparación para el esfuerzo de mayor intensidad de la sesión mediante movimientos progresivamente más explosivos o series de aproximación — obligatorio si la sesión incluye pliometría o cargas cercanas al máximo; opcional/breve si la sesión es de intensidad moderada.

**Duración total orientativa:** 10-15 min en una sesión completa; se puede comprimir a 5-8 min combinando Raise+Activate cuando `disponibilidad.minutos_por_sesion` es ajustada — nunca eliminar por completo la fase Potentiate si el día incluye pliometría o cargas máximas.

## 2. Series de aproximación antes de las series de trabajo (fuerza)

- El número óptimo de series de aproximación se sitúa orientativamente entre 3 y 5, subiendo de carga progresivamente hacia el peso de la primera serie de trabajo.
- Cuanto más exigente sea la carga objetivo, más importa que las series de aproximación se acerquen a esa carga — series de aproximación demasiado ligeras (ej. ≈40% del peso de trabajo) rinden peor que series más cercanas (≈80%) en ejercicios de tren inferior con cargas altas.
- **No te excedas:** demasiadas series de aproximación, o series de aproximación demasiado exigentes, pueden restar rendimiento a las series de trabajo por fatiga acumulada antes de tiempo. Planifica el número de series de aproximación, no lo dejes libre.

## 3. Estiramiento estático: cuándo sí y cuándo no

- Estiramientos estáticos **cortos (≤60 segundos por grupo muscular)**, integrados dentro de un calentamiento completo (con parte aeróbica y dinámica), tienen un efecto trivial sobre la fuerza y potencia posteriores (~1-2% de reducción).
- Estiramientos estáticos **largos (>60 segundos por grupo muscular)** sí producen una reducción relevante de fuerza y potencia (~4-7.5%).
- **Regla práctica:** si el cliente quiere o necesita estiramiento estático (por preferencia, por una limitación de movilidad concreta), colócalo **al final de la sesión**, no en el calentamiento. El calentamiento se apoya en movimiento dinámico y movilidad activa, no en estiramiento estático mantenido.

## 4. Calentamiento en contextos con tiempo limitado

Cuando `disponibilidad.minutos_por_sesion` es baja, prioriza en este orden: Raise breve → Activate de los patrones clave del día → series de aproximación del primer ejercicio (que ya hacen de Potentiate para fuerza). Solo mantén una fase Potentiate explícita separada si el día incluye pliometría de intensidad media/alta (ver `pliometria-rigidez-tendinosa.md`) — ahí no es negociable.

## Conflictos conocidos con otros módulos

- **Con `pliometria-rigidez-tendinosa.md`:** ningún trabajo pliométrico de intensidad media o alta empieza sin haber completado la fase Potentiate — no se entra "en frío" a saltos unilaterales ni drop jumps.
- **Con `contraindicaciones-medicas.md`:** en contraindicaciones relativas cardiovasculares (ej. hipertensión no controlada con autorización), la fase Raise debe ser más gradual, sin picos bruscos de intensidad.
- **Con la disponibilidad del cliente (`perfil_cliente.disponibilidad`):** el tiempo de calentamiento cuenta dentro de `minutos_por_sesion` — no se planifica el resto de la sesión ignorando este tiempo.

## Referencias

- Jeffreys, I. (2007). *Warm-up revisited: The RAMP method of optimizing warm-ups.* Professional Strength and Conditioning.
- Estudios sobre número óptimo de series de aproximación y carga relativa de las mismas (BarBend/revisión de literatura, 2024-2025).
- Behm, D. G., et al. (2019). *Acute Effects of Static Stretching on Muscle Strength and Power: An Attempt to Clarify Previous Caveats.* Frontiers in Physiology.
