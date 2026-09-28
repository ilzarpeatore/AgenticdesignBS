# Changelog — Agente Copywriter (contenido educativo del blog in-app)

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
