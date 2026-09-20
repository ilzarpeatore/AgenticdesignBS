# Módulo: Periodización por calendario

**Tipo:** General, condicional
**Se activa cuando:** NO existe `fecha_evento` en el perfil del cliente (objetivo sin competición ni fecha límite: recomposición corporal, mantenimiento, fuerza general). Si en algún momento aparece una fecha, el módulo `periodizacion-orientada-evento.md` toma el control. Esta comprobación es determinista (existe el dato o no existe) — no requiere que el Productor razone sobre ello, solo que lo consulte.
**Versión:** 0.3.0 · **Última actualización:** 2026-09-20
**Procedencia:** formalización de la jerarquía de periodización descrita en `docs/roadmap.md` — no existía todavía como módulo independiente. v0.3.0: la revisión de un macrociclo real (cliente de hipertrofia, Be Stronger) expuso que la tabla original fijaba en cifras concretas (6 meses, 2 bloques de 3 meses, ~4 semanas/mes) algo que el propio texto ya decía que debía decidir cada módulo de objetivo por cliente — se corrige la tabla para dejar de contradecir esa intención. Decisión explícita del usuario: el número de mesociclos y de semanas por mesociclo depende del cliente (objetivo, nivel, disponibilidad), nunca una cifra fija de plantilla; el contenido metodológico concreto de ese caso real (clasificación de ejercicios ancla/variable/nuevo, patrones de reps, esquema de RIR, regla de progresión, deload, MEV/MRV) es específico de ese cliente y no se traslada a este ni a ningún otro módulo — es un servicio individualizado.

## Regla operativa

Estructura jerárquica en 4 niveles. Ninguna duración de esta tabla es una cifra fija de plantilla — el objetivo, el nivel del cliente y los módulos de objetivo activos determinan cuántos mesociclos tiene el macrociclo y cuántas semanas dura cada uno:

| Nivel | Horizonte | Se fija al crear el plan | Se recalcula |
|---|---|---|---|
| Macrociclo | Duración total del objetivo del cliente — variable, la determina el caso concreto | Objetivo(s), restricciones, módulos activos, nº de mesociclos previsto | — |
| Bloque (mesociclo) | Nº de semanas variable por cliente — lo fija el módulo de objetivo activo (p.ej. `hipertrofia-recomposicion-corporal.md`, cadencia de deload de `gestion-fatiga-deload.md`); el nº total de mesociclos del macrociclo también depende del cliente | Énfasis del bloque, duración en semanas, semana(s) de deload | Al cerrar cada bloque, con el resultado real |
| Semana (microciclo) | 1 semana, tantas como dure el mesociclo activo | `reglas_programa` del cliente, progresión semana a semana (carga/RIR/volumen) | Carga, volumen y RPE de cada ejercicio, según adherencia real |
| Sesión / ejercicio | Día a día | Ejercicios básicos fijos | Accesorios (rotan según regla) y ajuste fino |

**Cadencia de generación:** el Productor puede generar el detalle semana a semana de todo el macrociclo en un único pase (progresión de carga/RIR y notas técnicas completas para cada mesociclo) cuando el caso lo justifique — no está obligado a limitarse a un esqueleto macro más detalle mes a mes. Generar el detalle completo por adelantado no lo convierte en un contrato fijo: sigue siendo un borrador vivo que se revisa mesociclo a mesociclo con la adherencia y el feedback real del anterior (memoria episódica, `historial_ciclos`) antes de entregarse — un plan detallado hoy para dentro de varios meses no deja de necesitar ese ajuste solo por estar ya escrito.

Cada módulo de objetivo (ej. `hipertrofia-recomposicion-corporal.md`) rellena este esqueleto con sus propios parámetros de duración de mesociclo, frecuencia de deload y criterios de progresión — este módulo solo aporta la estructura, no el contenido.

## Conflictos conocidos con otros módulos

- **Con `periodizacion-orientada-evento.md`:** mutuamente excluyentes en un momento dado — decide `fecha_evento`. Si el cliente no tenía fecha y luego la consigue (ej. decide competir), se cambia de módulo sin reiniciar el macrociclo desde cero: se reprograma solo lo necesario.
- **Con `gestion-fatiga-deload.md`:** el deload se ubica naturalmente al cierre de cada mesociclo, salvo que las señales de fatiga pidan adelantarlo.
