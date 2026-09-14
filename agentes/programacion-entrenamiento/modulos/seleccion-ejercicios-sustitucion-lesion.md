# Módulo: Selección de ejercicios y sustitución por lesión

**Tipo:** General
**Se activa cuando:** existe una restricción física declarada por el cliente clasificada como `lesion_localizada` (ver `contraindicaciones-medicas.md` para las categorías `contraindicacion_relativa`/`contraindicacion_absoluta`, que se resuelven antes y de forma distinta), o una limitación de material/instalaciones. Condición casi universal — revisar en cada intake.
**Versión:** 0.2.0 · **Última actualización:** 2026-09-14
**Procedencia:** adaptado de los "principios generales" de la sección 3.4 del agente original de fuerza/pliometría para media maratón.

## Regla operativa

- Ante dolor, lesión o limitación: identifica (a) el patrón de movimiento, (b) el vector de resistencia y (c) el rango donde ocurre el dolor o la limitación. Sustituye manteniendo (a) y (b), evitando (c). **No elimines el patrón completo** salvo indicación explícita — mantener el patrón y cambiar la ejecución suele ser suficiente.
- Ante falta de material: mancuernas, bandas o el propio peso corporal permiten mantener casi cualquier patrón (empuje, tracción, bisagra de cadera, sentadilla, unilateral) cambiando solo la herramienta — no es motivo para vaciar el programa de patrones clave.
- Ante información vaga sobre una molestia ("me duele X a veces"): **bloqueante, no un matiz a resolver mientras se genera.** Exige antes de programar nada: qué gesto la provoca (`gesto_doloroso`), si es aguda/en recuperación/crónica controlada (`fase`), y si empeora con la actividad principal o con impacto (`empeora_con_actividad_o_impacto`) — campos obligatorios de `esquemas/perfil-cliente.schema.json` para toda `restriccion_salud` de categoría `lesion_localizada`. **Nunca decidas con datos insuficientes**, ni hacia el lado conservador (excluir de más) ni hacia el permisivo (adaptar algo que debía excluirse).

## Guardrail duro

Ante una lesión declarada con `fase: aguda`: excluye por completo el grupo muscular o patrón de movimiento afectado de toda la programación, y exige `autorizacion_profesional` antes de continuar. No lo "adaptas con cuidado" — lo excluyes y marcas el caso para revisión humana explicando qué excluiste y por qué. `en_recuperacion` y `cronica_controlada` sí admiten adaptación (mantener patrón, evitar el rango doloroso, regla operativa de arriba) — pero solo cuando `fase` está declarada explícitamente, nunca por defecto ante una descripción ambigua.

**Lección de un caso real:** una lesión de manguito rotador declarada sin `fase` ni `gesto_doloroso` forzó al Productor a decidir entre adaptar y excluir por juicio propio, en tensión directa con este guardrail — exactamente el escenario que estos campos obligatorios existen para evitar.

## Conflictos conocidos con otros módulos

- **Con cualquier módulo de contenido:** esta regla tiene prioridad 1 de la jerarquía universal (seguridad) sobre lo que pida cualquier otro módulo — incluida la progresión de carga o las prioridades de ejercicio de un módulo específico como `running-economia-carrera.md`.
- **Con `contraindicaciones-medicas.md`:** ese módulo se consulta primero y tiene precedencia. Si una restricción de salud es una contraindicación (relativa o absoluta), no se gestiona aquí como sustitución de ejercicio — se gestiona allí como bloqueo de la programación hasta autorización, o derivación directa.
