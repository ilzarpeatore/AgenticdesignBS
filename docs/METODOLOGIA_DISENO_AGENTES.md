# Metodología de diseño de agentes — orden de trabajo

**Última actualización:** 2026-09-27

Este documento no es teoría abstracta — es el proceso real que se siguió para diseñar los 5 agentes existentes (`agentes/`), extraído a propósito para que el diseño del siguiente sea igual de riguroso y no dependa de que quien lo haga se acuerde de todo. Si una sesión de Claude Code en consola va a diseñar el próximo agente del organigrama (`docs/ORGANIGRAMA_AGENTES.md`), este es el orden a seguir.

---

## Fase 0 — Confirmar que toca construir el siguiente, y cuál

No se añade un agente operativo nuevo por completar el organigrama. Antes de elegir:

1. Comprobar en `docs/TAREAS_PENDIENTES.md` y `docs/roadmap.md` que los agentes ya diseñados no tienen gaps críticos abiertos que deberían cerrarse primero.
2. Elegir el candidato siguiendo el criterio ya fijado en `docs/ORGANIGRAMA_AGENTES.md`: **priorizar por impacto en tiempo ahorrado real, no por completitud del organigrama.** En igualdad de condiciones, el candidato que reutiliza infraestructura ya montada (misma área de negocio que un agente existente) es más barato de construir y de mantener que uno que abre un área nueva.
3. Esto es una decisión del usuario, no una que se toma sola: presentar 2-3 candidatos reales del organigrama con una recomendación clara y el porqué (`AskUserQuestion`, con la opción recomendada primero) — así se decidió Onboarding sobre los otros 9 candidatos restantes.

## Fase 1 — Investigar el código real ANTES de diseñar nada

Esta es la regla más repetida y la que más ha evitado trabajo perdido en todo el proyecto: **nunca se inventa una integración, se comprueba.**

1. Buscar en el backend real (Bckbs) qué ya existe para lo que el agente necesitaría: modelos, columnas, endpoints, servicios, comandos artisan. No asumir que hace falta construir algo sin haberlo comprobado con `grep`/lectura de código real.
2. Cuando algo falta de verdad, documentarlo como **"gap real, documentado, no construido todavía"** — no se cierra por adelantado sin que el volumen real lo justifique o el usuario lo pida explícitamente. Ejemplos reales: la búsqueda por teléfono se documentó como gap en el diseño inicial de Soporte y se construyó semanas después, cuando el usuario pidió profundizar en ello — no antes.
3. Revisar los agentes hermanos ya diseñados en la misma área para **reutilizar, no duplicar**: tono, validación determinista, esquemas de log, herramientas. Un agente nuevo en la misma área (ej. Onboarding junto a Soporte) debería poder señalar "comparte X con el agente Y" en la mayoría de sus filas de herramientas, no reinventar cada una.

## Fase 2 — Investigar la práctica real del sector, no inventar desde cero

Cuando el diseño toca una decisión de "cómo debería funcionar esto en la vida real" (un check-in, un flujo de bienvenida, un criterio de retención) — no se diseña desde la intuición, se investiga primero:

1. `WebSearch` sobre cómo lo hacen los que más facturan en ese nicho concreto (no genérico de "SaaS" o "atención al cliente" — el nicho real: coaching online, entrenamiento personal, alto ticket).
2. **Adaptar los hallazgos al contexto real del negocio, nunca copiarlos literalmente**: servicio de trato 1:1, facturación real <1.000€/mes, un solo coach, sin equipo. Un hallazgo como "vídeo de bienvenida" se adapta a "un único vídeo genérico grabado una vez", no a "un vídeo personalizado por cliente" — eso sería sobre-ingeniería para el volumen real.
3. Citar las fuentes reales con URLs (obligatorio en las respuestas de `WebSearch`) — un hallazgo sin fuente verificable no entra en el diseño como si fuera un hecho.

## Fase 3 — Aislar las decisiones que son del usuario, no del diseño

Cada vez que aparece un punto donde la respuesta correcta depende de una decisión de negocio (no de una comprobación técnica), se pregunta — no se asume. Usar `AskUserQuestion` con una opción recomendada primero. Ejemplos reales de este proyecto:

- Cuándo empieza a contar la ventana de actividad de un agente (Onboarding: alta de cuenta vs. cuestionario vs. primera asignación real).
- El criterio de un aviso automático (¿toda tarea de alta prioridad, o solo ciertas categorías?).
- El alcance de un fix de backend cuando hay varias formas válidas de resolverlo.

No cerrar estos puntos con una suposición "razonable" propia — son del usuario porque afectan cómo se siente el trato con sus clientes reales, no algo que se pueda derivar solo del código.

## Fase 4 — Diseñar el marco fijo (`system-prompt.md`)

Estructura estándar, la misma en los 5 agentes existentes — no hay que reinventar el esqueleto cada vez:

