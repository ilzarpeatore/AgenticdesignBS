# Módulo: Running / economía de carrera

**Tipo:** Específico
**Se activa cuando:** el cliente corre o compite en fondo/medio fondo y aporta su plan/volumen de carrera actual como dato de entrada. Este módulo **no diseña** el plan de carrera en sí (series, ritmos, kilometraje, distribución de intensidades) — se asume como dato de entrada.
**Versión:** 0.1.0 · **Última actualización:** 2026-09-14
**Procedencia:** agente original completo, especializado en fuerza/pliometría para corredores de media maratón (v1.0, 2026-09-07) — la parte específica de running tras separar los principios generales en sus propios módulos.

## Regla operativa

### Entrenamiento concurrente y efecto interferencia

- El "efecto interferencia" clásico (Hickson, 1980) se matiza en revisiones recientes (Schumann et al.): no se encontró que la frecuencia semanal, el estado de entrenamiento, la edad ni el orden de las sesiones interfirieran de forma relevante en fuerza máxima o hipertrofia.
- El efecto interferencia sí es más consistente en **potencia y fuerza explosiva** (Stronger by Science, análisis 2024) — justo las cualidades que se priorizan en `fuerza-maxima-potencia.md` y `pliometria-rigidez-tendinosa.md`. Por eso hay que ser más conservador con el orden y el espaciado de las sesiones que lo que sería necesario para un objetivo de solo fuerza máxima.
- **Orden dentro de una misma sesión:** si carrera y fuerza se hacen el mismo día, entrenar fuerza/potencia **antes** de correr cuando el objetivo prioritario del día sea la fuerza/potencia; si el objetivo prioritario del día es la calidad de la carrera (tirada larga, serie de intensidad), la fuerza se programa muy espaciada o en otro día.
- **Espaciado mínimo si se hace el mismo día:** idealmente >3 horas entre sesión de carrera y de fuerza (revisión Frontiers, 2025).
- **Frecuencia semanal:** 2 sesiones/semana de fuerza+pliometría cubre a la mayoría de corredores recreativos de media maratón; 3/semana es viable en fases de menor volumen de carrera o en corredores más avanzados, siempre que no comprometa la recuperación para las sesiones de carrera clave.
- **Días no consecutivos:** preferir separar las sesiones de fuerza/pliometría entre sí y respecto a las sesiones de carrera de alta exigencia.

### Prioridades de selección de ejercicios (por relevancia para el gesto de carrera)

1. **Unilateral / tren inferior** — la carrera es una sucesión de apoyos monopodales: zancada búlgara, step-up, zancada, sentadilla a una pierna. Más peso relativo que en un programa general bilateral.
2. **Bisagra de cadera / cadena posterior** — peso muerto rumano, hip thrust, buenos días: la extensión de cadera es el motor principal de la propulsión en carrera.
3. **Tríceps sural / complejo aquíleo-plantar** — elevaciones de talón (bilaterales, unilaterales, con rodilla flexionada para el sóleo), trabajo isométrico cuando esté indicado (ver `pliometria-rigidez-tendinosa.md`).
4. **Core/tronco en función anti-rotación y anti-extensión** — plancha, pallof press, deadbug: transferencia de fuerza y control pélvico durante el apoyo.
5. **Sentadilla y patrones bilaterales de tren inferior** — ejercicio ancla de fuerza máxima, pero no el único ni el principal estímulo.
6. **Tren superior** — papel secundario; no debe restar recursos de recuperación a las prioridades 1-4.

> Nota abierta: varias de estas prioridades (unilateral, bisagra de cadera) probablemente también aplican a otros deportes de campo (fútbol, por ejemplo). Al escribir el módulo de fútbol, evaluar si parte de esta lista debería extraerse a un módulo general de "prioridades por demanda de tren inferior en deportes de impacto/cambio de dirección" en vez de quedar duplicada o encerrada aquí.

### Casos frecuentes en corredores

- **Dolor en la banda iliotibial** → revisar si aparece con sentadilla profunda o zancada lateral; suele tolerarse mejor el trabajo sagital (zancada frontal, step-up) mientras se gestiona.
- **Fascitis plantar / dolor en el arco** → limitar temporalmente la pliometría de alto impacto y priorizar trabajo isométrico/de fuerza para el tríceps sural y la musculatura intrínseca del pie; reintroducir impacto de forma progresiva.
- **Molestia lumbar en la bisagra de cadera** → antes de sustituir el patrón, revisar la neutralidad de columna; si persiste con técnica correcta, el hip thrust guiado reduce la exigencia de estabilización lumbar manteniendo la extensión de cadera.

## Preguntas de intake adicionales que activa este módulo

- Fecha de la carrera objetivo (si no la hay, usar periodización por calendario mientras tanto — ver `periodizacion-orientada-evento.md`).
- Plan/volumen de carrera actual: días de carrera/semana, kilometraje semanal aproximado, distribución de intensidades si se conoce.

## Conflictos conocidos con otros módulos

- **Con `pliometria-rigidez-tendinosa.md`:** este módulo pide más conservadurismo en espaciado que el que Pliometría pediría en aislado (ver "entrenamiento concurrente" arriba).
- **Con `periodizacion-orientada-evento.md`:** la fecha objetivo suele ser la fecha de la carrera; coordina el deload de fuerza con las semanas de descarga del plan de carrera si el cliente las tiene.
