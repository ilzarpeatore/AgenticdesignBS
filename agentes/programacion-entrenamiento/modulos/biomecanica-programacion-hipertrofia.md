# Módulo: Biomecánica y programación de carga para hipertrofia

**Tipo:** General
**Se activa cuando:** el objetivo incluye ganancia de tamaño muscular como componente relevante — casi siempre junto con `hipertrofia-recomposicion-corporal.md`, pero también con cualquier otro módulo de objetivo que incluya hipertrofia como parte del plan (ej. un deportista que además quiere ganar masa en fase de base).
**Versión:** 0.2.0 · **Última actualización:** 2026-09-14
**Procedencia:** primer módulo escrito desde cero. Cubre el "cómo entrenar" a nivel de ejercicio y serie; `hipertrofia-recomposicion-corporal.md` cubre el "cuánto y en qué contexto energético".

> Este módulo responde a una pregunta de control de calidad directa: ¿el agente sabe programar carga/volumen a nivel fino y conoce la biomecánica de la hipertrofia, o solo maneja el contexto de déficit/superávit? Antes de este módulo, no. Con él, sí.

## 1. Perfiles de resistencia (curvas de fuerza) y selección de ejercicio

Cada ejercicio tiene una curva de fuerza distinta a lo largo de su rango de movimiento — dónde es "más difícil" no es uniforme:

- **Ascendente:** más difícil al final del recorrido (ej. la mayoría de ejercicios de empuje — press banca, sentadilla cerca del lockout). Carga mucho los elementos pasivos (tendón/articulación) en el tramo final.
- **Descendente:** más difícil al principio del recorrido, se alivia según avanza (ej. varios ejercicios de aislamiento con polea alta).
- **En campana:** el pico de dificultad está en el rango medio (ej. curl de bíceps de pie clásico).

**Implicación práctica:** no trates todas las repeticiones de un ejercicio como equivalentes — identifica en qué tramo del recorrido se pierde tensión y, si el objetivo es maximizar el estímulo en ese músculo, prioriza variantes o implementos (poleas, máquinas con leva) que mantengan tensión donde el ejercicio libre la pierde.

## 2. Rango de movimiento e hipertrofia mediada por estiramiento

- Entrenar con el músculo en **posición larga (estirada) bajo carga** genera más tensión mecánica por fibra que en posición corta — la tensión mecánica es la señal principal de crecimiento.
- **ROM completo vs. parciales:** ambos producen hipertrofia similar en promedio, pero cuando los parciales se hacen en la **posición larga** (rango final del estiramiento), el resultado se inclina a su favor frente al ROM completo; los parciales en posición corta son inferiores.
- **Recomendación práctica:** para maximizar hipertrofia, prioriza el ROM completo o, si se usan parciales por fatiga/limitación articular, que sean en la posición estirada del músculo objetivo — nunca parciales en el rango corto como sustituto por comodidad.

## 3. Proximidad al fallo (RIR)

- La hipertrofia mejora al acercar las series al fallo, especialmente con cargas ligeras (donde hace falta más proximidad al fallo para generar tensión mecánica comparable a una carga pesada).
- La relación no es lineal: no hay evidencia de que llegar al **fallo absoluto** en cada serie sea superior a quedarse muy cerca (0-3 RIR) — y sí añade fatiga y riesgo, especialmente en gestos técnicos complejos.
- **Rango práctico por defecto: RIR 0-3.** Reservar el fallo absoluto para series aisladas (ej. última serie de un ejercicio de aislamiento), no como norma en cada serie de cada sesión.

## 4. Rango de repeticiones

- La hipertrofia se puede lograr en un espectro amplio de repeticiones (aproximadamente 6 a 30+) siempre que la proximidad al fallo sea similar — no existe un "rango mágico" único para crecer.
- **Implicación práctica:** esto da flexibilidad real para adaptar el rango de reps a la articulación, el equipo disponible o la preferencia del cliente, sin sacrificar resultado — útil para combinar con las restricciones de `seleccion-ejercicios-sustitucion-lesion.md` o `contraindicaciones-medicas.md` (ej. evitar cargas muy altas en una articulación sensible usando rangos altos de reps en su lugar, cerca del fallo).

## 5. Descansos entre series

