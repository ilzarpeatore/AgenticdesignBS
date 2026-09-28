# Changelog — Agente de Control Contenido (audita Copywriter + Copywriter Comercial)

## v0.1.0 — 2026-09-28

Primer diseño, a petición explícita del usuario. Primer agente de Control (nivel 2 del organigrama) de todo el proyecto.

- **Decisión de alcance real, no la del organigrama original al pie de la letra**: el organigrama define "Control contenido" y "Control ventas"/"Control marketing" por separado. Estos dos últimos no tienen ningún agente operativo real que auditar hoy (sin Closer/CRM ni Ads/Email Marketing) — auditar el Copywriter Comercial (que sí existe) encaja mejor dentro de este Control contenido, absorbiendo su chequeo legal/comercial, que esperar a un Control ventas/marketing sin nada más que controlar.
- **Groundeado sin ningún backend nuevo**: toda la auditoría se hace sobre `GET admin/posts`, el mismo endpoint que ya usan los dos Copywriter para su propia memoria — sin filtrar por `channel`, que es exactamente lo que le falta a cada agente por separado para comparar entre sí.
- **Valor real que ningún Copywriter individual puede dar**: comparación de temas entre los dos agentes (Multi-Agent Collaboration, cap. 7), consistencia de tono entre canales, y visión de conjunto del cumplimiento del calendario de publicación — cada uno de los dos Copywriter solo se compara contra su propio historial.
- **Tensión documentada, no resuelta en silencio**: `docs/ORGANIGRAMA_AGENTES.md` recomienda añadir un Control solo cuando el operativo correspondiente funcione sin supervisión constante — ni el Copywriter ni el Copywriter Comercial han corrido todavía un ciclo real. Se diseña ahora a petición explícita del usuario, pero queda marcado como "no activar todavía" (sección 8), con un criterio de activación concreto (2 ciclos reales por agente).
