# Changelog — Agente de Soporte / Customer Success

## v0.2.0 — 2026-09-27

El usuario pidió explícitamente que el agente no "suene a bot" — que responda con la formación real de un profesional de ciencias del deporte combinado con atención al cliente, no como un FAQ automatizado que reconoce palabras clave.

- **Nuevo `modulos/tono-y-conocimiento-deportivo.md`:** persona (cómo habla, cómo adapta cada respuesta al cliente real en vez de copiar una plantilla), principios de atención al cliente (validar antes de resolver, nunca un "no" seco, ser concreto no genérico), y un banco de **patrones** de respuesta — no plantillas de copiar/pegar — para las dudas reales más frecuentes: agujetas/DOMS (con la línea exacta que obliga a escalar en vez de tranquilizar), "no veo resultados" (reencuadre honesto con datos reales de su historial, nunca prometiendo un plazo), desliz puntual en dieta/entrenamiento (quitar presión sin sugerir "compensar"), uso de la app, bajón de motivación, y curiosidad sobre por qué su plan está diseñado así (citando el razonamiento real ya guardado, nunca inventando uno).
- **Guardrail explícito:** este módulo nunca amplía el alcance de la sección 1 del `system-prompt.md` — mejora cómo se responde dentro de lo ya permitido. Ninguno de sus patrones autoriza saltarse el cribado del Paso 2 ni la escalación de la sección 4; varios patrones incluyen explícitamente cuándo, pese a "sonar bien", hay que escalar igual (ej. si "no veo resultados" se repite, es señal de riesgo de baja, no solo una duda a resolver una vez).
- `system-prompt.md` sube a v0.2.0: sección 1 y Paso 4 del flujo referencian el nuevo módulo.

## v0.1.0 — 2026-09-27

Primer diseño. Primer agente operativo nuevo tras la transición M0→M1 (ver `docs/roadmap.md` y `docs/ORGANIGRAMA_AGENTES.md`), priorizado por el usuario sobre el Agente de Onboarding por cubrir más volumen real de trabajo hoy.

- **Investigación previa contra el código real de Bckbs** (mismo criterio que los otros 3 agentes: no inventar integraciones sin comprobar) — se encontraron dos gaps reales, ninguno bloqueante: **(1)** no existe forma de buscar un usuario por `phone_number` (`UserController::index` solo busca por nombre/email/username) — el mapeo teléfono→cliente_id vive en una hoja mantenida a mano hasta que el volumen lo justifique. **(2)** `tasks.category` no tiene un valor `soporte` (solo `entrenamiento,nutricion,revisiones,otro`) — se usa `otro` por ahora.
- **Sí existen ya, confirmado en el código real:** `GET client-calendar-data` (admin, `ClientProfileCalendarController::getMergedMonth`) para preguntas factuales sobre el plan del cliente, y `POST task-store` (`TaskController::store`) como mecanismo de escalación a humano — ambos reutilizados tal cual, sin construir nada nuevo en Bckbs.
- **Canal confirmado por el usuario:** WhatsApp (número personal/business), sin integración con Bckbs todavía — de ahí que el diseño use Twilio + n8n (infraestructura de M1) en vez de asumir un canal distinto.
- Diseño completo en `system-prompt.md`: rol/alcance (qué responde directo vs. qué escalar siempre, sin excepción — programación/nutrición, precios/cancelación, salud), flujo paso a paso, reglas de escalación en tiempo real (no espera a ningún resumen semanal, el Agente Director ni siquiera existe todavía), manejo de excepciones, asignación de modelo.
- Nuevo `esquemas/log-interaccion.schema.json` — adapta el JSON de ejemplo de `docs/ORGANIGRAMA_AGENTES.md` a los datos reales disponibles (cliente_id real, no un id genérico; task_id_creado quedando trazado si escaló).
- **No desplegable todavía** — quedan prerrequisitos puramente operativos (cuenta WhatsApp Business/Twilio, instancia n8n, hojas de mapeo y de log) documentados en `docs/TAREAS_PENDIENTES.md`, ninguno de código.
- Sin Control de Soporte todavía (nivel 2 del organigrama) — por diseño, se añade solo cuando este operativo funcione sin supervisión constante.