- En personas entrenadas, descansos más largos (≥2 min) igualan o superan ligeramente a los descansos cortos para hipertrofia — probablemente porque permiten mantener el volumen/carga de la siguiente serie.
- En principiantes, la duración del descanso tiene un efecto mínimo sobre hipertrofia en general (con una posible excepción en cuádriceps, donde descansos más largos muestran un beneficio leve).
- **Recomendación práctica:** por defecto, 2-3 min en ejercicios estructurales/pesados; 60-90s es aceptable en ejercicios de aislamiento o cuando la disponibilidad de tiempo del cliente (`disponibilidad.duracion_sesion_preferida`, franja "30"/"45") lo exige.

## 6. Orden de ejercicios

- A diferencia de la fuerza (donde el primer ejercicio de la sesión gana más), el orden no muestra un efecto claro sobre la hipertrofia total de la sesión.
- **Recomendación práctica:** ordena por prioridad del objetivo del cliente (lo más importante primero, cuando hay más energía y calidad técnica disponible), no por convención rígida de "básicos antes que aislamiento".

## 7. Enfoque atencional (conexión mente-músculo)

- El enfoque interno (atención puesta en sentir el músculo trabajar) puede aumentar la activación muscular con cargas moderadas/bajas — pero pierde relevancia con cargas muy altas (~80%+ 1RM), donde el músculo ya recluta al máximo.
- El enfoque externo (atención puesta en mover la carga/el objetivo del movimiento) produce más fuerza por repetición — mejor cuando el objetivo de la serie es rendimiento, no hipertrofia pura.
- **Recomendación práctica:** sugiere enfoque interno en ejercicios de aislamiento con cargas moderadas orientados a hipertrofia; enfoque externo en ejercicios estructurales pesados. La evidencia a largo plazo es todavía limitada — no lo presentes como una certeza absoluta al cliente.

## 8. Selección de implemento: peso libre vs. máquina

- La hipertrofia es equivalente entre peso libre y máquina cuando el volumen y el esfuerzo se equiparan — no hay una superioridad intrínseca de uno sobre otro para crecer.
- El peso libre recluta más musculatura estabilizadora (mayor exigencia de equilibrio); la máquina permite aislar y llevar al músculo diana más cerca de su límite sin que el equilibrio sea el factor limitante.
- **Recomendación práctica (enfoque híbrido):** peso libre como base para patrones estructurales y coordinación; máquinas para aislar y rematar el músculo diana con seguridad, especialmente útil cuando `contraindicaciones-medicas.md` o `seleccion-ejercicios-sustitucion-lesion.md` piden minimizar exigencia de estabilización.

## 9. Progresión de volumen dentro del mesociclo (MEV → MAV → MRV)

`progresion-carga.md` cubre cómo sube la **carga** (peso) semana a semana. Esto cubre cómo debe subir el **volumen** (número de series) dentro de un mesociclo — la mitad que faltaba de "carga y volumen".

- **Volumen mínimo eficaz (MEV):** el número de series semanales por grupo muscular por debajo del cual no hay estímulo suficiente para crecer, solo para mantener. Orientativo: ≈6-10 series/semana/grupo muscular para la mayoría.
- **Volumen máximo adaptativo (MAV):** el rango donde se obtiene más crecimiento por el esfuerzo invertido, sin comprometer la recuperación. Orientativo: ≈10-20 series/semana/grupo muscular en la mayoría de intermedios (coincide con el rango base ya usado en `hipertrofia-recomposicion-corporal.md`).
- **Volumen máximo recuperable (MRV):** el punto a partir del cual el cliente deja de recuperar entre sesiones — pasarlo no da más crecimiento, da estancamiento o regresión. Varía mucho entre individuos (historial de entrenamiento, sueño, estrés, nutrición) — no es un número fijo, se detecta con las señales de `gestion-fatiga-deload.md`.

**Esquema de progresión dentro de un mesociclo:**
1. Empieza el mesociclo cerca del MEV o en la parte baja del MAV.
2. Añade 1-2 series por grupo muscular cada semana (o cada 2 semanas en intermedios/avanzados, que fatigan más rápido) según tolerancia — no todas las semanas de golpe.
3. Termina el mesociclo cerca del MRV estimado (o donde `gestion-fatiga-deload.md` detecte señales de fatiga, lo que llegue antes) y cierra con la semana de deload.

