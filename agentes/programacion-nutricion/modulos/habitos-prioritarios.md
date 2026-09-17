# Módulo: Hábitos prioritarios

**Tipo:** General — síntesis final, no una capa de contenido nutricional nueva
**Se activa cuando:** siempre — después de fijar el plan de comidas (Paso 2), antes del Paso 3
**Versión:** 0.1.0 · **Última actualización:** 2026-09-17
**Procedencia:** ítem 2.7 de `docs/TAREAS_PENDIENTES.md`, construido a partir del caso real de Borja (guideline compartido por el usuario) — su sección 6, "Bloque de hábitos prioritarios", es exactamente lo que este módulo formaliza: no una dieta más detallada, sino una lista corta y ordenada de qué cambiar primero para que el plan funcione de verdad.

## Por qué existe este módulo

El caso real mostró algo que ni el plan de macros ni el recetario resuelven por sí solos: Borja tenía un plan nutricional coherente, pero su entorno real (turno de noche, 5 adultos con hábitos distintos en casa, hambre a las 3-4am) hacía que ese plan fallara en la práctica. Los cinco hábitos de ese caso no eran una dieta alternativa — eran los puntos de fricción concretos que, resueltos, desbloqueaban el plan ya diseñado. Tres de los cinco eran estrictamente nutricionales (proteína mínima, snack en una ventana horaria crítica, superávit calórico mínimo); dos eran hábitos de estilo de vida sin relación directa con la comida (regularidad del sueño, pasos/NEAT), pero con impacto directo y medible sobre el objetivo nutricional declarado (recomposición corporal). Este módulo cubre ambos tipos — no lo limites a temas de comida.

## Regla operativa

1. **Cuándo generarlo:** siempre, en todo ciclo de generación — no es opcional ni depende de un objetivo concreto. Un cliente sin ningún punto de fricción real solo tendrá hábitos de mantenimiento (ej. "sigue registrando en HubFit"), pero la sección no se omite.
2. **De dónde salen los candidatos a hábito:** no se inventan genéricos ("bebe más agua", "duerme bien") — cada hábito debe estar anclado a un dato concreto de este cliente:
   - `contexto_vida` del perfil compartido (horario laboral, sueño, estrés) — ver `esquemas/perfil-cliente.schema.json` del agente de entrenamiento.
   - `observaciones_coach` de los checkpoints físicos (`checkpoint-fisico.schema.json`) — si el coach ya identificó una causa de estancamiento, ese es el candidato de mayor prioridad, no uno nuevo inventado desde cero.
   - `adherencia_real`/`correccion_manual` de ciclos anteriores de `log-nutricion.schema.json` — qué falló en la práctica, no solo qué faltaba en el plan.
   - `gustos_y_aversiones.descripcion_dia_tipo` del `perfil-nutricional.schema.json` — dónde está el patrón real de comidas del cliente hoy, para detectar el punto de fricción (ej. una ventana horaria concreta donde el cliente ya suele fallar).
3. **Máximo 3-5 hábitos, sin excepción.** Más que eso deja de ser "prioritario" — es la lista completa de todo lo que se podría mejorar, que es justo lo que este módulo no debe ser. Si hay más de 5 candidatos válidos, prioriza y descarta el resto para el siguiente ciclo — no los metas todos "por si acaso".
4. **Orden por impacto potencial, no por facilidad ni por orden cronológico del día.** Como en el caso real: si el bloqueo principal es nutricional, los primeros hábitos son nutricionales, aunque un hábito de sueño sea "más fácil" de anotar. Explicita el criterio de orden en el propio razonamiento (Paso 2 del `system-prompt.md`).
5. **Cada hábito lleva exactamente dos partes, ninguna es opcional:**
   - **Por qué importa:** la explicación causal específica de este cliente, con sus propios números cuando existan (ej. "con 68 kg y 54.6 kg de masa muscular, necesitas 140-150g de proteína/día; hoy solo lo alcanzas de forma irregular"). Una justificación genérica de manual no cumple este punto.
   - **Cómo implementarlo:** instrucción concreta y de fricción mínima, no una recomendación abstracta. Preferir anclar el hábito nuevo a uno que el cliente ya tiene (ej. "prepararlo antes de salir de casa", "vincúlalo a que ya vas al gym") — es más probable que se sostenga que un hábito aislado sin ancla.
6. **Hábitos de estilo de vida sin relación directa con la comida son válidos** (sueño, pasos/NEAT, gestión del estrés) siempre que su "por qué importa" conecte explícitamente con el objetivo nutricional/de composición corporal declarado — si no hay esa conexión explícita, no es un hábito prioritario de este módulo, es contenido que no le corresponde a este agente.
7. **Persistencia:** guarda la lista generada en el campo `habitos_prioritarios` de la entrada de `log-nutricion.schema.json` de este ciclo (ver esquema). En el siguiente ciclo, el Paso 1 (memoria del cliente) debe leer los hábitos del ciclo anterior y preguntar/valorar su adherencia antes de generar una lista nueva — no se regenera desde cero cada vez como si el ciclo anterior no hubiera pasado (mismo criterio que el resto de memoria episódica).

## Guardrail

No uses este módulo para reintroducir contenido de seguridad (alergias, cribado médico) — eso ya lo bloquea `alergias-intolerancias.md`/`contraindicaciones-medicas.md` antes de llegar aquí. Este módulo asume que el plan ya es seguro y trata exclusivamente de qué lo hace sostenible en la vida real del cliente.

## Dónde no vive esto

`meal_plan_templates`/`daily_plans` (Bckbs) no tienen ninguna columna para una lista de hábitos — no es una comida ni una receta, y no se fuerza a que lo sea. Esta sección queda en el borrador que revisa el humano (Paso 5) y en la memoria episódica (`log-nutricion.schema.json`), no en ninguna tabla de Bckbs. Ver `agentes/programacion-nutricion/formato-salida/entrega-bckbs.md`.
