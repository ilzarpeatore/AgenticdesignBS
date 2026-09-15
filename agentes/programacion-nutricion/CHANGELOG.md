# Changelog — Asistente de Programación de Nutrición

## v0.1.0 — 2026-09-15

Primer borrador. Mismo marco arquitectónico que `agentes/programacion-entrenamiento/` (base de conocimiento modular, sin encasillar al cliente en una dieta fija), adaptado a nutrición y coordinado con el entrenamiento real del cliente.

- **Nuevo `system-prompt.md`:** rol y alcance (qué NO decide: ni entrenamiento, ni diagnóstico, ni suplementación de riesgo), Paso 0 (selección de módulos multi-etiqueta), Paso 1 con cribado de alergias obligatorio primero y coordinación explícita con el Asistente de Programación de Entrenamiento (Multi-Agent Collaboration — sequential handoff, cap. 7: lee `perfil-cliente.schema.json` y el razonamiento del Productor de ese agente en vez de regenerar el entrenamiento), Paso 2 con razonamiento CoT + consulta de recetario (Tool Use, cap. 5, pendiente de recetario real), jerarquía universal de conflictos, y una sección 9 explícita de lo que todavía no existe (recetario real, formato de salida real, validador determinista, log de nutrición) para no fingir que está resuelto.
- **Nuevo módulo `alergias-intolerancias.md`:** primer módulo real, capa de seguridad transversal. Aplica directamente la lección del intake de lesiones del otro agente (bloqueo duro ante datos de seguridad ambiguos, no una nota a mejorar después) — esta vez desde el primer borrador, no tras un incidente real. Sin deep-search de evidencia clínica todavía, declarado explícitamente como pendiente.
- **`agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json` (v0.9.0 de ese agente):** `restricciones_dieteticas` pasa de lista de texto libre a objetos estructurados con `tipo` y `severidad` obligatoria si `tipo: alergia` — mismo patrón que `restricciones_salud`, para que el campo compartido llegue ya bien formado a este agente en vez de heredar la ambigüedad.
- **Nuevo `esquemas/perfil-nutricional.schema.json`:** solo los campos que no viven ya en el esquema compartido (objetivos nutricionales, gustos/aversiones, disponibilidad para cocinar, presupuesto, nº de comidas) — no duplica `cliente_id`, `restricciones_dieteticas` ni `disponibilidad`/`actividad_principal` de entrenamiento.

**Pendiente (declarado en la sección 9 del `system-prompt.md`, no oculto):**
- Recetario real contra el que el Paso 2 pueda buscar (equivalente a `catalogo-ejercicios.xlsx`).
- Formato de salida real hacia algún sistema de producción — no existe todavía, se define cuando haya un caso real que lo necesite.
- Validador determinista (Paso 3) — por ahora la checklist mecánica es prosa, igual que le pasó al agente de entrenamiento antes de `validador/validar_programa.py`.
- Deep-search de evidencia real para módulos de contenido (macros, timing, recomposición nutricional) — todavía no se ha escrito ninguno más allá de la capa de seguridad.