1. **Rol y alcance** — qué SÍ hace y qué NO hace, explícito en dos listas. Incluye el contexto de nivel de servicio si aplica (trato premium 1:1, no chatbot masivo).
2. **Herramientas disponibles (Tool Use, cap. 5)** — tabla con estado real de cada una ("ya existe, confirmado en el código real" / "gap real, documentado"). Nunca una herramienta que no se comprobó en la Fase 1.
3. **Flujo paso a paso (Planning, cap. 6 + Prompt Chaining, cap. 1)** — pasos numerados, cada uno con su disparador y su condición de salida.
4. **Escalación (Human-in-the-Loop, cap. 13 — no negociable)** — lista explícita de señales que cortan cualquier generación de contenido y crean una tarea para el humano. Nunca ambiguo.
5. **Manejo de excepciones — las DOS clases, desde el principio, no añadidas después:**
   - **De negocio**: el cliente da un dato ambiguo, contradictorio, o pide algo fuera de alcance.
   - **Técnicas (Exception Handling and Recovery, cap. 12)**: una herramienta falla, una API devuelve 500, hay timeout. Si el agente opera de forma autónoma (sin revisión humana previa a cada mensaje), esto no es opcional — ver `agentes/soporte-customer-success/modulos/manejo-excepciones-tecnicas.md` como referencia de qué cubrir (detección, reintentos, fallback honesto, escalación, caso límite de que la propia API del modelo falle del todo).
6. **Memoria (Memory Management, cap. 8)** — qué lee antes de generar/responder, y si escribe algo nuevo. Antes de añadir un campo de escritura nueva, comprobar que no exista ya un sistema de registro real para ese dato (no duplicar lo que Bckbs u otro agente ya persiste).
7. **Si hay una etapa de producción de contenido con revisión**: separar Productor/Crítico (Reflection — Producer-Critic, cap. 4) en dos pasadas de LLM con prompts distintos, no una sola pasada que se autoevalúa.
8. **Jerarquía de conflictos (Prioritization, cap. 20)** si hay reglas que podrían chocar entre sí — explícita, no dejarla a la interpretación del momento.
9. **Asignación de modelo por paso (Resource-Aware Optimization, cap. 16)** — no todo el flujo al modelo más caro por defecto.
10. **Notas de mantenimiento** — prerrequisitos operativos pendientes, gaps reales sin cerrar, y el changelog versionado del propio documento.

**Antes de dar el diseño por cerrado: comprobar solapamiento con los agentes ya existentes.** ¿Puede este agente y otro ya construido contactar al mismo cliente en la misma ventana de tiempo? Diseñar la exclusión desde el principio (como debió hacerse entre Soporte y Onboarding, y que se corrigió después porque no se comprobó a tiempo) es más barato que encontrarlo más tarde.

## Fase 5 — Backend: solo lo mínimo necesario, nunca por adelantado

1. No se toca el backend real sin que el usuario lo pida explícitamente. Un gap se documenta primero; se cierra cuando el usuario decide que toca.
2. Al implementar: reutilizar servicios/patrones ya existentes en el propio backend (ej. `TaskEscalationAlertService` reutilizó exactamente el patrón de `EmptySessionAlertService`, no inventó uno nuevo).
3. Tests reales contra el motor de base de datos real del proyecto (no SQLite si el proyecto ya requiere MySQL/MariaDB por sus migraciones), suite completa en verde antes de pushear — nunca "debería funcionar".
4. Verificar que el despliegue real llegó — no asumir que un `git push` es suficiente (lección real de este proyecto: el pipeline automático llevaba fallando semanas sin que nadie lo notara).

## Fase 6 — Documentar y sincronizar, siempre en el mismo orden

1. `git fetch origin main` antes de editar y otra vez justo antes de pushear — varias sesiones trabajan en paralelo sobre este repo, y los números de versión/ítem colisionan si no se comprueba.
2. Actualizar, en este orden: el `system-prompt.md` del agente (versión + changelog inline) → su `CHANGELOG.md` → `docs/TAREAS_PENDIENTES.md` (ítem nuevo, número siguiente libre) → `docs/roadmap.md` (tabla "Agentes existentes") → `docs/ORGANIGRAMA_AGENTES.md` (nota de secuencia de implementación) si es un agente nuevo del organigrama.
3. Commits con mensaje descriptivo real (qué y por qué, no solo qué) y los trailers de atribución de la sesión que hace el cambio.

## Fase 7 — Verificar que los patrones citados se aplican de verdad, no solo se nombran

Antes de dar el diseño por terminado, releer cada cita de capítulo del propio documento y comprobar que el contenido debajo de esa cita hace lo que el capítulo describe — no solo que el nombre de la sección coincide. El propio proyecto tuvo este error real: una sección llamada "Manejo de excepciones" en cada agente, pero el capítulo 12 (Exception Handling and Recovery) habla de fallos técnicos y la sección solo cubría casos de negocio — el nombre coincidía, el patrón no. Revisar `docs/METODOLOGIA_DISENO_AGENTES.md` (este documento) no sustituye leer el capítulo real en `Agentic-Design-Patterns/` cuando haya duda de si un patrón se está aplicando de verdad.
