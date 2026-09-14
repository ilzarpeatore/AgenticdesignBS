# Módulo: Periodización por calendario

**Tipo:** General, condicional
**Se activa cuando:** NO existe `fecha_evento` en el perfil del cliente (objetivo sin competición ni fecha límite: recomposición corporal, mantenimiento, fuerza general). Si en algún momento aparece una fecha, el módulo `periodizacion-orientada-evento.md` toma el control. Esta comprobación es determinista (existe el dato o no existe) — no requiere que el Productor razone sobre ello, solo que lo consulte.
**Versión:** 0.2.0 · **Última actualización:** 2026-09-14
**Procedencia:** formalización de la jerarquía de periodización descrita en `docs/roadmap.md` — no existía todavía como módulo independiente.

## Regla operativa

Estructura jerárquica en 5 niveles, cada uno con lo que se fija al crear el plan y lo que se recalcula con el progreso real:

| Nivel | Horizonte | Se fija al crear el plan | Se recalcula |
|---|---|---|---|
| Macrociclo | 6 meses | Objetivo(s), restricciones, módulos activos | — |
| Bloque (mesociclo) | 3 meses × 2 | Énfasis del bloque, según los módulos de objetivo activos | Al cerrar cada bloque, con el resultado real |
| Mes | 1 mes × 3 por bloque | Meta medible del mes | Progresión mes a mes dentro del bloque |
| Semana (microciclo) | 1 semana × ~4 por mes | `reglas_programa` del cliente | Carga, volumen y RPE de cada ejercicio |
| Sesión / ejercicio | Día a día | Ejercicios básicos fijos | Accesorios (rotan según regla) y ajuste fino |

**Cadencia de generación recomendada:** no generar los 6 meses al detalle de una sola vez — un plan escrito hoy para dentro de 5 meses no puede saber cómo respondió realmente el cliente. Generar un **esqueleto macro** una vez (objetivos por bloque y mes) y el **detalle semana a semana** justo antes de que empiece, informado por la adherencia y el feedback real del ciclo anterior (memoria episódica, `historial_ciclos`).

Cada módulo de objetivo (ej. `hipertrofia-recomposicion-corporal.md`) rellena este esqueleto con sus propios parámetros de duración de mesociclo, frecuencia de deload y criterios de progresión — este módulo solo aporta la estructura, no el contenido.

## Conflictos conocidos con otros módulos

- **Con `periodizacion-orientada-evento.md`:** mutuamente excluyentes en un momento dado — decide `fecha_evento`. Si el cliente no tenía fecha y luego la consigue (ej. decide competir), se cambia de módulo sin reiniciar el macrociclo desde cero: se reprograma solo lo necesario.
- **Con `gestion-fatiga-deload.md`:** el deload se ubica naturalmente al cierre de cada mes o bloque, salvo que las señales de fatiga pidan adelantarlo.
