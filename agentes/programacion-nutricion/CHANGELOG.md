# Changelog — Asistente de Programación de Nutrición

## v0.2.0 — 2026-09-15

Deep search basado en ciencia para las tres piezas de contenido más básicas, siguiendo el proceso de `CONTRIBUTING.md` (evidencia convertida a regla operativa, no cita narrativa).

- **Nuevo módulo general `necesidades-energeticas-macronutrientes.md`:** estimación de TDEE (Mifflin-St Jeor + factor de actividad), rangos de proteína por contexto (ISSN Position Stand: 1.4-2.0 g/kg general, 1.6-2.0 fuerza, 1.0-1.6 resistencia, 2.3-3.1 en déficit), mínimo de grasa por salud hormonal (0.5-1 g/kg, ≥20% calorías), carbohidrato por diferencia, y el umbral de seguridad de disponibilidad energética (RED-S: <30 kcal/kg de masa libre de grasa/día = baja disponibilidad) como guardrail duro para cualquier déficit. Nota breve sobre micronutrientes de riesgo (hierro, vitamina D, calcio, fibra) como señal de alerta, no diagnóstico.
- **Nuevo módulo general `timing-nutricional-entrenamiento.md`:** desmonta el mito de la "ventana anabólica" estrecha (Aragon & Schoenfeld 2013: ventana real de 4-6h, el total diario de proteína domina sobre el timing exacto), distribución de proteína por toma (~0.4 g/kg, mínimo ~0.25 g/kg para estímulo relevante), periodización simple de carbohidrato por tipo de día (entrenamiento vs. descanso, coordinado con lo que el agente de entrenamiento indique para esa semana), e hidratación (ACSM: pre/durante/electrolitos).
- **Nuevo módulo específico `recomposicion-corporal-nutricion.md`:** implementación numérica de lo que `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento) ya usa como referencia — tamaño de déficit (300-500 kcal/día), proteína en déficit (2.3-3.1 g/kg), estructura práctica de diet breaks (1-2 semanas a mantenimiento recalculado al peso actual, cada 4-10 semanas) y refeeds (1-3 días, +carbohidrato, cada 7-14 días), coordinados con el deload de entrenamiento. Cross-referencia explícita en vez de duplicar cifras ya fijadas del lado de entrenamiento.
- **`system-prompt.md` (v0.2.0):** sección 9 actualizada para reflejar el estado real de contenido — ya no dice "solo existe la capa de seguridad".

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
