# Módulo: Periodización orientada a evento

**Tipo:** General, condicional
**Se activa cuando:** existe una `fecha_evento` en el perfil del cliente (carrera, competición, examen físico, o cualquier otra fecha objetivo). Mientras está activo, sustituye a la periodización por calendario fijo. La comprobación es determinista (Routing basado en regla, cap. 2) — no una decisión que el Productor deba razonar cada vez.
**Versión:** 0.2.0 · **Última actualización:** 2026-09-14
**Procedencia:** adaptado de la sección 3.7 del agente original de fuerza/pliometría para media maratón — generalizado: la lógica de fases no es específica de correr, es específica de tener una fecha.

## Regla operativa

**Fases del bloque (ajustar duración según semanas disponibles):**

1. **Adaptación anatómica/técnica (2-4 semanas, si el cliente es nuevo en fuerza o pliometría):** cargas moderadas, técnica como prioridad, pliometría de bajo impacto únicamente. Se puede acortar o saltar si el cliente ya tiene base sólida.
2. **Fuerza máxima (4-6 semanas):** cargas altas (80-90% 1RM), bajas repeticiones (3-6); la pliometría se mantiene en volumen de mantenimiento, no como foco.
3. **Fuerza-potencia/conversión (4-6 semanas):** se reduce ligeramente la carga máxima, se introduce el componente de velocidad de ejecución y pliometría de mayor exigencia.
4. **Taper (última 1-2 semanas antes del evento):** reducción marcada de volumen, intensidad relativa baja-moderada solo para preservar activación neuromuscular; eliminar estímulos de alto impacto o cercanos al fallo en los últimos 5-7 días.
5. **Semana del evento:** solo trabajo muy ligero de activación, nunca un estímulo nuevo ni de alta fatiga.

**Reglas de encaje según semanas restantes hasta el evento:**

- **<4 semanas:** no iniciar fase nueva de fuerza máxima; priorizar mantenimiento de lo ya construido + taper progresivo.
- **4-8 semanas:** fuerza máxima corta seguida de fuerza-potencia y taper.
- **>8 semanas:** las 4 fases completas caben con margen; si sobran semanas, alargar la fase de fuerza máxima o repetir un segundo ciclo fuerza máxima→potencia — nunca alargar el taper.
- **Sin fecha todavía:** queda en fase de adaptación/fuerza máxima de forma indefinida (usar periodización por calendario mientras tanto) hasta que exista fecha.

## Conflictos conocidos con otros módulos

- **Con `gestion-fatiga-deload.md`:** ver arriba — el taper absorbe la función del deload en el tramo final.
- **Con cualquier módulo de fuerza (`fuerza-maxima-potencia.md`, `pliometria-rigidez-tendinosa.md`):** el taper prevalece sobre la progresión de carga en el tramo final (jerarquía universal, puntos 1 y 3).
