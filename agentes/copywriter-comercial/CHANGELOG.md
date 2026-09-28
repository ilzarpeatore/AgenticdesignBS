# Changelog — Agente Copywriter Comercial (blog web, captación de clientes)

## v0.2.0 — 2026-09-28

El usuario pidió profundizar la investigación de mercado de este agente (captación) y del Copywriter educativo (retención), y reforzar los límites de ambos.

- **Mezcla de contenido de autoridad y de conversión**: la investigación distingue entre contenido de autoridad (filosofía de coaching, mitos desmontados) y contenido de conversión estricto (por qué contratar, FAQs) — un blog 100% conversión rinde peor en SEO y confianza. Nuevo criterio en el Paso 1 (sección 3): por defecto 2 de cada 3 ciclos son de captación (palabra clave long-tail) y 1 de autoridad (sin CTA de venta forzada), ajustable por el coach.
- **Límite legal real, no solo de tono**: "no promete resultados no garantizados" ya existía desde v0.1.0 como buena práctica de marketing responsable; ahora se documenta su base legal real — la Ley 34/1988 General de Publicidad considera no puesta cualquier cláusula que garantice un resultado económico/comercial, y la Directiva 2006/114/CE regula la publicidad engañosa. El Crítico (Paso 4) lo trata como límite no negociable, no como una preferencia de estilo.
- Fuentes: [Personal Trainer Marketing 2026 — Trainero](https://blog.trainero.com/personal-trainer-marketing/), [Content Marketing Strategies for Personal Trainers — Contentbase](https://contentbase.com/blog/personal-trainer-content-marketing-strategies/), [Ley General de Publicidad — BOE](https://www.boe.es/buscar/pdf/1988/BOE-A-1988-26156-consolidado.pdf), [Ley General de Publicidad — Wikipedia](https://es.wikipedia.org/wiki/Ley_General_de_Publicidad_(Espa%C3%B1a)).

## v0.1.0 — 2026-09-28

Primer diseño. El usuario pidió separar el contenido del blog en dos: educativo (app + web, ya diseñado en `agentes/copywriter/`) y de captación de nuevos clientes (solo web) — hoy ambos blogs comparten el mismo endpoint (`GET post-list`) sin ninguna distinción.

- **Requirió backend nuevo primero**, no solo diseño: campo `channel` (`app`/`web`/`both`) en `posts` de Bckbs (commit `70300b8`, migración + `Post::scopeChannel()` + validación en `Admin\PostController` + filtro opcional en `API\PostController::getList` + 6 tests). Retrocompatible — ningún consumidor que no mande el parámetro ve cambiar nada.
- **Decisión razonada de usar dos agentes, no uno** (el usuario preguntó explícitamente): objetivo distinto (educar vs. captar), riesgo distinto (el contenido de venta puede prometer de más o mencionar precios, el educativo no tiene ese riesgo), y separar los agentes hace estructuralmente imposible que este olvide fijar `channel: web`.
- **Investigación de mercado** (fuentes en `docs/TAREAS_PENDIENTES.md`): el contenido de captación que mejor funciona aporta valor real antes de vender (mejor SEO y más confianza que copy puramente promocional) — de ahí la estructura "valor primero, CTA al final" del Paso 3.
- **Guardrails de marketing responsable incorporados directamente** (el organigrama los asigna a "Control ventas"/"Control marketing", niveles que no existen todavía como agentes propios): el Crítico (Paso 4) revisa específicamente que no se prometan resultados no garantizados, que no se mencione un precio sin confirmación del coach, y que la CTA sea honesta.
- **`channel: web` es un campo fijo, no una elección** — este agente nunca tiene un camino en su flujo que produzca `app` o `both`.
- **Pendiente fuera de este repo**: los repos `bsa` (app) y `webbs` (web) todavía no mandan `?channel=` a `GET post-list` — el filtro existe en Bckbs pero no se nota en producción hasta que esos dos repos lo empiecen a usar.
