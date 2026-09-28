# Changelog — Agente de Control Contenido (audita Copywriter + Copywriter Comercial)

## v0.2.0 — 2026-09-28

El usuario pidió maximizar la eficiencia de este agente. Investigada la documentación real de la API de Claude (skill interna `claude-api`, `shared/agent-design.md` y `shared/cost-optimization.md`, snapshot 2026-06-24) antes de cambiar nada.

- **Hallazgo honesto de partida**: con el volumen real de este agente (una auditoría al mes, un puñado de posts), el coste en tokens ya es insignificante en cualquier configuración razonable. La eficiencia que de verdad aporta aquí es de arquitectura — menos llamadas, menos ambigüedad — no la optimización de céntimos que tendría sentido a mayor escala.
- **Consolidación de 3 llamadas a 1**: los chequeos de temas cruzados, tono y salud/nutrición pasan de ser 3 pasos/llamadas de juicio separados a un único prompt con salida estructurada (Paso 3, v0.2.0) — menos turnos, un solo prefijo de contexto, salida directamente parseable para la clasificación de riesgo.
- **Nuevo filtro determinista, sin modelo**: comparar `updated_at` contra `created_at` (Paso 2) decide qué posts necesitan de verdad el re-chequeo de salud — solo los que el coach editó después de la revisión del Crítico. Evita gastar tokens releyendo contenido que ya pasó por el Crítico sin ningún cambio desde entonces.
- **Higiene de tokens**: el chequeo de temas/tono usa título+descripción, no el artículo completo; el contenido completo solo se manda de los posts que superan el filtro anterior.
- **Effort `medium`, no el más alto por defecto**: la investigación de coste real de Anthropic muestra curvas casi planas en trabajo de tipo auditoría/clasificación — `medium` iguala la precisión del nivel por defecto a una fracción del coste.
- **Levers deliberadamente descartados, documentados con su razón**: caching entre ciclos (los ciclos están separados por un mes, muy por encima de cualquier ventana de caché real) y Batch API (pensada para volumen alto sin nadie esperando — aquí hay una llamada real al mes, el ahorro sería de céntimos). Añadirlos habría sido sobre-optimizar por completitud, no por necesidad real.

## v0.1.0 — 2026-09-28

Primer diseño, a petición explícita del usuario. Primer agente de Control (nivel 2 del organigrama) de todo el proyecto.

- **Decisión de alcance real, no la del organigrama original al pie de la letra**: el organigrama define "Control contenido" y "Control ventas"/"Control marketing" por separado. Estos dos últimos no tienen ningún agente operativo real que auditar hoy (sin Closer/CRM ni Ads/Email Marketing) — auditar el Copywriter Comercial (que sí existe) encaja mejor dentro de este Control contenido, absorbiendo su chequeo legal/comercial, que esperar a un Control ventas/marketing sin nada más que controlar.
- **Groundeado sin ningún backend nuevo**: toda la auditoría se hace sobre `GET admin/posts`, el mismo endpoint que ya usan los dos Copywriter para su propia memoria — sin filtrar por `channel`, que es exactamente lo que le falta a cada agente por separado para comparar entre sí.
- **Valor real que ningún Copywriter individual puede dar**: comparación de temas entre los dos agentes (Multi-Agent Collaboration, cap. 7), consistencia de tono entre canales, y visión de conjunto del cumplimiento del calendario de publicación — cada uno de los dos Copywriter solo se compara contra su propio historial.
- **Tensión documentada, no resuelta en silencio**: `docs/ORGANIGRAMA_AGENTES.md` recomienda añadir un Control solo cuando el operativo correspondiente funcione sin supervisión constante — ni el Copywriter ni el Copywriter Comercial han corrido todavía un ciclo real. Se diseña ahora a petición explícita del usuario, pero queda marcado como "no activar todavía" (sección 8), con un criterio de activación concreto (2 ciclos reales por agente).