**Progresa una variable a la vez:** subir series y subir carga agresivamente en la misma semana acumula fatiga más rápido de lo previsto. Evita también el patrón contrario — bajar repeticiones semana a semana mientras sube la carga rápido (ej. series de 10 → 8 → 6 mismo ejercicio en pocas semanas) suele ser subóptimo frente a simplemente añadir series manteniendo el rango de reps.

> **Nivel de certeza:** el marco MEV/MAV/MRV es una herramienta práctica muy extendida en el sector (popularizada por Israetel/RP Strength), no un consenso académico cerrado — alguna revisión señala que la evidencia de que la fatiga se "acumula" de forma predecible sesión a sesión es todavía equívoca. Úsalo como heurística de programación, no como cifra exacta que se le presente al cliente como certeza absoluta.

## 10. Unilateral vs. bilateral

- El trabajo unilateral transfiere mejor a rendimiento unilateral (útil si el cliente tiene un objetivo funcional/deportivo con ese componente); el bilateral transfiere mejor a rendimiento bilateral.
- Para hipertrofia pura, ambos son válidos — la decisión depende más del objetivo funcional del cliente y de posibles asimetrías (ver `seleccion-ejercicios-sustitucion-lesion.md`) que de una superioridad para crecer.

## Conflictos conocidos con otros módulos

- **Con `hipertrofia-recomposicion-corporal.md`:** ese módulo aporta el contexto energético (déficit, viabilidad por nivel de entrenamiento); este módulo aporta el "cómo" a nivel de ejercicio y serie. Se activan siempre juntos cuando hay objetivo de hipertrofia.
- **Con `fuerza-maxima-potencia.md`:** comparten ejercicios ancla pero difieren en RIR objetivo y rango de repeticiones — se arbitra por el objetivo primario declarado (jerarquía universal, punto 3).
- **Con `progresion-carga.md`:** ese módulo cubre cómo progresa la **carga** (peso); este módulo cubre además cómo progresa el **volumen** (sección 9) y cómo se estructura cada serie (RIR, ROM, descansos). No progreses ambas variables (carga y volumen) de forma agresiva la misma semana.
- **Con `gestion-fatiga-deload.md`:** ese módulo decide cuándo llega el deload (por calendario o por señales de fatiga); este módulo decide cómo se llenó el volumen de las semanas hasta llegar ahí. El MRV estimado de la sección 9 no es un número fijo — se ajusta con las señales reales que detecta `gestion-fatiga-deload.md`.
- **Con `contraindicaciones-medicas.md` y `seleccion-ejercicios-sustitucion-lesion.md`:** ambos tienen precedencia — si limitan una articulación o gesto, este módulo se adapta (ej. usar rangos de reps más altos con menos carga en vez de cargas pesadas cerca de una articulación sensible) en vez de imponer su recomendación por defecto.

## Referencias

- Beardsley, C. — revisiones sobre curvas de fuerza y su efecto en hipertrofia regional.
- Warneke, K., et al. (2023). Revisión narrativa sobre fisiología de la hipertrofia mediada por estiramiento, *Sports Medicine*.
- Estudios sobre repeticiones parciales en posición larga vs. corta y ROM completo (PeerJ, 2025; comparaciones en individuos entrenados).
- Robinson, Z., et al. / meta-regresiones sobre proximidad al fallo, ganancia de fuerza e hipertrofia (2024).
- Schoenfeld, B. J. (2021). Re-examinación del continuo de repeticiones — *Sports*.
- Singer, Wolf, Generoso, Schoenfeld, et al. (2024). Meta-análisis bayesiano sobre duración del descanso entre series e hipertrofia.
- Meta-análisis sobre orden de ejercicios y su efecto en fuerza e hipertrofia (2020).
- Investigación sobre enfoque atencional interno/externo e hipertrofia (Strength & Conditioning Journal, 2016 y estudios posteriores).
- Meta-análisis sobre entrenamiento con peso libre vs. máquinas en fuerza, hipertrofia y salto (2023).
- Israetel, M., et al. (RP Strength) — marco práctico de volume landmarks (MEV/MAV/MRV).
- *Mesocycle Progression in Hypertrophy: Volume Versus Intensity*, Strength & Conditioning Journal (2020).
