# Cómo alimentar de conocimiento a los agentes

Este documento es el proceso a seguir cada vez que tengas contenido científico/teórico nuevo (un estudio, un artículo, tus propias notas de formación) que quieras que el Asistente de Programación de Entrenamiento use.

## Paso 1 — Decide dónde va

- ¿Es sobre un tema que **ya tiene módulo** (`agentes/programacion-entrenamiento/modulos/`)? → va ahí, como una regla más.
- ¿Es sobre un **tema nuevo** (un deporte, una población, un objetivo que hoy no cubre ningún módulo)? → módulo nuevo, misma plantilla (ver Paso 3).
- ¿Es sobre **cómo debe comportarse el agente en general** (tono, límites de alcance, qué preguntar siempre)? → va en `system-prompt.md`, no en un módulo.

## Paso 2 — Conviértelo en regla operativa, nunca lo pegues tal cual

Esta es la disciplina más importante de todo el sistema, heredada de tu propio documento original:

- ❌ Mal: *"Un estudio de Llanos-Lagos et al. (2024) encontró mejoras en economía de carrera con cargas altas."*
- ✅ Bien: *"Prioriza cargas altas (3-6 reps, 80-90% 1RM) en ejercicios estructurales como eje del bloque de fuerza — mejoras pequeñas-moderadas en economía de movimiento frente a rangos de hipertrofia."*

La cita queda como referencia en "Procedencia" si quieres, pero la sección "Regla operativa" tiene que ser directamente aplicable por el agente sin que tenga que interpretar un resumen narrativo.

## Paso 3 — Si es un módulo nuevo, usa esta plantilla exacta

```markdown
# Módulo: [nombre]

**Tipo:** General | Específico
**Se activa cuando:** [condición concreta y verificable desde perfil_cliente]
**Versión:** 0.1.0 · **Última actualización:** [fecha]
**Procedencia:** [de dónde sale este conocimiento]

## Regla operativa
- [reglas aplicables, con números/condiciones concretas]

## Conflictos conocidos con otros módulos
- **Con `otro-modulo.md`:** [cómo se resuelve la tensión, o referencia a la jerarquía universal]
```

Añádelo también a la tabla de módulos en `docs/roadmap.md`.

## Paso 4 — Revisa conflictos con módulos existentes

Pregúntate: ¿esta regla nueva puede chocar con una regla de otro módulo que se active a la vez? Si sí, anótalo en "Conflictos conocidos" de **ambos** módulos. Si el conflicto es de un tipo que la jerarquía universal (`system-prompt.md`, sección 4) no resuelve todavía, no lo decidas sobre la marcha — es una decisión de diseño, tráela a una sesión de trabajo.

## Paso 5 — Sube versión y changelog

Cada módulo lleva su propia versión en la cabecera (`0.1.0` → `0.2.0` si añades contenido sustancial, `0.1.1` si es un matiz menor). Añade también una línea al `CHANGELOG.md` del agente.

## Paso 6 — Commit y push

Esto es lo que de verdad "alimenta" al agente. Hasta que el cambio no está en `main`, no existe para el sistema — ni para ti en la próxima sesión, ni para n8n cuando llegue M1.

## Cómo hacerlo en la práctica

**Conmigo:** pégame el contenido en bruto (el estudio, el artículo, tus notas) en cualquier sesión de Claude Code sobre este repo. Identifico dónde encaja, te propongo la regla operativa ya redactada, reviso conflictos y hago el commit.

**Tú solo, sin mí:** abre el archivo del módulo en GitHub (icono de lápiz, arriba a la derecha del archivo), edita directamente en el navegador siguiendo la plantilla, y confirma el commit. No hace falta terminal ni conocimientos técnicos.

## Importante en Mesociclo 0: esto no llega solo al agente todavía

Un commit actualiza la fuente de verdad, pero en M0 no hay ninguna automatización leyendo este repo. El "agente" en la práctica es el contenido que pegas a mano en tu Proyecto de Claude (o similar) cuando vas a programar a un cliente. Así que después de un cambio importante:

- O actualizas tú el contenido pegado en tu proyecto activo con la versión nueva del módulo,
- O me pides que te arme el bloque de contexto actualizado (marco fijo + módulos relevantes para ese cliente) para que lo copies.

Cuando llegue Mesociclo 1 con n8n, este último paso se vuelve automático: n8n lee el repo directamente en cada ejecución y este paso manual desaparece.
