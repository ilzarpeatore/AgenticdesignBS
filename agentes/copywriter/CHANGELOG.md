# Changelog — Agente Copywriter (contenido educativo del blog in-app)

## v0.3.0 — 2026-09-28

El usuario pidió profundizar la investigación de mercado de este agente (retención) y del Copywriter Comercial (captación), y reforzar los límites de ambos.

- **Formato pensado para retención, no solo para SEO**: la investigación confirma que el contenido corto y estructurado (microaprendizaje) retiene mejor que artículos largos que intentan cubrirlo todo — ajustado el criterio de extensión del Paso 3 (sección 3).
- **Límite legal real añadido, no solo editorial**: cualquier afirmación de que un alimento/suplemento "ayuda a" o "mejora" algo es una declaración de propiedad saludable regulada por el Reglamento (CE) 1924/2006, con una lista cerrada de 222 declaraciones autorizadas (Reglamento (UE) 432/2012) — nueva comprobación explícita en el Paso 5 (sección 3) y en "Qué NO hace" (sección 1). Antes este límite solo existía como "cita una fuente real"; ahora se distingue explícitamente de una fuente válida en general: una declaración de propiedad saludable necesita estar en la lista autorizada, no solo tener respaldo científico razonable.
- Fuentes: [How to Retain Online Fitness Clients — FitBudd](https://www.fitbudd.com/post/how-to-retain-online-fitness-clients-15-strategies-that-work), [13 Proven Strategies to Increase App Retention — Orangesoft](https://orangesoft.co/blog/strategies-to-increase-fitness-app-engagement-and-retention), [Reglamento (CE) 1924/2006 — BOE](https://www.boe.es/doue/2006/404/L00009-00025.pdf), [Declaraciones nutricionales y de propiedades saludables — Comunidad de Madrid](https://www.comunidad.madrid/salud/declaraciones-nutricionales-propiedades-saludables-alimentos).

## v0.2.0 — 2026-09-28

Corrección real sobre v0.1.0: sí existe una web pública (`webbs`) que sirve el mismo blog que la app, sincronizada sin ningún filtro hasta ahora — la afirmación anterior ("no hay web pública") era incorrecta.

- El usuario pidió separar el contenido en dos: educativo (app + web, este agente) y de captación de nuevos clientes (solo web, nuevo agente hermano **Copywriter Comercial**, `agentes/copywriter-comercial/`).
- Requirió backend nuevo: campo `channel` (`app`/`web`/`both`) en `posts` de Bckbs (commit `70300b8`).
- Este agente pasa a fijar siempre `channel: both` explícitamente en el Paso 6, en vez de depender del valor por defecto de la columna — no es lo mismo "no decir nada y que el default lo resuelva" que "confirmar activamente que este contenido debe verse en los dos sitios".
- Sección 1 actualizada: el punto "no genera contenido de venta" ahora referencia al agente hermano en vez de decir que esa pieza del organigrama no tiene integración real (ya la tiene, para el Copywriter Comercial).

## v0.1.0 — 2026-09-28

Primer diseño, a petición explícita del usuario tras haberlo descartado provisionalmente en la tanda anterior (`docs/TAREAS_PENDIENTES.md`, ítem 2.26) por falta de señal de intención de negocio.

- **Investigación más profunda que corrigió el descarte anterior:** Bckbs tiene un blog interno completo y realmente usado — `Post`/`BlogCategory`/`AdminPostController`, con 3 categorías reales (Entrenamiento, Nutrición, Hábitos, `database/seeders/BlogCategorySeeder.php`) y contenido semilla real desde 2026-09-14 (`BlogPostSeeder.php`), consumido por la propia app (`GET post-list`, `POST post-detail`). No es un blog público de marketing ni tiene nada que ver con redes sociales externas — es contenido educativo visible solo a clientes ya dados de alta dentro de la app.
- **Alcance reencuadrado respecto al organigrama original:** la descripción original del "Agente Copywriter" habla de emails, textos de venta y guiones multicanal — ninguna de esas piezas tiene integración real en Bckbs hoy. Este diseño se ciñe a lo único que sí tiene base real: artículos educativos para el blog in-app.
- **Investigación de mercado** (fuentes en `docs/TAREAS_PENDIENTES.md`): el contenido educativo se confirma como herramienta de retención, no de captación — coincide con la naturaleza del blog real (dentro de la app, para clientes existentes).
- **Publicación con Human-in-the-Loop no negociable** (cap. 13): todo artículo se crea con `status: draft`, nunca `publish` — el coach revisa y publica él mismo, mismo principio que "el Importador nunca asigna" o "el Crítico revisa, el coach aprueba".
- **Patrón Productor/Crítico** (Reflection, cap. 4), igual que Training/Nutrición: una segunda pasada de LLM revisa el borrador (aporta algo real, tono correcto, la fuente respalda la afirmación principal) antes incluso de la validación mecánica — quien redacta no es quien aprueba.
- **Guardrail de coherencia científica**: antes de escribir sobre un tema que los módulos de conocimiento de los Productores de entrenamiento/nutrición ya cubren, se leen primero — el blog no puede contradecir lo que el sistema ya le dice a un cliente real en su plan.
- **Sin gaps de backend**: a diferencia de todos los agentes anteriores, este no necesitó ningún cambio en Bckbs — `AdminPostController` ya soporta todo lo necesario (crear en borrador, categorizar, etiquetar, portada opcional).
- **Decisiones tomadas de forma autónoma**, documentadas para revisión: cadencia mensual (un artículo por ciclo), notificación al coach reutilizando `StaffAlertService`, asignación de modelo por paso.
